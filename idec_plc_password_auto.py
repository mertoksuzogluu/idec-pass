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

try:
    from pywinauto import Application as PywinautoApp
    from pywinauto import Desktop as PywinautoDesktop
    from pywinauto.findwindows import ElementNotFoundError
    HAS_PYWINAUTO = True
except ImportError:
    HAS_PYWINAUTO = False
    PywinautoDesktop = None

# Yaygın şifre listesi (önce bunlar denenecek)
PASSWORD_LIST = [
    "", "admin", "ADMIN", "password", "PASSWORD", "idec", "IDEC",
    "fc4a", "FC4A", "hpc3", "HPC3", "1234", "12345", "0000", "1111",
    "admin123", "password123", "idec123", "PLC", "plc", "factory", "default",
    "user", "root", "system", "operator", "technician", "service", "SERVICE",
    "123", "123456", "admin1", "pass", "idec1234", "fc4ahpc3", "FC4AHPC3",
    # Ek yaygınlar
    "passwd", "pwd", "login", "changeme", "welcome", "letmein", "master",
    "kontrol", "sifre", "parola", "default1", "admin2", "root123", "system1",
    "operator1", "tech", "service1", "maintenance", "plc1", "plc123", "idec1",
    "fc4a1", "hpc31", "1234567", "12345678", "0123456", "000000", "111111",
    "121212", "123123", "654321", "555555", "999999", "777777", "666666",
    "888888", "4321", "1122", "2211", "3333", "4444", "5555", "6666", "7777",
    "9999", "0123", "01234", "12340", "0001", "0002", "1000", "2000", "9998",
    "admin0", "Admin", "PASSWORD1", "Password", "Password1", "Password123",
    "root1", "Root", "USER", "User", "User1", "guest", "GUEST", "test", "TEST",
    "demo", "DEMO", "temp", "TEMP", "backup", "access", "ACCESS", "control",
    "CONTROL", "main", "MAIN", "super", "SUPER", "superuser", "supervisor",
    "manager", "MANAGER", "maintenance1", "tech1", "engineer", "ENGINEER",
    "service123", "support", "SUPPORT", "help", "id", "ID", "serial", "SERIAL",
    "device", "DEVICE", "panel", "PANEL", "machine", "MACHINE", "factory1",
    "default123", "init", "INIT", "setup", "SETUP", "config", "CONFIG",
    "idec2020", "idec2021", "idec2022", "idec2023", "idec2024", "plc2020",
    "fc4a1234", "hpc31234", "windldr", "WINDLDR", "wind", "ladder", "scada",
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "00", "01", "10", "11",
    "12", "21", "22", "99", "000", "001", "010", "100", "111", "222", "999",
    "1230", "1231", "1232", "1233", "1235", "1236", "1237", "1238", "1239",
    "1240", "1243", "1324", "1342", "1423", "1432", "2134", "2314", "2341",
    "3124", "3214", "3241", "3412", "3421", "4123", "4213", "4312", "4321",
    "1112", "1121", "1211", "2111", "2221", "2212", "2122", "1222",
    "2020", "2021", "2022", "2023", "2024", "2025", "1990", "1995", "2000",
    "2001", "2010", "2015", "1970", "1980", "12345", "54321", "11111", "00000",
    "123321", "112233", "1010", "2020", "3030", "4040", "5050", "6060", "7070",
    "8080", "9090", "1001", "2002", "3003", "4004", "5005", "6006", "7007",
    "8008", "9009", "1100", "2200", "3300", "4400", "5500", "6600", "7700",
    "8800", "9900", "1000", "2000", "3000", "4000", "5000", "6000", "7000",
    "8000", "9000", "9999", "8888", "7777", "6666", "5555", "4444", "3333",
    "2222", "1111", "1004", "1005", "1006", "1024", "1025", "2048", "4096",
    "11112", "11122", "11222", "12222", "22221", "22222", "33333", "44444",
    "55555", "66666", "77777", "88888", "99999", "12340", "12341", "12342",
    "12343", "12344", "12346", "12347", "12348", "12349", "12350", "12351",
]

# IDEC şifre konfigürasyonu: Resmi dokümanda net uzunluk/karakter seti yok.
# Bazı kaynaklarda "4 karakter şifre" geçiyor; sadece rakam veya harf+rakam olabilir.
IDEC_PASSWORD_NOTE = "IDEC: Bazı dokümanlarda 4 karakter şifre geçer; rakam veya harf+rakam olabilir (resmi spec yok)."

def _number_passwords(digits):
    """Rakamlardan oluşan tüm N haneli şifreleri üretir (0'dan 10^N-1)."""
    for i in range(10 ** digits):
        yield str(i).zfill(digits)

def _alphanum4_passwords():
    """4 karakter: sadece küçük harf (a-z) + rakam (0-9) = 36^4 = 1.679.616 kombinasyon."""
    import itertools
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    for c in itertools.product(chars, repeat=4):
        yield "".join(c)

def password_iterator(mode):
    """
    Seçilen moda göre (index, toplam, şifre) üretir.
    mode: "list", "list_4", "list_5", "list_6", "only_4", "only_5", "only_6", "only_4alpha"
    """
    n_list = len(PASSWORD_LIST)
    ALPHA4_TOTAL = 36 ** 4  # 1_679_616
    if mode == "list":
        for i, p in enumerate(PASSWORD_LIST):
            yield (i + 1, n_list, p)
        return
    # Önce liste
    for i, p in enumerate(PASSWORD_LIST):
        if mode == "list_4":
            total = n_list + 10000
        elif mode == "list_5":
            total = n_list + 100000
        elif mode == "list_6":
            total = n_list + 1000000
        else:
            total = n_list
        yield (i + 1, total, p)
    # Sonra sayısal / alfanumerik brute force
    if mode == "list_4":
        for i, p in enumerate(_number_passwords(4)):
            yield (n_list + i + 1, n_list + 10000, p)
    elif mode == "list_5":
        for i, p in enumerate(_number_passwords(5)):
            yield (n_list + i + 1, n_list + 100000, p)
    elif mode == "list_6":
        for i, p in enumerate(_number_passwords(6)):
            yield (n_list + i + 1, n_list + 1000000, p)
    elif mode == "only_4":
        for i, p in enumerate(_number_passwords(4)):
            yield (i + 1, 10000, p)
    elif mode == "only_5":
        for i, p in enumerate(_number_passwords(5)):
            yield (i + 1, 100000, p)
    elif mode == "only_6":
        for i, p in enumerate(_number_passwords(6)):
            yield (i + 1, 1000000, p)
    elif mode == "only_4alpha":
        for i, p in enumerate(_alphanum4_passwords()):
            yield (i + 1, ALPHA4_TOTAL, p)

def get_total_count(mode):
    n = len(PASSWORD_LIST)
    counts = {
        "list": n,
        "list_4": n + 10000,
        "list_5": n + 100000,
        "list_6": n + 1000000,
        "only_4": 10000,
        "only_5": 100000,
        "only_6": 1000000,
        "only_4alpha": 36 ** 4,  # 1_679_616
    }
    return counts.get(mode, n)

def _conn_type_key(display_value):
    """Bağlantı tipi combobox metnini sabit anahtara çevirir."""
    v = (display_value or "").strip()
    if "WindLDR" in v or "windldr" in v.lower():
        return "windldr"
    if "Pentra" in v:
        return "pentra"
    if "USB" in v or "Serial" in v:
        return "serial"
    if "Ethernet" in v:
        return "ethernet"
    if "Modbus" in v:
        return "modbus"
    return "serial"

# --- IDEC Pentra (Ethernet port 2101) - Capkj2/Idec-password-cracker referansı ---
PENTRA_DEFAULT_PORT = 2101
PENTRA_PREAMBLE_HEX = "0546463057560000000000000000"  # 26 hex chars
VALID_PASS_RESPONSE = bytes([0x06, 0x30, 0x31, 0x30, 0x33, 0x37, 0x0D])
INVALID_PASS_RESPONSE = bytes([0x06, 0x30, 0x31, 0x32, 0x30, 0x35, 0x33, 0x30, 0x0D])

def _pentra_build_packet(password_number):
    """
    IDEC Pentra paketi oluşturur (sayısal şifre).
    Kaynak: https://github.com/Capkj2/Idec-password-cracker (Pass-code.cpp)
    password_number: int (1-99999999)
    Returns: 18-byte packet veya en fazla 18 byte (hex string 36 char, eksikse 00 ile doldurulur).
    """
    pad = 2
    if password_number >= 10 and password_number < 100:
        pad = 3
    elif password_number >= 100 and password_number < 1000:
        pad = 4
    elif password_number >= 1000 and password_number < 10000:
        pad = 5
    elif password_number >= 10000 and password_number < 100000:
        pad = 6
    elif password_number >= 100000 and password_number < 1000000:
        pad = 7
    elif password_number >= 1000000 and password_number < 10000000:
        pad = 8
    elif password_number >= 10000000:
        pad = 9
    s = str(password_number).zfill(pad)
    hs = s.encode().hex().upper()
    packet_hex = list(PENTRA_PREAMBLE_HEX)
    start = 12
    for i, c in enumerate(hs):
        if start + i < len(packet_hex):
            packet_hex[start + i] = c
    packet_hex = "".join(packet_hex)[:26]
    cksm_hb = 0
    cksm_lb = 0
    for i in range(0, len(packet_hex), 2):
        cksm_hb ^= ord(packet_hex[i])
    for j in range(1, len(packet_hex), 2):
        cksm_lb ^= ord(packet_hex[j])
    cksm_hb ^= 0x33
    cksm_lb ^= 0x30
    if cksm_lb > 0x39:
        cksm_lb += 0x07
    packet_hex += "30" + f"{cksm_hb:02X}" + f"{cksm_lb:02X}" + "0D"
    while len(packet_hex) < 36:
        packet_hex += "00"
    packet_hex = packet_hex[:36]
    return bytes.fromhex(packet_hex)

class IDECPasswordFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("IDEC FC4A-HPC3 Şifre Bulucu — Developed by mertsis")
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
        conn_type_values = [
            "USB/Serial (deneysel – protokol bilinmiyor)",
            "IDEC Pentra Ethernet (port 2101, sayısal şifre)",
            "Ethernet/IP (sadece port kontrolü, şifre testi yok)",
            "Modbus TCP (sadece port kontrolü, şifre testi yok)",
        ]
        if HAS_PYWINAUTO:
            conn_type_values.insert(0, "WindLDR'da otomatik dene (önerilen)")
        self.connection_type = tk.StringVar(
            value=conn_type_values[0] if conn_type_values else "USB/Serial (deneysel – protokol bilinmiyor)"
        )
        conn_type_combo = ttk.Combobox(
            conn_frame,
            textvariable=self.connection_type,
            values=conn_type_values,
            state="readonly",
            width=24
        )
        conn_type_combo.grid(row=0, column=1, pady=5, padx=10)
        ttk.Button(
            conn_frame,
            text="WindLDR penceresini tara (tanı)",
            command=self.scan_windldr_controls
        ).grid(row=0, column=2, pady=5, padx=5)
        
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
        
        # Arama kapsamı (kaç şifre denenecek)
        ttk.Label(conn_frame, text="Arama kapsamı:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.search_mode = tk.StringVar(value="list_4")
        mode_combo = ttk.Combobox(
            conn_frame,
            textvariable=self.search_mode,
            values=[
                "Yaygın liste (~240 şifre)",
                "Liste + 4 rakam (0-9999) → ~10.240",
                "Liste + 5 rakam (0-99999) → ~100.240",
                "Liste + 6 rakam (0-999999) → ~1.000.240",
                "Sadece 4 rakam (tüm 10.000)",
                "Sadece 5 rakam (tüm 100.000)",
                "Sadece 6 rakam (tüm 1.000.000)",
                "4 karakter harf+rakam (a-z,0-9) → ~1,68M",
            ],
            state="readonly",
            width=42
        )
        mode_combo.grid(row=3, column=1, columnspan=2, pady=5, padx=10, sticky=tk.W)
        self.mode_to_key = {
            "Yaygın liste (~240 şifre)": "list",
            "Liste + 4 rakam (0-9999) → ~10.240": "list_4",
            "Liste + 5 rakam (0-99999) → ~100.240": "list_5",
            "Liste + 6 rakam (0-999999) → ~1.000.240": "list_6",
            "Sadece 4 rakam (tüm 10.000)": "only_4",
            "Sadece 5 rakam (tüm 100.000)": "only_5",
            "Sadece 6 rakam (tüm 1.000.000)": "only_6",
            "4 karakter harf+rakam (a-z,0-9) → ~1,68M": "only_4alpha",
        }
        
        # Hızlı mod (bekleme sürelerini kısaltır; WindLDR yavaş yanıt verirse kapatın)
        self.fast_mode = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            conn_frame,
            text="Hızlı mod (daha kısa bekleme – daha hızlı deneme)",
            variable=self.fast_mode
        ).grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=5, padx=0)
        
        # Kontrol butonları
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.test_conn_button = ttk.Button(
            button_frame,
            text="Bağlantıyı test et",
            command=self.test_connection
        )
        self.test_conn_button.pack(side=tk.LEFT, padx=5)
        
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
        info_label.pack(pady=2)
        usage_label = ttk.Label(
            main_frame,
            text="Önerilen: WindLDR'da otomatik dene — WindLDR'ı açın, bağlantı/şifre penceresini açıp şifre kutusu görünür olsun. COM modu deneyseldir (protokol dokümante değil).",
            font=("Arial", 8),
            foreground="gray",
            wraplength=720
        )
        usage_label.pack(pady=2)
        idec_note = ttk.Label(
            main_frame,
            text=IDEC_PASSWORD_NOTE,
            font=("Arial", 8),
            foreground="gray",
            wraplength=720
        )
        idec_note.pack(pady=1)
        dev_label = ttk.Label(
            main_frame,
            text="Developed by mertsis",
            font=("Arial", 9, "bold"),
            foreground="#3498db"
        )
        dev_label.pack(pady=4)
        
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
    
    def check_connection_serial(self, com_port, baud_rate):
        """
        COM portun açılıp açılmadığını ve cihazdan yanıt gelip gelmediğini kontrol eder.
        Returns: ("ok", mesaj) | ("port_error", mesaj) | ("no_response", mesaj)
        """
        try:
            ser = serial.Serial(
                port=com_port,
                baudrate=int(baud_rate),
                timeout=1.5,
                write_timeout=1
            )
        except serial.SerialException as e:
            return ("port_error", str(e))
        except Exception as e:
            return ("port_error", str(e))
        
        try:
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            # Kısa bir probe gönder (bazı cihazlar yanıt verir veya NAK döner)
            probe = b"\x00\x01\x00"  # minimal; IDEC protokolü değil, sadece "bir şey var mı?" için
            ser.write(probe)
            time.sleep(0.3)
            response = ser.read(50)
            ser.close()
            if response and len(response) > 0:
                return ("ok", "Port açıldı ve cihazdan yanıt alındı (bağlantı var).")
            return ("no_response", "Port açıldı ama cihazdan hiç yanıt gelmedi. PLC açık mı? Kablo/baud doğru mu?")
        except Exception as e:
            try:
                ser.close()
            except Exception:
                pass
            return ("port_error", str(e))
    
    def test_connection(self):
        """Bağlantıyı test et butonu"""
        conn_key = _conn_type_key(self.connection_type.get())
        conn_addr = self.connection_address.get().strip()
        if not conn_addr:
            messagebox.showwarning("Uyarı", "Önce COM Port veya IP girin.")
            return
        if conn_key == "pentra":
            self.log_message("Bağlantı test ediliyor (Pentra TCP 2101)...")
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((conn_addr, PENTRA_DEFAULT_PORT))
                sock.close()
                self.log_message(f"Pentra {conn_addr}:{PENTRA_DEFAULT_PORT} bağlantısı OK.")
                messagebox.showinfo("Bağlantı tamam", f"Pentra {conn_addr}:{PENTRA_DEFAULT_PORT} bağlantısı kuruldu.")
                return
            except Exception as e:
                self.log_message(str(e))
                messagebox.showerror("Bağlantı hatası", f"Pentra {conn_addr}:{PENTRA_DEFAULT_PORT} bağlanılamadı.\n{e}")
                return
        elif conn_key != "serial":
            messagebox.showinfo("Bilgi", "Bağlantı testi şu an USB/Serial ve IDEC Pentra için destekleniyor.")
            return
        self.log_message("Bağlantı test ediliyor (COM)...")
        self.root.update()
        status, msg = self.check_connection_serial(conn_addr, self.baud_rate.get())
        self.log_message(msg)
        if status == "ok":
            messagebox.showinfo("Bağlantı tamam", msg)
        elif status == "port_error":
            messagebox.showerror(
                "Port açılamadı",
                msg + "\n\nWindLDR veya başka program bu portu kullanıyor olabilir. Kapatıp tekrar deneyin."
            )
        else:
            messagebox.showwarning(
                "Cihazdan yanıt yok",
                msg + "\n\nNot: PLC sadece WindLDR protokolüne yanıt veriyor olabilir; bu yüzden yanıt gelmemesi normal olabilir. Port açılabildiyse kablo/PLC bağlı demektir."
            )
    
    def _serial_send_and_check(self, ser, password):
        """Açık serial port üzerinden şifre gönderir, yanıtı kontrol eder. Hızlı timeout kullanır."""
        fast = self.fast_mode.get()
        ser.reset_input_buffer()
        test_command = f"PASSWORD:{password}\r\n"
        ser.write(test_command.encode())
        time.sleep(0.15 if fast else 0.35)
        response = ser.read(100).decode('utf-8', errors='ignore')
        return "OK" in response or "CONNECTED" in response

    def test_password_serial(self, password, com_port, baud_rate, ser=None):
        """Serial port üzerinden şifre test eder. ser verilirse aynı port kullanılır (hızlı)."""
        if ser is not None:
            try:
                return self._serial_send_and_check(ser, password)
            except Exception as e:
                self.log_message(f"Hata: {str(e)}")
                return False
        try:
            fast = self.fast_mode.get()
            timeout = 0.6 if fast else 1.2
            ser = serial.Serial(
                port=com_port,
                baudrate=int(baud_rate),
                timeout=timeout,
                write_timeout=1
            )
            time.sleep(0.1 if fast else 0.25)
            result = self._serial_send_and_check(ser, password)
            ser.close()
            return result
        except Exception as e:
            self.log_message(f"Hata: {str(e)}")
            return False
    
    def test_password_pentra(self, password, ip_address, port=PENTRA_DEFAULT_PORT):
        """
        IDEC Pentra Ethernet (port 2101): Capkj2/Idec-password-cracker protokolü.
        Şifre sadece sayısal olmalı (örn. 1234); metin şifreler False döner.
        """
        try:
            num = int(password) if password and str(password).strip().isdigit() else None
            if num is None or num < 0 or num > 99999999:
                return False
            packet = _pentra_build_packet(num)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2.5)
            sock.connect((ip_address, port))
            sock.sendall(packet)
            buf = sock.recv(64)
            sock.close()
            if len(buf) >= len(VALID_PASS_RESPONSE) and buf[:len(VALID_PASS_RESPONSE)] == VALID_PASS_RESPONSE:
                return True
            return False
        except (ValueError, OSError, socket.error) as e:
            self.log_message(f"Pentra hatası: {e}")
            return False

    def test_password_ethernet(self, password, ip_address):
        """Ethernet üzerinden şifre test eder (Modbus TCP port 502 - sadece port kontrolü)."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((ip_address, 502))
            sock.close()
            if result == 0:
                return True
            return False
        except Exception as e:
            self.log_message(f"Hata: {str(e)}")
            return False
    
    def _find_windldr_window(self):
        """WindLDR veya IDEC penceresini bulur. Başarılıysa (app, window) yoksa (None, hata mesajı)."""
        if not HAS_PYWINAUTO:
            return None, "pywinauto yüklü değil. pip install pywinauto"
        try:
            app = PywinautoApp(backend="uia").connect(title_re=".*WindLDR.*|.*IDEC.*|.*LDR.*", timeout=3)
            wins = app.windows()
            if not wins:
                return None, "WindLDR penceresi bulunamadı. WindLDR'ı açıp bağlantı/şifre ekranını açın."
            return app, wins[0]
        except Exception as e:
            return None, f"WindLDR bulunamadı: {e}. WindLDR açık mı? Bağlantı penceresi açık mı?"

    def _dump_control_tree(self, elem, depth=0, max_depth=8, lines=None):
        """Pencere/kontrol ağacını metin olarak döndürür (tanı için). max_depth ile derinlik sınırı."""
        if lines is None:
            lines = []
        if depth > max_depth:
            return lines
        try:
            indent = "  " * depth
            ctype = getattr(elem.element_info, "control_type", "?")
            name = (elem.window_text() or "")[:60]
            auto_id = getattr(elem.element_info, "automation_id", "") or ""
            class_name = getattr(elem.element_info, "class_name", "") or ""
            line = f"{indent}{ctype}"
            if name:
                line += f" text=\"{name}\""
            if auto_id:
                line += f" automation_id=\"{auto_id}\""
            if class_name and class_name != ctype:
                line += f" class=\"{class_name}\""
            lines.append(line)
        except Exception:
            lines.append("  " * depth + "(okunamadı)")
        try:
            for child in elem.children():
                self._dump_control_tree(child, depth + 1, max_depth, lines)
        except Exception:
            pass
        return lines

    def scan_windldr_controls(self):
        """WindLDR penceresini bulup tüm kontrolleri log'a yazar (tanı / sürüm uyumu için)."""
        if not HAS_PYWINAUTO:
            messagebox.showwarning("Uyarı", "pywinauto yüklü değil. pip install pywinauto")
            return
        self.log_message("WindLDR taraması başlıyor...")
        self.root.update()
        app_or_none, win_or_msg = self._find_windldr_window()
        if app_or_none is None:
            self.log_message(f"Hata: {win_or_msg}")
            messagebox.showerror("WindLDR bulunamadı", win_or_msg)
            return
        app, win = app_or_none, win_or_msg
        try:
            title = win.window_text()
            self.log_message(f"Pencere başlığı: {title}")
            self.log_message("-" * 50)
            lines = self._dump_control_tree(win, max_depth=6)
            for line in lines[:300]:  # ilk 300 satır
                self.log_message(line)
            if len(lines) > 300:
                self.log_message(f"... ve {len(lines) - 300} satır daha (kısaltıldı).")
            self.log_message("-" * 50)
            edit, btn = self._get_windldr_password_and_button(win)
            if edit:
                try:
                    self.log_message("Bulunan şifre alanı: " + (edit.window_text() or "") + " " + (getattr(edit.element_info, "automation_id", "") or ""))
                except Exception:
                    self.log_message("Bulunan şifre alanı: (detay alınamadı)")
            else:
                self.log_message("Şifre alanı (Edit) bulunamadı.")
            if btn:
                try:
                    self.log_message("Bulunan Bağlan butonu: " + (btn.window_text() or ""))
                except Exception:
                    self.log_message("Bulunan Bağlan butonu: (detay alınamadı)")
            else:
                self.log_message("Bağlan/OK butonu bulunamadı.")
            self.log_message("Tarama tamamlandı.")
        except Exception as e:
            self.log_message(f"Tarama hatası: {e}")
            messagebox.showerror("Hata", str(e))
    
    def _get_windldr_password_and_button(self, win):
        """Pencerede şifre Edit ve Bağlan/OK butonunu bulur. (edit, button) veya (None, None)."""
        try:
            edits = []
            buttons = []
            for c in win.descendants():
                try:
                    ct = c.element_info.control_type
                    if ct == "Edit":
                        edits.append(c)
                    elif ct == "Button":
                        buttons.append(c)
                except Exception:
                    pass
            # Şifre alanı: genelde tek Edit veya "Password" içeren; yoksa son Edit
            password_edit = None
            for e in edits:
                try:
                    name = (e.window_text() or "") + (getattr(e.element_info, "automation_id", "") or "")
                    if "pass" in name.lower() or "şifre" in name.lower() or "sifre" in name.lower():
                        password_edit = e
                        break
                except Exception:
                    pass
            if password_edit is None and edits:
                password_edit = edits[-1]
            # Bağlan/OK butonu
            connect_btn = None
            for b in buttons:
                try:
                    t = (b.window_text() or "").strip()
                    if any(x in t for x in ("Connect", "OK", "Bağlan", "Tamam", "OK", "Giriş", "Login")):
                        connect_btn = b
                        break
                except Exception:
                    pass
            if connect_btn is None and buttons:
                connect_btn = buttons[0]
            return password_edit, connect_btn
        except Exception:
            return None, None
    
    def try_password_windldr(self, password, password_edit, connect_btn):
        """WindLDR'da şifreyi dener: alanı doldurur, Bağlan'a tıklar; hata kutusu çıkmazsa başarılı sayar."""
        fast = self.fast_mode.get()
        delay_small = 0.02 if fast else 0.05
        delay_after_click = 0.85 if fast else 1.25
        try:
            password_edit.set_focus()
            time.sleep(delay_small)
            password_edit.set_edit_text(password)  # type_keys yerine anında yazma
            time.sleep(delay_small)
            connect_btn.click_input()
            time.sleep(delay_after_click)
            desktop = PywinautoDesktop(backend="uia")
            # Önce hata penceresi var mı kontrol et (yanlış şifre vb.)
            try:
                for dlg in desktop.windows():
                    try:
                        t = (dlg.window_text() or "").strip()
                        if not t:
                            continue
                        t_lower = t.lower()
                        if any(x in t_lower for x in ("error", "wrong", "failed", "invalid", "yanlış", "hatalı", "password", "şifre", "uyarı", "warning", "incorrect")):
                            for child in dlg.descendants():
                                try:
                                    if child.element_info.control_type == "Button":
                                        txt = (child.window_text() or "").strip()
                                        if any(x in txt for x in ("OK", "Tamam", "Yes", "Evet")):
                                            child.click_input()
                                            time.sleep(0.15 if fast else 0.25)
                                            return False
                                except Exception:
                                    pass
                            try:
                                dlg.close()
                            except Exception:
                                pass
                            return False
                    except Exception:
                        pass
            except Exception:
                pass
            # Pozitif başarı: herhangi bir pencerede "Connected" / "Bağlı" / "Online" var mı?
            try:
                for w in desktop.windows():
                    try:
                        title = (w.window_text() or "").strip()
                        if not title:
                            continue
                        title_lower = title.lower()
                        if any(x in title_lower for x in ("connected", "bağlı", "online", "connected to", "bağlandı")):
                            return True
                    except Exception:
                        pass
            except Exception:
                pass
            # Hata kutusu yok ve "Connected" görünmüyorsa da bağlantı başarılı sayılabilir (dialog kapandıysa)
            return True
        except Exception as e:
            self.log_message(f"WindLDR deneme hatası: {e}")
            return False
    
    def search_passwords(self):
        """Şifre arama işlemini başlatır"""
        self.is_running = True
        self.found_password = None
        
        conn_type = self.connection_type.get()
        conn_addr = self.connection_address.get()
        
        mode_key = self.mode_to_key.get(self.search_mode.get(), "list_4")
        total_passwords = get_total_count(mode_key)
        
        conn_key = _conn_type_key(conn_type)
        self.log_message("="*60)
        self.log_message("Şifre araması başlatılıyor...")
        self.log_message(f"Bağlantı Tipi: {conn_type}")
        self.log_message(f"Toplam denenecek şifre: {total_passwords:,}")
        if conn_key == "windldr":
            self.log_message("WindLDR penceresinde şifreler otomatik denenecek (şifre alanı + Bağlan butonu).")
        elif conn_key == "serial":
            self.log_message("Not: COM modu deneyseldir; IDEC protokolü bilinmiyor, PLC yanıt vermeyebilir.")
        elif conn_key == "pentra":
            self.log_message("IDEC Pentra Ethernet (port 2101) — sadece sayısal şifreler denenecek (kaynak: Capkj2/Idec-password-cracker).")
        self.log_message("="*60)
        
        password_edit_wldr = None
        connect_btn_wldr = None
        if conn_key == "windldr":
            app_or_none, win_or_msg = self._find_windldr_window()
            if app_or_none is None:
                self.log_message(f"Hata: {win_or_msg}")
                messagebox.showerror("WindLDR bulunamadı", win_or_msg)
                self.is_running = False
                self.start_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.DISABLED)
                return
            _, win = app_or_none, win_or_msg
            password_edit_wldr, connect_btn_wldr = self._get_windldr_password_and_button(win)
            if password_edit_wldr is None or connect_btn_wldr is None:
                self.log_message("WindLDR penceresinde şifre alanı veya Bağlan butonu bulunamadı.")
                messagebox.showerror("Kontrol bulunamadı", "Bağlantı penceresinde şifre kutusu veya Bağlan/OK butonu bulunamadı. WindLDR sürümü farklı olabilir.")
                self.is_running = False
                self.start_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.DISABLED)
                return
            win.set_focus()
        
        ser_handle = None  # COM port tek seferde açılıp tüm denemede kullanılır (hız)
        if conn_key == "serial":
            try:
                fast = self.fast_mode.get()
                ser_handle = serial.Serial(
                    port=conn_addr,
                    baudrate=int(self.baud_rate.get()),
                    timeout=0.6 if fast else 1.2,
                    write_timeout=1
                )
                time.sleep(0.1)
            except Exception as e:
                self.log_message(f"COM port açılamadı: {e}")
                ser_handle = None
        
        try:
            delay_between = 0.03 if self.fast_mode.get() else 0.08
            for index, total, password in password_iterator(mode_key):
                if not self.is_running:
                    self.log_message("\nArama durduruldu!")
                    break
                
                display_password = password if password else "(BOŞ)"
                if index <= 20 or index % 50 == 0 or index == total:
                    self.log_message(f"[{index:,}/{total:,}] Deneniyor: '{display_password}'")
                
                progress = (index / total) * 100
                self.progress_var.set(progress)
                self.status_label.config(text=f"Deneniyor: {display_password} ({index:,}/{total:,})")
                
                success = False
                if conn_key == "serial":
                    if ser_handle:
                        success = self.test_password_serial(password, conn_addr, self.baud_rate.get(), ser=ser_handle)
                    else:
                        success = self.test_password_serial(password, conn_addr, self.baud_rate.get())
                elif conn_key == "pentra":
                    success = self.test_password_pentra(password, conn_addr, PENTRA_DEFAULT_PORT)
                elif conn_key in ("ethernet", "modbus"):
                    success = self.test_password_ethernet(password, conn_addr)
                elif conn_key == "windldr" and password_edit_wldr and connect_btn_wldr:
                    try:
                        success = self.try_password_windldr(password, password_edit_wldr, connect_btn_wldr)
                    except Exception as e:
                        self.log_message(f"WindLDR deneme hatası: {e}")
                        # Kontrol referansı geçersiz olmuş olabilir; hemen yeniden tara
                        app_or_none, win_or_msg = self._find_windldr_window()
                        if app_or_none is not None:
                            _, win = app_or_none, win_or_msg
                            pe, cb = self._get_windldr_password_and_button(win)
                            if pe is not None and cb is not None:
                                password_edit_wldr, connect_btn_wldr = pe, cb
                            else:
                                password_edit_wldr, connect_btn_wldr = None, None
                        else:
                            password_edit_wldr, connect_btn_wldr = None, None
                    # Her 40 denemede bir WindLDR referanslarını tazele (pencere/control değişebilir)
                    if conn_key == "windldr" and index % 40 == 0 and index > 0 and (password_edit_wldr or connect_btn_wldr):
                        app_or_none, win_or_msg = self._find_windldr_window()
                        if app_or_none is not None:
                            _, win = app_or_none, win_or_msg
                            pe, cb = self._get_windldr_password_and_button(win)
                            if pe is not None and cb is not None:
                                password_edit_wldr, connect_btn_wldr = pe, cb
                
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
                
                time.sleep(delay_between)
        finally:
            if ser_handle:
                try:
                    ser_handle.close()
                except Exception:
                    pass
        
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
        conn_type = self.connection_type.get()
        conn_key = _conn_type_key(conn_type)
        conn_addr = self.connection_address.get().strip()
        if conn_key != "windldr" and not conn_addr:
            messagebox.showerror("Hata", "Lütfen COM Port veya IP adresi girin!")
            return
        
        if conn_key == "serial":
            status, msg = self.check_connection_serial(conn_addr, self.baud_rate.get())
            if status == "port_error":
                messagebox.showerror(
                    "Bağlantı yok",
                    "COM port açılamadı.\n\n" + msg + "\n\nWindLDR kapalı mı? Port doğru mu?"
                )
                return
            if status == "no_response":
                devam = messagebox.askyesno(
                    "Cihazdan yanıt yok",
                    msg + "\n\n(IDEC sadece WindLDR komutlarına yanıt verdiği için bu normal olabilir.)\nYine de otomatik denemeyi başlatmak istiyor musunuz?"
                )
                if not devam:
                    return
        
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
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

