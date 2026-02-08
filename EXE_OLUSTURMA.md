# IDEC PLC Password Finder — EXE Oluşturma

Bu rehber, **herhangi bir Windows PC'de Python yüklü olmadan** çalışacak tek dosyalık `.exe` oluşturmak içindir.

## Gereksinimler (sadece EXE üretmek için)

- **Windows 10/11**
- **Python 3.8 veya üzeri** ([python.org/downloads](https://www.python.org/downloads/))
- Kurulumda **"Add Python to PATH"** işaretli olsun

## Adımlar

### 1. Projeyi indirin

```bash
git clone https://github.com/mertoksuzogluu/idec-pass2.git
cd idec-pass2
```

Veya ZIP olarak indirip klasöre girin.

### 2. EXE oluştur

**Yöntem A — Çift tıklama (önerilen)**  
`EXE_OLUSTUR_WINDOWS.bat` dosyasına çift tıklayın. Script:

- Python ve pip kontrolü yapar
- `requirements.txt` ile gerekli paketleri yükler (pyserial, pywinauto, pyinstaller)
- `IDEC_PLC_Password_Finder.spec` ile tek dosyalık exe üretir

**Yöntem B — Komut satırı**

```cmd
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --noconfirm IDEC_PLC_Password_Finder.spec
```

### 3. EXE dosyasının yeri

Oluşan dosya:

```
idec-pass2\dist\IDEC_PLC_Password_Finder.exe
```

Bu **tek dosyayı** istediğiniz Windows PC'ye kopyalayabilirsiniz. O PC'de:

- Python kurulu olması gerekmez
- WindLDR modu için sadece WindLDR yüklü ve açık olmalı
- Pentra modu için PLC Ethernet’e bağlı olmalı

## Dağıtım

- `dist\IDEC_PLC_Password_Finder.exe` dosyasını USB, ağ paylaşımı veya GitHub Release ile dağıtabilirsiniz.
- Virüs uyarısı: PyInstaller ile üretilen exe’ler bazen antivirüs tarafından işaretlenebilir; güvendiğiniz bilgisayarda üretip “izin ver” / istisna ekleyebilirsiniz.

## Sorun giderme

| Hata | Çözüm |
|------|--------|
| `pip bulunamadı` | Python’u “Add to PATH” ile yeniden kurun veya `python -m pip` kullanın. |
| `pywinauto` hatası | `pip install pywinauto` çalıştırın. |
| EXE açılmıyor | Aynı Windows sürümüne yakın bir PC’de exe’yi tekrar derleyin. |
| Antivirüs engelliyor | EXE’yi “güvenli” olarak işaretleyin veya geçici kapatın. |
