log_file_path = "smtp_debug.log"
 
def parsingText(text):
    # Memisahkan teks berdasarkan ": " dan mengambil bagian setelah ": "
    text = ": ".join(text.split(': ')[1:])
    return text
 
conditions = {
    # 1. Mencetak pesah EHLO
    "ehlo": lambda line: print(parsingText(line)),
    # 2. Mencetak pesan yang menyatakan bahwa server mendukung TLS
    "250-starttls": lambda line: print(parsingText(line)),
    # 3. Mencetak pesan yang menyatakan server siap mengirim email
    "msg: b'2.0.0 smtp server ready": lambda line: print(parsingText(line)),
    # 4. Mencetak pesan yang menunjukkan username yang sudah di-hash
    "send: 'auth login": lambda line: print(parsingText(line)),
    # 5. Mencetak pesan balasan server dari sebuah hello message dari client
    "reply: b'250-si": lambda line: print(parsingText(line)),
    # 6. Mencetak pesan bahwa koneksi telah ditutup
    "reply: b'221 2.0.0": lambda line: print(parsingText(line)),
    "send: 'rcpt to:": lambda line: print(parsingText(line))
}

matched_conditions = set()
 
# Membuka file log dalam mode baca
with open(log_file_path, 'r') as log_file:
    # Membaca setiap baris dalam file log
    for line in log_file.readlines():
        # Loop dan periksa apakah ada kondisi yang cocok
        for condition, action in conditions.items():
            if condition in line.lower() and condition not in matched_conditions:
                action(line)
                matched_conditions.add(condition)
                break
