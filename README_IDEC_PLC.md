# IDEC FC4A-HPC3 Otomatik Şifre Bulucu

Windows için IDEC FC4A-HPC3 PLC şifre kurtarma aracı.

## Özellikler

- ✅ Otomatik şifre deneme (29 farklı şifre)
- ✅ WindLDR otomasyonu (önerilen), USB/Serial (deneysel), **IDEC Pentra Ethernet (port 2101)**
- ✅ Modern Windows GUI arayüzü
- ✅ İlerleme çubuğu ve log ekranı
- ✅ COM port otomatik tespiti
- ✅ Tek tıkla çalıştırma

## Kurulum

### Yöntem 1: Hazır .exe Dosyası (Önerilen)

1. `IDEC_PLC_Password_Finder.exe` dosyasını indirin
2. Çift tıklayarak çalıştırın
3. Kurulum gerekmez!

### Yöntem 2: Python'dan Çalıştırma

1. Python 3.8+ yüklü olmalı
2. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
3. Programı çalıştırın:
   ```bash
   python idec_plc_password_auto.py
   ```

### Yöntem 3: Kendi .exe Dosyanızı Oluşturun (her PC'de çalışır)

Python yüklü bir Windows PC'de projeyi açın, **EXE_OLUSTUR_WINDOWS.bat** dosyasına çift tıklayın. Oluşan `dist\IDEC_PLC_Password_Finder.exe` dosyasını istediğiniz bilgisayara kopyalayabilirsiniz; o PC'de Python gerekmez.

Ayrıntılı adımlar: **[EXE_OLUSTURMA.md](EXE_OLUSTURMA.md)**

## Kullanım Senaryosu (COM Port ile)

Şifresini unuttuğunuz PLC’yi COM port ile bilgisayara bağlıyorsunuz; yazılımda (WindLDR) PLC’ye bağlanırken şifre isteniyor. Adım adım rehber için: **[KULLANIM_SENARYOSU.md](KULLANIM_SENARYOSU.md)** dosyasına bakın.

## Kullanım

1. **Programı açın**

2. **Bağlantı ayarlarını yapın:**
   - Bağlantı Tipi: WindLDR (önerilen), USB/Serial, **IDEC Pentra Ethernet (port 2101)** veya Ethernet/IP
   - **IDEC Pentra (FC5A):** Sadece **MicroSmart Pentra (FC5A)** için. PLC’nin IP adresini girin; şifreler **sadece sayısal** denir (kaynak: [Capkj2/Idec-password-cracker](https://github.com/Capkj2/Idec-password-cracker)). **FC4A ile Pentra aynı değildir** — FC4A için WindLDR veya COM kullanın.
   - COM Port / IP: COM port numarası veya IP adresi girin
   - "COM Portları Listele" butonu ile mevcut portları görebilirsiniz
   - Baud Rate: Serial için 9600 (varsayılan)

3. **"Şifre Aramayı Başlat" butonuna tıklayın**

4. **Program otomatik olarak tüm şifreleri dener:**
   - İlerleme çubuğu ilerlemeyi gösterir
   - Log ekranında denenen şifreler görünür
   - Bulunan şifre otomatik gösterilir

5. **Bulunan şifreyi WindLDR'da kullanın**

## Denenen Şifreler

Program şu şifreleri sırayla dener:
- (Boş şifre)
- admin, password, idec
- fc4a, hpc3
- 1234, 12345, 0000
- Ve daha fazlası...

## Sorun Giderme

### COM Port Bulunamıyor
- "COM Portları Listele" butonuna tıklayın
- Cihaz Yöneticisi'nde COM port numarasını kontrol edin
- USB kablosunun bağlı olduğundan emin olun

### Bağlantı Kurulamıyor
- WindLDR driver'larının yüklü olduğundan emin olun
- COM port numarasının doğru olduğunu kontrol edin
- Baud rate ayarını kontrol edin (genellikle 9600)

### Hiçbir Şifre Çalışmıyor
- Donanımsal reset yapın:
  1. Cihazı kapatın
  2. RESET butonuna basılı tutun
  3. Güç kaynağını açın
  4. 5-10 saniye basılı tutun
  5. RESET'i bırakın

⚠️ **UYARI:** Reset işlemi programı siler! Yedek alın!

## Teknik Detaylar

- **Dil:** Python 3.8+
- **GUI:** Tkinter
- **Serial:** pyserial
- **Platform:** Windows 10/11

## Yasal Uyarı

Bu araç sadece:
- ✅ Kendi cihazınız için kullanılmalıdır
- ✅ Yetkili erişim için kullanılmalıdır
- ❌ Yetkisiz erişim için kullanılamaz

## Destek

Sorunlar için:
- IDEC Teknik Destek: support@idec.com
- Model: FC4A-HPC3

## Referanslar / Credits

- **IDEC Pentra Ethernet (port 2101)** protokolü: [Capkj2/Idec-password-cracker](https://github.com/Capkj2/Idec-password-cracker) (C++, K Johnson, 2016) — açık kaynak referansı.
- Geliştirici: **mertsis**

## Lisans

Bu araç eğitim ve kendi cihazınız için kullanım amaçlıdır.

