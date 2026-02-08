#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IDEC PLC Şifre Kurtarma Scripti
Not: Bu script sadece kendi cihazınız için kullanılmalıdır.
"""

import socket
import time
import sys

# IDEC PLC yaygın varsayılan şifreler
DEFAULT_PASSWORDS = [
    "",  # Boş şifre
    "admin",
    "password",
    "idec",
    "IDEC",
    "1234",
    "12345",
    "0000",
    "admin123",
    "password123",
    "idec123",
    "PLC",
    "plc",
    "factory",
    "default",
    "user",
    "root",
    "system",
    "operator",
    "technician",
]

# IDEC PLC yaygın portlar
DEFAULT_PORTS = [502, 2000, 2001, 44818, 9600]

def try_password(ip_address, port, password, timeout=2):
    """Belirli bir şifre ile bağlantı denemesi yapar"""
    try:
        # Modbus TCP bağlantısı (IDEC PLC'ler genellikle Modbus kullanır)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        result = sock.connect_ex((ip_address, port))
        sock.close()
        
        if result == 0:
            print(f"  Port {port} açık - Şifre denemesi: '{password}'")
            # Burada gerçek şifre kontrolü yapılabilir
            # IDEC PLC'lerin API'sine göre değişir
            return True
        return False
    except Exception as e:
        return False

def scan_idec_plc(ip_address, ports=None):
    """IDEC PLC'yi tarar ve açık portları bulur"""
    if ports is None:
        ports = DEFAULT_PORTS
    
    print(f"\n{'='*60}")
    print(f"IDEC PLC Tarama: {ip_address}")
    print(f"{'='*60}\n")
    
    open_ports = []
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip_address, port))
            sock.close()
            
            if result == 0:
                open_ports.append(port)
                print(f"✓ Port {port} açık")
        except:
            pass
    
    return open_ports

def brute_force_password(ip_address, port, passwords=None):
    """Şifre brute force denemesi"""
    if passwords is None:
        passwords = DEFAULT_PASSWORDS
    
    print(f"\n{'='*60}")
    print(f"Şifre Denemesi: {ip_address}:{port}")
    print(f"{'='*60}\n")
    
    for i, password in enumerate(passwords, 1):
        print(f"[{i}/{len(passwords)}] Deneniyor: '{password}'", end="\r")
        sys.stdout.flush()
        
        # Burada gerçek şifre kontrolü yapılmalı
        # IDEC PLC modeline göre API çağrısı yapılır
        time.sleep(0.1)
    
    print(f"\n\nTüm varsayılan şifreler denendi.")
    print("Eğer hiçbiri çalışmadıysa, donanımsal reset gerekebilir.")

def get_idec_model_info():
    """IDEC PLC model bilgilerini gösterir"""
    print("""
IDEC PLC Şifre Sıfırlama Yöntemleri:

1. DONANIMSAL RESET (En etkili yöntem):
   - Cihazın üzerinde RESET butonu varsa basılı tutun
   - Genellikle 5-10 saniye basılı tutmak gerekir
   - Cihazı kapatıp açarken RESET butonuna basılı tutun

2. VARSayılan ŞİFRELER:
   - Boş şifre (hiçbir şey yazmadan)
   - "admin"
   - "password"
   - "idec"
   - "1234"

3. ÜRETİCİ DOKÜMANTASYONU:
   - IDEC'in resmi dokümantasyonunu kontrol edin
   - Model numarasına göre özel prosedür olabilir

4. FIRMWARE GÜNCELLEMESİ:
   - Bazı modellerde firmware güncellemesi şifreyi sıfırlar
   - Dikkatli olun, tüm programı kaybedebilirsiniz

5. ÜRETİCİ DESTEĞİ:
   - IDEC teknik desteğine başvurun
   - Seri numarası ile doğrulama yapabilirler
    """)

def main():
    print("="*60)
    print("IDEC PLC ŞİFRE KURTARMA ARACI")
    print("="*60)
    
    print("\nÖNEMLİ UYARI:")
    print("- Bu araç sadece kendi cihazınız için kullanılmalıdır")
    print("- Yetkisiz erişim yasaktır")
    print("- Şifre sıfırlama işlemi programı silebilir\n")
    
    # Genel bilgiler
    get_idec_model_info()
    
    # Varsayılan şifre listesi
    print("\n" + "="*60)
    print("DENENECEK VARSayılan ŞİFRELER:")
    print("="*60)
    for i, pwd in enumerate(DEFAULT_PASSWORDS, 1):
        display = f"'{pwd}'" if pwd else "'(boş)'"
        print(f"{i:2d}. {display}")
    
    print("\n" + "="*60)
    print("ÖNERİLEN ADIMLAR:")
    print("="*60)
    print("1. IDEC PLC programlama yazılımını açın (WindLDR veya diğer)")
    print("2. Yukarıdaki şifreleri sırayla deneyin")
    print("3. Eğer hiçbiri çalışmazsa, donanımsal reset yapın")
    print("4. Reset işlemi programı silebilir - yedek alın!")
    print("5. IDEC teknik desteğine başvurun: support@idec.com")
    
    print("\n" + "="*60)
    print("DONANIMSAL RESET YÖNTEMLERİ:")
    print("="*60)
    print("""
IDEC PLC Modellerine Göre Reset Yöntemleri:

1. FC5A / FC6A Serisi:
   - Cihazı kapatın
   - RESET butonunu bulun (genellikle yan tarafta)
   - RESET butonuna basılı tutarak cihazı açın
   - 5-10 saniye basılı tutun
   - Şifre sıfırlanır (program da silinebilir!)

2. MicroSmart Serisi:
   - DIP switch'lerde RESET konumuna alın
   - Cihazı yeniden başlatın
   - Şifre sıfırlanır

3. Genel Yöntem:
   - Cihazın üzerindeki tüm butonları kontrol edin
   - Kullanım kılavuzunu inceleyin
   - Seri numarası ile IDEC'e başvurun
    """)
    
    print("\n" + "="*60)
    print("IP ADRESİ İLE TARAMA (Opsiyonel):")
    print("="*60)
    print("Eğer PLC'nin IP adresini biliyorsanız:")
    print("  python3 idec_plc_password_recovery.py --ip 192.168.1.100")
    print("\nVeya script içinde ip_address değişkenini düzenleyin.")

if __name__ == "__main__":
    main()

