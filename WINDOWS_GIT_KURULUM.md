# Windows'ta Git Kurulumu ve Kullanımı

## 🚀 Hızlı Çözüm: Git Olmadan İndirme

### Yöntem 1: GitHub'dan ZIP İndir (En Kolay) ⭐

1. **GitHub'a gidin:**
   - https://github.com/mertoksuzogluu/idec-pass

2. **Yeşil "Code" butonuna tıklayın**
   - Açılan menüden **"Download ZIP"** seçin

3. **ZIP dosyasını açın**
   - İndirilen `idec-pass-main.zip` dosyasını sağ tıklayın
   - "Extract All" (Tümünü Çıkar) seçin
   - Bir klasöre çıkarın (örn: `C:\IDEC_PLC\`)

4. **Dosyalar hazır!**
   - Artık Git gerekmez
   - `EXE_OLUSTUR_WINDOWS.bat` dosyasına çift tıklayın

---

## 📥 Git Kurulumu (İsteğe Bağlı)

Eğer Git kullanmak isterseniz:

### Adım 1: Git İndirin

1. **Git İndirme Sayfası:**
   - https://git-scm.com/download/win

2. **İndirilen `Git-xxx.exe` dosyasına çift tıklayın**

3. **Kurulum:**
   - "Next" butonlarına tıklayın
   - Varsayılan ayarları kullanın
   - "Install" butonuna tıklayın

4. **Kurulum tamamlandı!**

### Adım 2: Git'i Kullanın

**Command Prompt veya PowerShell'de:**

```batch
# Dosyaları indir
git clone https://github.com/mertoksuzogluu/idec-pass.git

# Klasöre gir
cd idec-pass

# .exe oluştur
EXE_OLUSTUR_WINDOWS.bat
```

---

## 🔧 Git Kurulumunu Kontrol Etme

**Command Prompt'u açın ve şunu yazın:**

```batch
git --version
```

Eğer versiyon numarası görünüyorsa → Git kurulu ✅
Eğer "git is not recognized" hatası alıyorsanız → Git kurulu değil ❌

---

## 💡 Git Olmadan Kullanım (Önerilen)

**Git kurmanıza gerek yok!**

1. **GitHub'dan ZIP indirin:**
   - https://github.com/mertoksuzogluu/idec-pass
   - "Code" → "Download ZIP"

2. **ZIP'i açın**

3. **`EXE_OLUSTUR_WINDOWS.bat` dosyasına çift tıklayın**

4. **Hazır!**

---

## 📋 Alternatif: Manuel Dosya İndirme

Eğer ZIP de indiremiyorsanız, her dosyayı tek tek indirebilirsiniz:

1. https://github.com/mertoksuzogluu/idec-pass adresine gidin

2. Her dosyaya tıklayın:
   - `idec_plc_password_auto.py` → "Raw" butonuna tıklayın → Sağ tık → "Save As"
   - `EXE_OLUSTUR_WINDOWS.bat` → "Raw" → "Save As"
   - Diğer dosyalar için aynı işlem

3. Tüm dosyaları aynı klasöre kaydedin

---

## ⚠️ Sorun Giderme

### "git is not recognized" hatası:
- Git kurulu değil
- Git olmadan ZIP indirme yöntemini kullanın

### "Python bulunamadı" hatası:
- Python kurulu değil
- Python kurun: https://www.python.org/downloads/
- Veya hazır .exe dosyası kullanın

### ZIP açılmıyor:
- Windows'un kendi ZIP açıcısını kullanın
- Veya WinRAR/7-Zip kullanın

---

## ✅ Özet

**En Kolay Yöntem:**
1. GitHub'dan ZIP indir
2. ZIP'i aç
3. `EXE_OLUSTUR_WINDOWS.bat` çalıştır
4. Hazır!

**Git gerekmez!** 🎉

