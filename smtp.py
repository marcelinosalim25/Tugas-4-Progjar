import smtplib
import logging
import base64
import socket

logging.basicConfig(filename='smtp_log.txt', level=logging.DEBUG)

smtp_server = 'smtp.office365.com'
smtp_port = 587

username = 'email@mhs.its.ac.id'
password = 'pass'

server = smtplib.SMTP(smtp_server, smtp_port)

try:
    server.set_debuglevel(1)

    hostname = socket.gethostname()

    server.ehlo(hostname)

    server.starttls()

    server.login(username, password)

    from_addr = username
    to_addr = 'email@gmail.com'
    subject = 'Subject: Test Email'
    body = 'This is a test email sent from Python script.'
    msg = f'{subject}\n\n{body}'
    server.sendmail(from_addr, to_addr, msg)

    print("1. Pesan EHLO:")
    print(server.ehlo_msg)

    print("2. Pesan dukungan TLS:")
    if 'STARTTLS' in server.esmtp_features:
        print('250-STARTTLS')

    print("3. Pesan server siap kirim email:")
    print(server.esmtp_features.get('AUTH', ''))

    print("4. Pesan username yang sudah di-hash:")
    encoded_username = base64.b64encode(username.encode()).decode()
    encoded_password = base64.b64encode(password.encode()).decode()
    print(f'AUTH LOGIN {encoded_username}\r\n')
    print(f'AUTH LOGIN {encoded_password}\r\n')

    print("5. Pesan balasan server dari hello message:")
    print(server.helo_resp)
    
    print("6. Pesan koneksi ditutup:")
    print(server.quit())

finally:
    server.close()
