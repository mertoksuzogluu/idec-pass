# Windows'a Kurulum - Basit Yöntem (Python Gerektirmez)

## ⚡ En Kolay Yöntem: Hazır .exe Dosyası

### Adım 1: .exe Dosyasını İndirin

**Seçenek A: GitHub'dan Hazır .exe (Eğer varsa)**
- https://github.com/mertoksuzogluu/idec-pass/releases
- `IDEC_PLC_Password_Finder.exe` dosyasını indirin

**Seçenek B: Kendi .exe'nizi Oluşturun (Python'lu bir bilgisayarda)**

1. **Windows bilgisayarda** (Python yüklü olan):
   ```batch
   # GitHub'dan dosyaları indirin
   git clone https://github.com/mertoksuzogluu/idec-pass.git
   cd idec-pass
   
   # .exe oluştur
   EXE_OLUSTUR_WINDOWS.bat
   ```

2. Oluşan `dist\IDEC_PLC_Password_Finder.exe` dosyasını alın

### Adım 2: .exe Dosyasını Kullanın

1. **İndirdiğiniz veya oluşturduğunuz `.exe` dosyasına çift tıklayın**
2. **Kurulum gerekmez!** Direkt çalışır
3. Program açılır, kullanmaya başlayın

---

## 🔧 .exe Oluşturma (Python'lu Bilgisayarda)

Eğer bir Windows bilgisayarda Python varsa:

### Hızlı Yöntem:

1. **Dosyaları İndirin:**
   - GitHub'dan tüm dosyaları indirin
   - Veya `git clone https://github.com/mertoksuzogluu/idec-pass.git`

2. **`EXE_OLUSTUR_WINDOWS.bat` dosyasına çift tıklayın**
   - Otomatik olarak .exe oluşturur
   - `dist\` klasöründe hazır olur

### Manuel Yöntem:

```batch
# Terminal'de (Command Prompt veya PowerShell)
cd idec-pass
pip install pyinstaller pyserial
pyinstaller --onefile --windowed --name "IDEC_PLC_Password_Finder" idec_plc_password_auto.py
```

Oluşan dosya: `dist\IDEC_PLC_Password_Finder.exe`

---

## 📦 .exe Dosyasını Paylaşma

Oluşturduğunuz `.exe` dosyasını:
- USB'ye kopyalayın
- Email ile gönderin
- Cloud'a yükleyin (Google Drive, Dropbox, vb.)
- Başka bilgisayarlara kopyalayın

**Önemli:** `.exe` dosyası tek başına çalışır, Python gerekmez!

---

## ⚠️ Antivirus Uyarısı

İlk kez çalıştırdığınızda Windows Defender veya antivirus uyarı verebilir:
- **"Windows protected your PC"** mesajı çıkabilir
- **"More info"** → **"Run anyway"** tıklayın
- Bu normaldir, çünkü .exe yeni oluşturulmuş

---

## 🚀 Kullanım

1. `.exe` dosyasına çift tıklayın
2. Program açılır
3. COM Port veya IP adresini girin
4. "Şifre Aramayı Başlat" butonuna tıklayın
5. Program otomatik şifreleri dener

---

## 💡 İpuçları

- `.exe` dosyasını bir klasöre koyun (örn: `C:\IDEC_PLC\`)
- Masaüstüne kısayol oluşturun
- Programı "Yönetici olarak çalıştır" gerekebilir

---

## ❓ Sorun mu var?

**"Dosya çalışmıyor" hatası:**
- Windows 10/11 kullandığınızdan emin olun
- Antivirus'ü geçici olarak kapatıp deneyin
- Yönetici olarak çalıştırın

**"COM Port bulunamadı":**
- USB kablosunun bağlı olduğundan emin olun
- Cihaz Yöneticisi'nde COM port numarasını kontrol edin

---

## 📞 Yardım

- GitHub: https://github.com/mertoksuzogluu/idec-pass
- IDEC Destek: support@idec.com

