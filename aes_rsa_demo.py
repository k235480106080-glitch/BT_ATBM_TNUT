import time
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def demo_aes():
    print("==================================================")
    print("1. DEMO THUẬT TOÁN MÃ HÓA ĐỐI XỨNG AES-128 (CBC)")
    print("==================================================")
    key = get_random_bytes(16) # Khóa 128-bit ngẫu nhiên
    data = "Sinh vien: Tran Hoang Xuan Vu - MSSV: K235480106080 - Lop: K59KMT".encode('utf-8')
    
    # Process Mã hóa AES
    t0 = time.perf_counter()
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    iv = cipher.iv
    t_enc_aes = (time.perf_counter() - t0) * 1000 # ms
    
    # Process Giải mã AES
    t0 = time.perf_counter()
    cipher_dec = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher_dec.decrypt(ciphertext), AES.block_size)
    t_dec_aes = (time.perf_counter() - t0) * 1000 # ms
    
    print(f"[-] Văn bản gốc: {data.decode('utf-8')}")
    print(f"[-] Bản mã AES (Hex): {ciphertext.hex()[:60]}...")
    print(f"[-] Giải mã thành công: {decrypted_data.decode('utf-8')}")
    print(f"[*] Thời gian mã hóa AES: {t_enc_aes:.4f} ms")
    print(f"[*] Thời gian giải mã AES: {t_dec_aes:.4f} ms\n")
    return key, ciphertext

def demo_rsa_hybrid(aes_key):
    print("==================================================")
    print("2. DEMO THUẬT TOÁN RSA & MÔ HÌNH MÃ HÓA LAI (HYBRID)")
    print("==================================================")
    print("[+] Đang sinh cặp khóa RSA-2048...")
    rsa_key = RSA.generate(2048)
    pub_key = rsa_key.publickey()
    
    # Mã hóa khóa AES bằng RSA Public Key
    cipher_rsa = PKCS1_OAEP.new(pub_key)
    t0 = time.perf_counter()
    enc_aes_key = cipher_rsa.encrypt(aes_key)
    t_enc_rsa = (time.perf_counter() - t0) * 1000
    
    # Giải mã khóa AES bằng RSA Private Key
    cipher_rsa_dec = PKCS1_OAEP.new(rsa_key)
    t0 = time.perf_counter()
    dec_aes_key = cipher_rsa_dec.decrypt(enc_aes_key)
    t_dec_rsa = (time.perf_counter() - t0) * 1000
    
    print(f"[-] Khóa AES gốc (Hex): {aes_key.hex()}")
    print(f"[-] Khóa AES mã hóa bằng RSA (Hex): {enc_aes_key.hex()[:60]}...")
    print(f"[-] Khóa AES sau khi dùng RSA Private Key giải mã: {dec_aes_key.hex()}")
    print(f"[-] Khóa khớp 100%: {aes_key == dec_aes_key}")
    print(f"[*] Thời gian mã hóa bằng RSA: {t_enc_rsa:.4f} ms")
    print(f"[*] Thời gian giải mã bằng RSA: {t_dec_rsa:.4f} ms\n")

if __name__ == "__main__":
    key, _ = demo_aes()
    demo_rsa_hybrid(key)
