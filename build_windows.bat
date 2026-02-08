@echo off
echo ========================================
echo IDEC PLC Password Finder - Windows Build
echo ========================================
echo.

echo [1/3] Gerekli paketler yukleniyor...
pip install -r requirements.txt

echo.
echo [2/3] Windows .exe dosyasi olusturuluyor...
pyinstaller --onefile --windowed --name "IDEC_PLC_Password_Finder" --icon=NONE idec_plc_password_auto.py

echo.
echo [3/3] Dosya hazir!
echo.
echo .exe dosyasi: dist\IDEC_PLC_Password_Finder.exe
echo.
pause

