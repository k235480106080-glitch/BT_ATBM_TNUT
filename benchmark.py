import time
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

print("==========================================================================")
print("      BÀI THỰC NGHIỆM ĐÁNH GIÁ HIỆU NĂNG: AES vs RSA vs HYBRID CRYPTO     ")
print("      Sinh vien: Tran Hoang Xuan Vu - MSSV: K235480106080 - Lop: K59KMT   ")
print("==========================================================================")

print("\n[+] Đang khởi tạo bộ khóa RSA-2048 bit...")
rsa_key = RSA.generate(2048)
rsa_pub = rsa_key.publickey()

# Các kích thước dữ liệu thử nghiệm
sizes = [
    ("64 Bytes", 64),
    ("190 Bytes (Max RSA)", 190),
    ("1 KiloByte (1 KB)", 1024),
    ("100 KiloBytes (100 KB)", 1024 * 100),
    ("1 MegaByte (1 MB)", 1024 * 1024)
]

print("\n" + "="*88)
print(f"{'Dung lượng Data':<22} | {'AES-128 (Mã hóa / Giải mã)':<26} | {'RSA-2048 (Mã hóa / Giải mã)':<26} | {'Mã hóa lai (Hybrid)':<20}")
print("="*88)

for label, size in sizes:
    data = get_random_bytes(size)
    
    # 1. AES-128 CBC Mode
    aes_key = get_random_bytes(16)
    t0 = time.perf_counter()
    cipher_aes = AES.new(aes_key, AES.MODE_CBC)
    ct_aes = cipher_aes.encrypt(pad(data, AES.block_size))
    t_aes_enc = (time.perf_counter() - t0) * 1000
    
    t0 = time.perf_counter()
    cipher_dec = AES.new(aes_key, AES.MODE_CBC, cipher_aes.iv)
    unpad(cipher_dec.decrypt(ct_aes), AES.block_size)
    t_aes_dec = (time.perf_counter() - t0) * 1000
    
    str_aes = f"{t_aes_enc:.2f}ms / {t_aes_dec:.2f}ms"
    
    # 2. RSA-2048 Direct Mode (Bị giới hạn tối đa ~190 Bytes với padding OAEP)
    if size <= 190:
        cipher_rsa = PKCS1_OAEP.new(rsa_pub)
        t0 = time.perf_counter()
        ct_rsa = cipher_rsa.encrypt(data)
        t_rsa_enc = (time.perf_counter() - t0) * 1000
        
        cipher_rsa_dec = PKCS1_OAEP.new(rsa_key)
        t0 = time.perf_counter()
        cipher_rsa_dec.decrypt(ct_rsa)
        t_rsa_dec = (time.perf_counter() - t0) * 1000
        str_rsa = f"{t_rsa_enc:.2f}ms / {t_rsa_dec:.2f}ms"
    else:
        str_rsa = "LỖI: >190B (Quá tải)"
        
    # 3. Hybrid Encryption (AES payload + RSA Key wrap)
    t0 = time.perf_counter()
    session_key = get_random_bytes(16)
    c_aes = AES.new(session_key, AES.MODE_CBC)
    c_data = c_aes.encrypt(pad(data, AES.block_size))
    c_rsa = PKCS1_OAEP.new(rsa_pub)
    c_key = c_rsa.encrypt(session_key)
    t_hyb_enc = (time.perf_counter() - t0) * 1000
    
    t0 = time.perf_counter()
    dec_rsa = PKCS1_OAEP.new(rsa_key)
    d_key = dec_rsa.decrypt(c_key)
    dec_aes = AES.new(d_key, AES.MODE_CBC, c_aes.iv)
    unpad(dec_aes.decrypt(c_data), AES.block_size)
    t_hyb_dec = (time.perf_counter() - t0) * 1000
    
    str_hyb = f"{t_hyb_enc:.2f}ms / {t_hyb_dec:.2f}ms"
    
    print(f"{label:<22} | {str_aes:<26} | {str_rsa:<26} | {str_hyb:<20}")

print("="*88 + "\n")
