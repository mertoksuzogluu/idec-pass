@echo off
echo ========================================
echo IDEC PLC Password Finder - EXE Olusturucu
echo ========================================
echo.
echo Bu script Windows'ta .exe dosyasi olusturacak
echo.
echo Gereksinimler:
echo - Python 3.8+ yuklu olmali
echo - Internet baglantisi olmali
echo.
pause

echo.
echo [1/4] Python kontrol ediliyor...
python --version
if errorlevel 1 (
    echo HATA: Python bulunamadi!
    echo Lutfen Python yukleyin: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo [2/4] Gerekli paketler yukleniyor...
pip install -r requirements.txt
pip install pyinstaller

echo.
echo [3/4] .exe dosyasi olusturuluyor (tek dosya, WindLDR + Pentra dahil)...
pyinstaller --noconfirm IDEC_PLC_Password_Finder.spec

echo.
echo [4/4] Tamamlandi!
echo.
echo .exe dosyasi: dist\IDEC_PLC_Password_Finder.exe
echo.
echo Bu dosyayi istediginiz yere kopyalayabilirsiniz.
echo Python yuklu olmayan bilgisayarlarda da calisir!
echo.
pause

