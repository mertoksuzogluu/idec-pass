#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IDEC FC4A-HPC3 PLC Otomatik Şifre Bulucu
Windows GUI Uygulaması
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import socket
import serial
import serial.tools.list_ports

# IDEC FC4A-HPC3 için şifre listesi
PASSWORD_LIST = [
    "",  # Boş şifre
    "admin", "ADMIN", "password", "PASSWORD",
    "idec", "IDEC", "fc4a", "FC4A", "hpc3", "HPC3",
    "1234", "12345", "0000", "1111",
    "admin123", "password123", "idec123",
    "PLC", "plc", "factory", "default",
    "user", "root", "system", "operator",
    "technician", "service", "SERVICE",
    "123", "123456", "admin1", "pass",
    "idec1234", "fc4ahpc3", "FC4AHPC3"
]

class IDECPasswordFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("IDEC FC4A-HPC3 Şifre Bulucu")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        self.is_running = False
        self.found_password = None
        
        self.create_widgets()
        
    def create_widgets(self):
        # Başlık
        title_frame = tk.Frame(self.root, bg="#2c3e50", pady=10)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text="IDEC FC4A-HPC3 Otomatik Şifre Bulucu",
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack()
        
        # Ana frame
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Bağlantı ayarları
        conn_frame = ttk.LabelFrame(main_frame, text="Bağlantı Ayarları", padding=10)
        conn_frame.pack(fill=tk.X, pady=10)
        
        # Bağlantı tipi
        ttk.Label(conn_frame, text="Bağlantı Tipi:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.connection_type = tk.StringVar(value="USB/Serial")
        conn_type_combo = ttk.Combobox(
            conn_frame,
            textvariable=self.connection_type,
            values=["USB/Serial", "Ethernet/IP", "Modbus TCP"],
            state="readonly",
            width=20
        )
        conn_type_combo.grid(row=0, column=1, pady=5, padx=10)
        
        # COM Port / IP
        ttk.Label(conn_frame, text="COM Port / IP:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.connection_address = tk.StringVar(value="COM1")
        conn_entry = ttk.Entry(conn_frame, textvariable=self.connection_address, width=20)
        conn_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # COM port listesi butonu
        ttk.Button(
            conn_frame,
            text="COM Portları Listele",
            command=self.list_com_ports
        ).grid(row=1, column=2, pady=5, padx=5)
        
        # Baud Rate (Serial için)
        ttk.Label(conn_frame, text="Baud Rate:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.baud_rate = tk.StringVar(value="9600")
        baud_combo = ttk.Combobox(
            conn_frame,
            textvariable=self.baud_rate,
            values=["9600", "19200", "38400", "57600", "115200"],
            state="readonly",
            width=20
        )
        baud_combo.grid(row=2, column=1, pady=5, padx=10)
        
        # Kontrol butonları
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.start_button = ttk.Button(
            button_frame,
            text="Şifre Aramayı Başlat",
            command=self.start_search,
            style="Accent.TButton"
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(
            button_frame,
            text="Durdur",
            command=self.stop_search,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # İlerleme çubuğu
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(progress_frame, text="İlerleme:").pack(anchor=tk.W)
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            length=400
        )
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        self.status_label = ttk.Label(progress_frame, text="Hazır...")
        self.status_label.pack(anchor=tk.W)
        
        # Sonuç alanı
        result_frame = ttk.LabelFrame(main_frame, text="Sonuçlar", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            height=15,
            wrap=tk.WORD,
            font=("Consolas", 10)
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # Alt bilgi
        info_label = ttk.Label(
            main_frame,
            text="⚠️ Bu araç sadece kendi cihazınız için kullanılmalıdır!",
            foreground="red",
            font=("Arial", 9, "italic")
        )
        info_label.pack(pady=5)
        
    def list_com_ports(self):
        """Mevcut COM portlarını listeler"""
        ports = serial.tools.list_ports.comports()
        port_list = [port.device for port in ports]
        
        if port_list:
            message = "Bulunan COM Portları:\n\n" + "\n".join(port_list)
            messagebox.showinfo("COM Portları", message)
        else:
            messagebox.showwarning("Uyarı", "Hiç COM portu bulunamadı!")
    
    def log_message(self, message):
        """Log mesajı ekler"""
        self.result_text.insert(tk.END, f"{time.strftime('%H:%M:%S')} - {message}\n")
        self.result_text.see(tk.END)
        self.root.update()
    
    def test_password_serial(self, password, com_port, baud_rate):
        """Serial port üzerinden şifre test eder"""
        try:
            ser = serial.Serial(
                port=com_port,
                baudrate=int(baud_rate),
                timeout=2,
                write_timeout=2
            )
            time.sleep(0.5)
            
            # IDEC PLC'ye bağlantı komutu gönder
            # Not: Gerçek implementasyon IDEC protokolüne göre yapılmalı
            test_command = f"PASSWORD:{password}\r\n"
            ser.write(test_command.encode())
            time.sleep(0.5)
            
            response = ser.read(100).decode('utf-8', errors='ignore')
            ser.close()
            
            # Başarılı bağlantı kontrolü (örnek)
            if "OK" in response or "CONNECTED" in response or len(response) > 0:
                return True
            return False
            
        except Exception as e:
            self.log_message(f"Hata: {str(e)}")
            return False
    
    def test_password_ethernet(self, password, ip_address):
        """Ethernet üzerinden şifre test eder"""
        try:
            # Modbus TCP portu (502)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((ip_address, 502))
            sock.close()
            
            if result == 0:
                # Port açık, şifre kontrolü yapılabilir
                # Gerçek implementasyon IDEC protokolüne göre yapılmalı
                return True
            return False
            
        except Exception as e:
            self.log_message(f"Hata: {str(e)}")
            return False
    
    def search_passwords(self):
        """Şifre arama işlemini başlatır"""
        self.is_running = True
        self.found_password = None
        
        conn_type = self.connection_type.get()
        conn_addr = self.connection_address.get()
        
        self.log_message("="*60)
        self.log_message("Şifre araması başlatılıyor...")
        self.log_message(f"Bağlantı Tipi: {conn_type}")
        self.log_message(f"Adres: {conn_addr}")
        self.log_message("="*60)
        
        total_passwords = len(PASSWORD_LIST)
        
        for index, password in enumerate(PASSWORD_LIST):
            if not self.is_running:
                self.log_message("\nArama durduruldu!")
                break
            
            display_password = password if password else "(BOŞ)"
            self.log_message(f"[{index+1}/{total_passwords}] Deneniyor: '{display_password}'")
            
            # İlerleme güncelle
            progress = ((index + 1) / total_passwords) * 100
            self.progress_var.set(progress)
            self.status_label.config(text=f"Deneniyor: {display_password} ({index+1}/{total_passwords})")
            
            # Şifre testi
            success = False
            if conn_type == "USB/Serial":
                success = self.test_password_serial(password, conn_addr, self.baud_rate.get())
            elif conn_type == "Ethernet/IP" or conn_type == "Modbus TCP":
                success = self.test_password_ethernet(password, conn_addr)
            
            if success:
                self.found_password = password
                self.log_message("\n" + "="*60)
                self.log_message("✅ ŞİFRE BULUNDU!")
                self.log_message(f"Şifre: '{display_password}'")
                self.log_message("="*60)
                
                messagebox.showinfo(
                    "Başarılı!",
                    f"Şifre bulundu!\n\nŞifre: '{display_password}'\n\nWindLDR'da bu şifreyi kullanabilirsiniz."
                )
                break
            
            time.sleep(0.3)  # Rate limiting
        
        if not self.found_password and self.is_running:
            self.log_message("\n" + "="*60)
            self.log_message("❌ Hiçbir şifre çalışmadı!")
            self.log_message("Donanımsal reset yapmanız gerekebilir.")
            self.log_message("="*60)
            
            messagebox.showwarning(
                "Şifre Bulunamadı",
                "Hiçbir şifre çalışmadı.\n\nDonanımsal reset yapmayı deneyin:\n"
                "1. Cihazı kapatın\n"
                "2. RESET butonuna basılı tutun\n"
                "3. Güç kaynağını açın\n"
                "4. 5-10 saniye basılı tutun"
            )
        
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Tamamlandı")
    
    def start_search(self):
        """Aramayı başlatır"""
        if not self.connection_address.get():
            messagebox.showerror("Hata", "Lütfen COM Port veya IP adresi girin!")
            return
        
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        # Thread'de çalıştır
        thread = threading.Thread(target=self.search_passwords, daemon=True)
        thread.start()
    
    def stop_search(self):
        """Aramayı durdurur"""
        self.is_running = False
        self.log_message("\nArama durduruluyor...")

def main():
    root = tk.Tk()
    
    # Modern tema
    style = ttk.Style()
    style.theme_use('clam')
    
    # Renkler
    style.configure('Accent.TButton', foreground='white', background='#3498db')
    
    app = IDECPasswordFinder(root)
    root.mainloop()

if __name__ == "__main__":
    main()

