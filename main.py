import smtplib
import sys
import os
 
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
 
class SMTPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        # Membuat objek SMTP dengan host dan port yang diberikan
        self.smtp = smtplib.SMTP(host, port)
        # Mengaktifkan mode debug untuk melihat pesan-pesan komunikasi dengan server SMTP
        self.smtp.set_debuglevel(1)
 
    def connect(self, email, password):
        try:
            # Mengaktifkan enkripsi TLS
            self.smtp.starttls()
            # Melakukan otentikasi dengan email dan password yang diberikan
            self.smtp.login(email, password)
        except Exception as e:
            print(e)
 
    def disconnect(self):
        # Memutuskan koneksi dengan server SMTP
        self.smtp.quit()
 
    def sendEmail(self, from_addr, to_addr, msg):
        # Mengirim email dengan menggunakan metode sendmail dari objek SMTP
        self.smtp.sendmail(from_addr, to_addr, msg)
 
if __name__ == '__main__':
    # Membuka file untuk mencatat pesan debug dari server SMTP
    log_file = open("smtp_debug.log", 'w')
    original_stderr = sys.stderr
    # Mengganti sys.stderr dengan file log untuk menulis pesan error ke file tersebut
    sys.stderr = log_file
 
    with open(os.path.join(BASE_DIR, 'smtp.conf')) as config_file:
        # Membaca dan mem-parsing konfigurasi SMTP dari file
        config = dict(line.strip().split('=') for line in config_file)
 
    # Mengambil nilai konfigurasi HOST dari config
    HOST = config.get("HOST")
    # Mengambil nilai konfigurasi PORT dari config dan mengonversinya ke integer
    PORT = int(config.get("PORT", 587))
    # Mengambil nilai konfigurasi SENDER_EMAIL dari config
    EMAIL = config.get("SENDER_EMAIL")
    # Mengambil nilai konfigurasi PASSWORD dari config
    PASSWORD = config.get("PASSWORD")
    # Mengambil nilai konfigurasi RECIPIENT_EMAIL dari config
    RECIPIENT_EMAIL = config.get("RECIPIENT_EMAIL")
 
    # Membuat objek SMTPServer dengan host dan port yang telah dibaca
    mySMTP = SMTPServer(HOST, PORT)
    # Terhubung ke server SMTP menggunakan email dan password yang telah dibaca
    mySMTP.connect(EMAIL, PASSWORD)
    # Mengirim email dengan menggunakan metode sendEmail
    mySMTP.sendEmail(EMAIL, RECIPIENT_EMAIL, "This is a test email")
    # Memutuskan koneksi dengan server SMTP
    mySMTP.disconnect()
 
    # Menutup file log
    log_file.close()
    # Mengembalikan sys.stderr ke nilai semula
    sys.stderr = original_stderr
