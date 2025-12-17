
### qr_code_generator.py

**Required libraries:**
```bash
python -m pip install qrcode
python -m pip install image
```

<img width="300" height="300" alt="Image" src="https://github.com/user-attachments/assets/1de1dce3-e725-4755-92b0-75796c313563" />

### youtube_mp3_downloader.py
**Gerekli Kurulumlar:**
```bash
1) Python 3.9+ yüklü olmalı
2) yt-dlp kurulumu:
   python -m pip install yt-dlp

3) FFmpeg kurulumu (zorunlu):  // mp3 dönüşümü için
   https://www.gyan.dev/ffmpeg/builds/
   ffmpeg-release-essentials.zip indir
   ffmpeg/bin klasörünü PATH’e ekle

Kontrol:
   ffmpeg -version
```  

<img width="400" height="400" alt="Image" src="https://github.com/user-attachments/assets/a28f7534-d829-4f4e-8ed4-74e1257958f0" />


### face_detection.py
```bash
python -m pip install opencv-python
```  
<img width="400" height="400" alt="Image" src="https://github.com/user-attachments/assets/445f1d1f-3f66-4214-93bc-691d6840aca5" />

<img width="400" height="400" alt="Image" src="https://github.com/user-attachments/assets/367a4e8a-008d-461a-8de5-62bebdb5ee35" />

### hand_tracker.py
```bash
python -m pip install opencv-python
python -m pip install opencv-python mediapipe
``` 
<img width="400" height="400" alt="Image" src="https://github.com/user-attachments/assets/1298d44b-2d3c-4335-bd82-f5a99e14da97" />

<img width="400" height="400" alt="Image" src="https://github.com/user-attachments/assets/c2b73a1c-78a1-4c8e-9aee-1e50a0ce11bf" />

### body_posture_detection.py
```bash
python -m pip install opencv-python
python -m pip install opencv-python mediapipe
``` 
https://github.com/user-attachments/assets/53439fdc-4e56-4ba7-81f2-becea580bd50

### duplicate_remove.py

belirttiğin bir klasör içindeki duplicate (aynı) dosyaları silen sade ve güvenli bir Python kodu var.
Mantık: Dosyaların hash (SHA256) değerini alır, birebir aynı olanlardan sadece birini bırakır.

Bu yöntem dosya adına değil içeriğine bakar, en sağlıklısıdır.

### secure_file_verifier.py

Kriptografik karma fonksiyonları kullanarak dosya bütünlüğünü doğrulayan hafif bir Python yardımcı programı.
Depolanmış ve mevcut karma değerlerini karşılaştırarak yetkisiz değişiklikleri tespit eder.


### not_tut.py

- Not Defteri Pro, PyQt5 kullanılarak geliştirilmiş masaüstü bir metin düzenleyici uygulamasıdır.
- Zengin metin formatında not alma, görsel ekleme ve belgeleri PDF olarak dışa aktarma imkânı sunar.
- Otomatik kayıt özelliği sayesinde veri kaybını önler.

## Özellikler
- Zengin metin düzenleme (font, boyut, kalın, italik, altı çizili)
- Metin hizalama (sol, orta, sağ, iki yana yasla)
- Metin rengi seçimi
- Resim ekleme (dosyadan ekleme ve panodan yapıştırma)
- HTML ve TXT dosyalarını açma ve kaydetme
- PDF formatında dışa aktarma
- Otomatik kayıt ve önceki oturumu geri yükleme
- Pencere boyutu ve konum bilgisini hatırlama


## Kurulum
- PyQt5 kütüphanesini yüklemek için:
  ```bash
  pip install PyQt5
  ``` 
<img width="400" height="400" alt="Image" src="https://github.com/user-attachments/assets/6eb7ffc8-4408-4deb-96a7-760cc8726428" />



### keylogger.py

- Eğitim amaçlı geliştirilmiş basit bir keylogger uygulaması. Klavye tuşlarını kaydeder ve belirli aralıklarla e-posta ile gönderir.

## Uyarı

Bu proje **yalnızca eğitim amaçlıdır**. Başkalarının cihazlarında izinsiz kullanımı **yasadışıdır** ve ciddi hukuki sonuçları vardır. Sadece kendi cihazınızda ve yasal amaçlarla kullanın.

## Özellikler

- Klavye tuşlarını gerçek zamanlı olarak kaydeder
- Basılan tuşları tarih/saat damgası ile txt dosyasına yazar
- Belirlenen süre aralıklarında logları e-posta ile gönderir
- Mail gönderildikten sonra log dosyasını temizler


## Kurulum

1. Repoyu klonlayın:
```bash
git clone https://github.com/kullanici-adiniz/keylogger-project.git
cd keylogger-project
```

2. Gerekli kütüphaneyi yükleyin:
```bash
pip install keyboard
```

3. Gmail uygulama şifresi oluşturun:
   - Gmail hesabınızda 2 adımlı doğrulamayı açın
   - [Google Uygulama Şifreleri](https://myaccount.google.com/apppasswords) sayfasından şifre oluşturun

4. Kod içindeki mail ayarlarını düzenleyin:
```python
mail.login('sizin-mail@gmail.com', 'UYGULAMA_ŞİFRENİZ')
```


<img width="600" height="600" alt="Image" src="https://github.com/user-attachments/assets/5c2ef516-07fa-4ea3-8006-1490b5a18f14" />
