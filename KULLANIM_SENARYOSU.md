# IDEC PLC Şifre Kurtarma – Sizin Senaryo

Bu rehber, **şifresini unuttuğunuz IDEC PLC**’ye COM port ile bağlanıp, yazılımda (WindLDR vb.) şifre istendiği noktada şifreyi bulmak için aracı nasıl kullanacağınızı anlatır.

---

## Senaryo Özeti

1. PLC’yi bilgisayara **herhangi bir COM port** ile bağlıyorsunuz (USB–seri dönüştürücü veya doğrudan seri port).
2. IDEC yazılımını (WindLDR vb.) açıp PLC’ye bağlanmak istiyorsunuz.
3. **Şifre tam bu noktada** isteniyor; şifreyi bilmiyorsunuz.
4. Bu araç, denenecek şifre listesini otomatik denemek veya size listeden manuel denemeniz için vermek için kullanılır.

---

## Adım 1: PLC’yi Bilgisayara Bağlayın

- PLC’yi USB–seri kablosu veya seri port ile bilgisayara bağlayın.
- Gerekli sürücüler yüklü olsun (genelde kablo ile gelen CD veya üretici sitesinden).

---

## Adım 2: COM Port Numarasını Bulun

1. **Cihaz Yöneticisi**’ni açın:  
   `Win + X` → **Cihaz Yöneticisi**
2. **“Bağlantı noktaları (COM ve LPT)”** bölümünü açın.
3. PLC’nin bağlı olduğu portu bulun (örnek: **COM3**, **COM4**).
4. Bu **COM numarasını not alın** (örn: COM3).

---

## Adım 3: Aracı Kurun ve Çalıştırın

### Seçenek A: Python ile (önerilen)

1. **Python 3.8+** yüklü olsun.
2. Klasöre gidin:
   ```batch
   cd C:\Users\merto\idec-pass
   ```
3. Bağımlılıkları yükleyin:
   ```batch
   pip install -r requirements.txt
   ```
4. GUI programını çalıştırın:
   ```batch
   python idec_plc_password_auto.py
   ```

### Seçenek B: Hazır .exe varsa

- `IDEC_PLC_Password_Finder.exe` dosyasına çift tıklayın (Python gerekmez).

---

## Adım 4: Programda Ayarlar

1. **Bağlantı Tipi:**  
   - **WindLDR'da otomatik dene (önerilen):** WindLDR açıkken şifre penceresi açık olsun; program şifreleri orada otomatik dener. COM port gerekmez.  
   - **USB/Serial (deneysel):** IDEC seri protokolü dokümante olmadığı için PLC çoğu zaman yanıt vermez; yine de denemek isterseniz COM portu ve baud seçin.
2. **WindLDR penceresini tara (tanı):** WindLDR açıksa bu butonla penceredeki kontroller log’a yazılır; farklı WindLDR sürümü/dil kullanıyorsanız tanı için faydalıdır.
3. **COM Port / IP:** Serial/Ethernet kullanıyorsanız port veya IP girin (örn: **COM3**).
4. **COM Portları Listele** ile portları kontrol edebilirsiniz.
5. **Baud Rate:** Genelde **9600** (IDEC için yaygın).

---

## Adım 5: Şifre Aramayı Başlatın

1. **WindLDR modunda:** WindLDR’ı açın, PLC’ye bağlanmayı deneyin; şifre/bağlantı penceresi açık kalsın. **“Şifre Aramayı Başlat”** ile program bu penceredeki şifre kutusuna yazıp “Bağlan”a basarak şifreleri dener.
2. Program listedeki şifreleri sırayla dener; ilerleme ve log ekranda görünür.
3. **Şifre bulunursa** pencerede gösterilir; bu şifreyi WindLDR’da kullanın.

---

## Eğer Otomatik Bulamazsa (COM / Serial)

Bazı IDEC modellerinde seri port üzerinden şifre denemesi, cihazın protokolüne bağlı olarak çalışmayabilir. Bu durumda:

1. Programın **“Sonuçlar”** / log kısmında veya aşağıdaki listede gördüğünüz şifreleri **elle** deneyin.
2. **WindLDR** (veya kullandığınız yazılım) içinde PLC’ye bağlanırken şifre istendiğinde:
   - Önce **boş** bırakıp Enter deneyin.
   - Sonra sırayla: **admin**, **password**, **idec**, **1234**, **0000**, **fc4a**, **hpc3** vb.
3. Bu liste `idec_plc_password_auto.py` içindeki `PASSWORD_LIST` ile aynıdır; hepsini deneyebilirsiniz.

---

## Denenecek Şifre Listesi (Manuel Kullanım)

Yazılımda şifre istenen yerde sırayla deneyin:

- *(Boş)* – hiçbir şey yazmadan Enter  
- admin, ADMIN, password, idec, IDEC  
- fc4a, FC4A, hpc3, HPC3  
- 1234, 12345, 0000, 1111  
- admin123, password123, idec123  
- PLC, factory, default, user, root, system, operator, technician, service  

---

## Son Çare: Donanımsal Reset

Hiçbir şifre işe yaramazsa, kullanım kılavuzuna göre **donanımsal reset** gerekebilir:

1. PLC’nin gücünü kapatın.
2. **RESET** butonunu bulun (genelde yan tarafta veya küçük bir delikte).
3. RESET’e **basılı tutarak** gücü açın.
4. **5–10 saniye** basılı tutun, sonra bırakın.

**Uyarı:** Reset çoğu modelde **programı da siler**. Mümkünse yedek alın veya programı kaybetmeyi kabul edin.

---

## Özet Akış

```
PLC → COM port ile bilgisayara bağlı
       ↓
COM port numarasını not al (örn. COM3)
       ↓
idec_plc_password_auto.py çalıştır (veya .exe)
       ↓
Bağlantı: USB/Serial, COM3, Baud 9600
       ↓
"Şifre Aramayı Başlat" → Bulunan şifreyi WindLDR’da kullan
       ↓
Bulunamazsa → Aynı listeyi WindLDR’da elle dene
       ↓
Yine olmazsa → Donanımsal reset (program silinebilir)
```

---

## Sorun Giderme

| Sorun | Çözüm |
|--------|--------|
| COM port görünmüyor | USB/seri sürücüsünü yükleyin; Cihaz Yöneticisi’nde COM’u kontrol edin. |
| “Port açılamıyor” | WindLDR’ı kapatın; aynı COM portu aynı anda iki program kullanamaz. |
| Hiçbir şifre çalışmıyor | Listeyi WindLDR’da elle deneyin; gerekirse donanımsal reset. |

Bu senaryo, şifresini unuttuğunuz IDEC PLC’yi COM port ile bağlayıp yazılımda şifre istediği noktada kullanım içindir.
