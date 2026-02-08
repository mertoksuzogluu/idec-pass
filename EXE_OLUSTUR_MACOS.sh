#!/bin/bash
# macOS'ta Windows .exe oluşturma scripti
# Not: Bu cross-compilation gerektirir, genellikle çalışmaz
# En iyi yöntem: Windows'ta .exe oluşturmak

echo "=========================================="
echo "Windows .exe Olusturma (macOS)"
echo "=========================================="
echo ""
echo "NOT: macOS'ta Windows .exe olusturmak zordur."
echo "En iyi yontem: Windows bilgisayarda .exe olusturmak"
echo ""

# PyInstaller yükle
echo "[1/3] PyInstaller yukleniyor..."
pip3 install pyinstaller pyserial

# Windows için .exe oluşturmayı dene (genellikle çalışmaz)
echo "[2/3] Windows .exe olusturulmaya calisiliyor..."
echo "UYARI: Bu cross-compilation gerektirir ve genellikle calismaz!"
echo ""

# Normal .exe oluşturma (macOS'ta çalışmaz ama deneyelim)
pyinstaller --onefile --windowed --name "IDEC_PLC_Password_Finder" idec_plc_password_auto.py 2>&1 | head -20

echo ""
echo "[3/3] Tamamlandi (ama muhtemelen calismadi)"
echo ""
echo "=========================================="
echo "ONERILEN YONTEM:"
echo "=========================================="
echo "1. Windows bilgisayarda Python kurun"
echo "2. GitHub'dan dosyalari indirin"
echo "3. EXE_OLUSTUR_WINDOWS.bat calistirin"
echo "4. Olusan .exe dosyasini Python'suz bilgisayara kopyalayin"
echo "=========================================="

