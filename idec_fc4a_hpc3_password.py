#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IDEC FC4A-HPC3 PLC Şifre Kurtarma Scripti
Özel olarak FC4A-HPC3 modeli için hazırlanmıştır.
"""

import socket
import time
import sys

# FC4A-HPC3 için özel varsayılan şifreler
FC4A_HPC3_PASSWORDS = [
    "",  # Boş şifre (en yaygın)
    "admin",
    "ADMIN",
    "password",
    "PASSWORD",
    "idec",
    "IDEC",
    "fc4a",
    "FC4A",
    "hpc3",
    "HPC3",
    "1234",
    "12345",
    "0000",
    "1111",
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
    "service",
    "SERVICE",
]

def fc4a_hpc3_reset_procedure():
    """FC4A-HPC3 için özel reset prosedürü"""
    print("="*70)
    print("IDEC FC4A-HPC3 ŞİFRE SIFIRLAMA YÖNTEMLERİ")
    print("="*70)
    
    print("""
1. DONANIMSAL RESET (En Etkili - Programı Siler!):
   
   ADIM 1: Cihazı kapatın (güç kaynağını kesin)
   
   ADIM 2: Cihazın üzerinde RESET butonunu bulun
           - Genellikle yan tarafta veya ön panelde
           - Küçük bir delik içinde olabilir (kalem ucu ile basılır)
   
   ADIM 3: RESET butonuna basılı tutun
   
   ADIM 4: Güç kaynağını açın (RESET'e basılı tutmaya devam edin)
   
   ADIM 5: 5-10 saniye basılı tutun
   
   ADIM 6: RESET butonunu bırakın
   
   SONUÇ: Şifre sıfırlanır (program da silinir!)
   
   ⚠️  UYARI: Bu işlem tüm programı siler! Yedek alın!

2. DIP SWITCH RESET (Eğer varsa):
   
   - Cihazın üzerindeki DIP switch'leri kontrol edin
   - RESET veya CLEAR konumuna alın
   - Cihazı yeniden başlatın
   - Şifre sıfırlanır

3. WINDLDR YAZILIMI İLE:
   
   - WindLDR programını açın
   - "Communication Settings" menüsüne gidin
   - "Password" alanını boş bırakın veya varsayılan şifreleri deneyin
   - "Connect" butonuna basın

4. SERİ PORT ÜZERİNDEN:
   
   - RS232/RS485 bağlantısı ile bağlanın
   - Bazı modellerde seri port üzerinden şifre bypass edilebilir
   - WindLDR'da "Direct Connection" seçeneğini deneyin
    """)

def try_windldr_connection():
    """WindLDR bağlantı ayarları"""
    print("\n" + "="*70)
    print("WINDLDR BAĞLANTI AYARLARI")
    print("="*70)
    
    print("""
WindLDR'da FC4A-HPC3'e bağlanmak için:

1. WindLDR'ı açın
2. File → New Project → FC4A serisi seçin
3. Communication → Settings
4. Connection Type: USB veya Serial seçin
5. Password alanını BOŞ bırakın veya aşağıdakileri deneyin:
   - (boş)
   - admin
   - password
   - idec
6. "Connect" butonuna basın

Eğer bağlanamazsanız:
- Cihazı resetleyin (yukarıdaki prosedür)
- USB/Serial driver'ların yüklü olduğundan emin olun
- COM port numarasını kontrol edin
    """)

def fc4a_hpc3_default_settings():
    """FC4A-HPC3 varsayılan ayarlar"""
    print("\n" + "="*70)
    print("FC4A-HPC3 VARSayılan AYARLAR")
    print("="*70)
    
    print("""
Varsayılan Bağlantı Ayarları:
- Baud Rate: 9600 (Serial) veya USB
- Data Bits: 8
- Stop Bits: 1
- Parity: None
- Flow Control: None

Varsayılan Şifre:
- Çoğu durumda BOŞ (hiçbir şey yazmadan)
- İlk kurulumda genellikle şifre yoktur
    """)

def brute_force_fc4a_hpc3(ip_address=None, port=502):
    """FC4A-HPC3 için şifre denemesi"""
    print("\n" + "="*70)
    print("ŞİFRE DENEME LİSTESİ (FC4A-HPC3)")
    print("="*70)
    
    print("\nBu şifreleri sırayla deneyin:\n")
    for i, password in enumerate(FC4A_HPC3_PASSWORDS, 1):
        display = f"'{password}'" if password else "'(BOŞ - hiçbir şey yazmadan Enter)'"
        print(f"{i:2d}. {display}")
    
    print("\n" + "-"*70)
    print("ÖNEMLİ: En yaygın çözüm BOŞ şifredir!")
    print("WindLDR'da password alanını boş bırakıp Enter'a basın.")
    print("-"*70)

def main():
    print("\n" + "="*70)
    print("IDEC FC4A-HPC3 PLC ŞİFRE KURTARMA")
    print("="*70)
    
    print("\nModel: FC4A-HPC3")
    print("Üretici: IDEC Corporation")
    print("\n⚠️  UYARI: Bu araç sadece kendi cihazınız için kullanılmalıdır!")
    
    # Reset prosedürü
    fc4a_hpc3_reset_procedure()
    
    # Varsayılan ayarlar
    fc4a_hpc3_default_settings()
    
    # Şifre listesi
    brute_force_fc4a_hpc3()
    
    # WindLDR bağlantı
    try_windldr_connection()
    
    print("\n" + "="*70)
    print("HIZLI ÇÖZÜM ÖNERİSİ")
    print("="*70)
    print("""
1. İLK DENEME: WindLDR'da password alanını BOŞ bırakın
2. İKİNCİ DENEME: "admin" yazın
3. ÜÇÜNCÜ DENEME: "password" yazın
4. HİÇBİRİ ÇALIŞMAZSA: Donanımsal reset yapın (yukarıdaki prosedür)

Eğer hala çözemezseniz:
- IDEC Teknik Destek: support@idec.com
- Model: FC4A-HPC3
- Seri numarasını belirtin
    """)
    
    print("\n" + "="*70)
    print("BAŞARILAR!")
    print("="*70)

if __name__ == "__main__":
    main()

