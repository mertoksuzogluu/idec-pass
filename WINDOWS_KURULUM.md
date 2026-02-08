# IDEC PLC Password Finder - Windows Kurulum Rehberi

## Yöntem 1: Hazır .exe Dosyası (En Kolay) ⭐

### Adımlar:

1. **GitHub'dan İndirin:**
   - https://github.com/mertoksuzogluu/idec-pass adresine gidin
   - "Releases" bölümünden `IDEC_PLC_Password_Finder.exe` dosyasını indirin
   - Veya repository'den `dist/IDEC_PLC_Password_Finder.exe` dosyasını indirin

2. **Çalıştırın:**
   - İndirdiğiniz `.exe` dosyasına çift tıklayın
   - Kurulum gerekmez, direkt çalışır!

3. **Kullanın:**
   - Program açılır
   - COM Port veya IP adresini girin
   - "Şifre Aramayı Başlat" butonuna tıklayın

---

## Yöntem 2: Python ile Çalıştırma

### Gereksinimler:
- Python 3.8 veya üzeri
- Windows 10/11

### Kurulum Adımları:

1. **Python'u İndirin ve Kurun:**
   - https://www.python.org/downloads/ adresine gidin
   - Python 3.11 veya üzeri sürümü indirin
   - Kurulum sırasında **"Add Python to PATH"** seçeneğini işaretleyin

2. **GitHub'dan Dosyaları İndirin:**
   ```bash
   # GitHub'dan repository'yi indirin veya
   git clone https://github.com/mertoksuzogluu/idec-pass.git
   cd idec-pass
   ```

3. **Gerekli Paketleri Yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Programı Çalıştırın:**
   ```bash
   python idec_plc_password_auto.py
   ```

---

## Yöntem 3: Kendi .exe Dosyanızı Oluşturun

### Adımlar:

1. **Python ve PyInstaller Kurun:**
   ```bash
   pip install pyinstaller
   ```

2. **.exe Dosyası Oluşturun:**
   ```bash
   pyinstaller --onefile --windowed --name "IDEC_PLC_Password_Finder" idec_plc_password_auto.py
   ```

3. **Oluşan Dosya:**
   - `dist/IDEC_PLC_Password_Finder.exe` dosyası hazır
   - Bu dosyayı istediğiniz yere kopyalayabilirsiniz

---

## Yöntem 4: Otomatik Kurulum Scripti (Windows)

Windows'ta `build_windows.bat` dosyasını çalıştırın:

```batch
build_windows.bat
```

Bu script:
- Gerekli paketleri yükler
- .exe dosyası oluşturur
- `dist/` klasörüne kaydeder

---

## Hızlı Başlangıç

### İlk Kullanım:

1. **Programı açın**

2. **Bağlantı ayarlarını yapın:**
   - **Bağlantı Tipi:** USB/Serial veya Ethernet/IP
   - **COM Port / IP:** COM port numarası veya IP adresi
   - **Baud Rate:** 9600 (Serial için)

3. **"COM Portları Listele"** butonuna tıklayarak mevcut portları görebilirsiniz

4. **"Şifre Aramayı Başlat"** butonuna tıklayın

5. **Program otomatik olarak şifreleri dener:**
   - İlerleme çubuğu ilerlemeyi gösterir
   - Log ekranında denenen şifreler görünür
   - Bulunan şifre otomatik gösterilir

---

## Sorun Giderme

### "Python bulunamadı" hatası:
- Python'un PATH'e eklendiğinden emin olun
- Terminal'i yeniden başlatın
- `python --version` komutu ile kontrol edin

### "COM Port bulunamadı":
- Cihaz Yöneticisi'nde COM port numarasını kontrol edin
- USB kablosunun bağlı olduğundan emin olun
- "COM Portları Listele" butonunu kullanın

### "Module not found" hatası:
```bash
pip install pyserial
```

### Antivirus uyarısı:
- .exe dosyası yeni oluşturulduğu için antivirus uyarı verebilir
- Dosyayı "İzin ver" olarak işaretleyin
- Güvenli bir kaynaktan indirdiğinizden emin olun

---

## Sistem Gereksinimleri

- **İşletim Sistemi:** Windows 10/11 (64-bit)
- **RAM:** En az 4 GB
- **Disk Alanı:** 50 MB
- **Python:** 3.8+ (Python ile çalıştırma için)

---

## Önemli Notlar

⚠️ **Güvenlik:**
- Bu program sadece kendi cihazınız için kullanılmalıdır
- Antivirus taraması yapın
- Güvenilir kaynaktan indirin

✅ **Öneriler:**
- Programı bir klasöre koyun (örn: `C:\Program Files\IDEC_PLC_Password_Finder\`)
- Masaüstüne kısayol oluşturun
- Yönetici olarak çalıştırmanız gerekebilir

---

## Destek

Sorunlar için:
- GitHub Issues: https://github.com/mertoksuzogluu/idec-pass/issues
- IDEC Teknik Destek: support@idec.com

