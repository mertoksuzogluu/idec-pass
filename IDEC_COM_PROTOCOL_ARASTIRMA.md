# IDEC COM / Seri Port Protokolü Araştırması

Bu dosya, IDEC PLC (FC4A, MicroSmart) **programlama portu** (COM/RS232) protokolünü bulmak için yapılan araştırmanın özetidir.

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

## Sonuç

- **IDEC COM (programlama portu) protokolü** hâlâ **açık ve resmi dokümanda bulunamadı**.
- Doğru protokolü uygulayabilmek için ya **resmi doküman/IDEC desteği** ya da **seri trafik kaydı ile reverse engineering** gerekiyor.
- Bu dosya, ileride protokol bulunduğunda veya yeni kaynak eklendiğinde güncellenebilir.
