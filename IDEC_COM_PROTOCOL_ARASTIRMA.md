# IDEC COM / Seri Port Protokolü Araştırması

Bu dosya, IDEC PLC (FC4A, MicroSmart) **programlama portu** (COM/RS232) protokolünü bulmak için yapılan araştırmanın özetidir.

---

## FC4A ile Pentra (FC5A) Aynı mı?

**Hayır. Farklı serilerdir.**

| Özellik | **FC4A** (MicroSmart) | **Pentra** = **FC5A** (MicroSmart Pentra) |
|--------|------------------------|-------------------------------------------|
| **Seri adı** | MicroSmart (eski nesil) | MicroSmart **Pentra** |
| **Ürün kodu** | FC4A-xxx (örn. FC4A-C16R2, FC4A-HPC3) | FC5A-xxx (örn. FC5A-C10R2) |
| **Programlama** | Seri/USB, WindLDR | WindLDR; **gömülü Ethernet** (10/100 Mbps) |
| **İletişim** | RS232 programlama portu, Modbus RTU/ASCII (kullanıcı) | Ethernet, Modbus TCP, port **2101** (şifre/programlama), seri RS232/RS485 |
| **Şifre protokolü** | Seri port üzerinden; **dokümante değil** | Ethernet port 2101 üzerinden; [Capkj2/Idec-password-cracker](https://github.com/Capkj2/Idec-password-cracker) ile bilinen paket formatı |
| **Durum** | Üretimden kalktı (end of life) | FC5A serisi de 2019’da üretimden kalktı |

**Sonuç:** Bu projedeki **FC4A-HPC3** ile **Pentra (FC5A)** aynı cihaz değildir. Pentra modu (Ethernet 2101) sadece **FC5A MicroSmart Pentra** için geçerlidir. FC4A için şifre denemesi **WindLDR otomasyonu** veya (protokol bilinmediği için güvenilir olmayan) **COM deneysel** modu kullanılmalıdır.

---

## Özet: Açık Protokol Dokümantasyonu Yok

- **Programlama portu** (WindLDR’ın bağlandığı port) için **komut/çerçeve/paket formatı** resmi ve ücretsiz dokümanda **açıklanmıyor**.
- IDEC’in yayınladığı dokümanlar genel özellikler, Modbus (kullanıcı iletişimi) ve WindLDR kullanımından bahsediyor; **şifre komutu veya programlama protokolü** detayı verilmiyor.

---

## Neler Bulundu?

### 1. Resmi dokümanlar
- **FC9Y-B1143** – FC4A MicroSmart Kullanıcı Kılavuzu  
  - RS485 kullanıcı iletişimi, Modbus ASCII/RTU, sistem program sürümü vb.  
  - Programlama portu için **komut listesi veya çerçeve yapısı yok** (arama sonuçlarında).
- **B-1730** – FC6A İletişim Kılavuzu  
  - FC6A için iletişim detayları; FC4A ile aynı mı bilinmiyor.
- **WindLDR Reference Manual**  
  - Yazılım kullanımı; seri protokol spesifikasyonu değil.

### 2. Teknik bilgiler
- FC4A: Programlama için **RS232** (FC4A-KC1, FC9Y-B3 USB-seri).
- FC4A seri hız: genelde **9600**, maks. **19200 bps** (bazı modellerde 38400 datalink).
- **Modbus RTU/ASCII** dokümanda geçiyor; bu **kullanıcı iletişimi** (veri okuma/yazma) için, programlama/şifre portu için değil.
- Programlama portu muhtemelen **özel (proprietary)** bir protokol kullanıyor; format public değil.

### 3. Üçüncü taraf “unlock” yazılımları
- Bazı siteler “FC4A şifre açma” yazılımı sunuyor; “standart programlama kablosu ve seri protokol” ile çalıştığı yazıyor.
- **Protokolü yayınlamıyorlar**; sadece kullanım iddiası var.

---

## Protokolü Bulmak İçin Olası Yollar

### A) Resmi kılavuzları elle taramak
1. **FC9Y-B1143** (FC4A kullanıcı kılavuzu) PDF’ini indir:  
   [IDEC FC4A MicroSmart User's Manual](https://us.idec.com/idec-us/en/USD/medias/FC9Y-B1143-0-V100.pdf)
2. PDF’te şunları ara: **password**, **communication**, **command**, **frame**, **STX**, **ETX**, **protocol**, **serial**, **upload**, **download**.
3. **FC6A Communication Manual (B-1730)** için de aynısını yap; FC4A ile benzer komut seti olabilir.

### B) IDEC teknik destek
- **support@idec.com** veya bölgesel IDEC destek.
- Sorulacak net soru:  
  *“FC4A programlama portu (RS232) için seri iletişim protokolü (komut/yanıt çerçeve formatı, özellikle şifre doğrulama komutu) dokümanda var mı? Varsa hangi doküman ve sayfa? Yoksa geliştirici için protokol bilgisi verilebilir mi?”*

### C) Seri port dinleme (reverse engineering)
1. **COM port sniffer** veya **seri port proxy** kullan (örn. com0com + bir dinleyici, veya seri port üzerinden trafiği loglayan yazılım).
2. WindLDR ile PLC’ye **yanlış şifre** ile bağlan; trafiği kaydet.
3. **Doğru şifre** ile bağlan; tekrar kaydet.
4. İki kayıttaki **farklı kısımlar** büyük ihtimalle şifre veya şifre ile ilgili alan; paket yapısı (başlık, uzunluk, checksum vb.) bu kayıtlardan çıkarılmaya çalışılır.

### D) WindLDR / IDEC güncellemeleri
- WindLDR veya IDEC sürüm notlarında “communication protocol” / “API” / “SDK” geçiyor mu diye bakmak.
- Şu ana kadar public bir API/SDK bilgisi görülmedi.

---

## Bu projede şu an ne kullanılıyor?

- COM modunda **tahmini** bir komut: `PASSWORD:şifre\r\n` metni gönderiliyor; yanıtta `OK` veya `CONNECTED` aranıyor.
- IDEC’in gerçek protokolü bu olmadığı için **PLC büyük ihtimalle yanıt vermiyor**; COM modu “şifre bulundu” sonucu güvenilir değil.
- **WindLDR’da otomatik dene** modu, protokolü kullanmıyor; sadece WindLDR arayüzünü otomatikleştiriyor; şifre doğrulaması WindLDR üzerinden yapılıyor.

---

## IDEC Pentra (FC5A) – Açık Kaynak Protokol (Ethernet, port 2101)

**Kaynak:** [Capkj2/Idec-password-cracker](https://github.com/Capkj2/Idec-password-cracker) (C++, Windows Winsock)  
Açıklama: IDEC **Pentra** (yani **FC5A** MicroSmart Pentra) PLC’ler için brute-force şifre denemesi; **TCP port 2101** üzerinden çalışıyor. **FC4A ile aynı cihaz değildir** (bkz. yukarıdaki tablo).

### Pentra protokolü özeti

| Öğe | Değer |
|-----|--------|
| Taşıma | TCP, port **2101** (varsayılan) |
| Paket uzunluğu | 18 bayt (binary) |
| Şifre formatı | **Sayısal** (1–99999999); pakette sıfırla doldurulmuş hex olarak gömülü |
| Preamble | Hex: `05 46 46 30 57 56 00 00 00 00 00 00 00 00` (ilk 12 hex karakter sabit; sonrası şifre alanı) |
| Checksum | Paket hex string üzerinde: çift sıradaki karakterlerin XOR’u ^ 0x33, tek sıradakilerin XOR’u ^ 0x30; sonuç > 0x39 ise +0x07. Sonuna 0x30 + checksum 2 bayt + 0x0D eklenir. |

### Yanıt kodları (PLC’den gelen)

- **Geçerli şifre:** `06 30 31 30 33 37 0D` (ACK + "01037" + CR)
- **Geçersiz şifre:** `06 30 31 32 30 35 33 30 0D` ("120530" + CR)
- **Hatalı checksum:** `15 30 31 30 31 30 32 35 0D` (NAK + ...)

### FC4A ile farkı

- Bu protokol **sadece Pentra (FC5A)** için geçerlidir. **FC4A** farklı seridir; seri/USB + WindLDR ile programlanır, Ethernet 2101 protokolü FC4A için tanımlı değildir.
- Bu projede **IDEC Pentra Ethernet (port 2101)** seçeneği yalnızca **FC5A MicroSmart Pentra** cihazları için kullanılmalıdır. FC4A-HPC3 için WindLDR veya COM (deneysel) modu kullanın.
- Seri (COM) programlama portu için bu paket formatı kullanılmıyor; COM tarafı hâlâ dokümante değil.

---

## Sonuç

- **IDEC COM (programlama portu) protokolü** hâlâ **açık ve resmi dokümanda bulunamadı**.
- **IDEC Pentra** için **Ethernet (port 2101)** üzerinde çalışan bir protokol [Capkj2/Idec-password-cracker](https://github.com/Capkj2/Idec-password-cracker) ile mevcut; sayısal şifre denemesi için bu projeye entegre edildi.
- Doğru protokolü uygulayabilmek için ya **resmi doküman/IDEC desteği** ya da **seri trafik kaydı ile reverse engineering** gerekiyor.
- Bu dosya, ileride protokol bulunduğunda veya yeni kaynak eklendiğinde güncellenebilir.
