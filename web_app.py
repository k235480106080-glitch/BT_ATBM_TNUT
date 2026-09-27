import time
import binascii
from flask import Flask, render_template_string, request, jsonify
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

app = Flask(__name__)

# Lưu bộ khóa RSA tạm thời trong RAM
rsa_key_store = {
    "key_pair": None,
    "pub_key": None
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TNUT Security - Demo Mã Hóa Bảo Mật Thông Tin</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Inter:wght@300;400;600;700&display=swap');
        body { font-family: 'Inter', sans-serif; }
        .code-font { font-family: 'Fira Code', monospace; }
        .glow-card { box-shadow: 0 0 25px -5px rgba(59, 130, 246, 0.15); }
    </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen pb-12">

    <!-- HEADER -->
    <header class="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
        <div class="max-w-6xl mx-auto px-4 py-4 flex flex-col md:flex-row justify-between items-center gap-4">
            <div class="flex items-center gap-3">
                <div class="p-2.5 bg-blue-600/20 text-blue-400 rounded-xl border border-blue-500/30">
                    <i class="fa-solid fa-shield-halved text-2xl"></i>
                </div>
                <div>
                    <h1 class="text-xl font-bold bg-gradient-to-r from-blue-400 via-indigo-300 to-purple-400 bg-clip-text text-transparent">
                        HỆ THỐNG DEMO MÃ HÓA & BẢO MẬT THÔNG TIN
                    </h1>
                    <p class="text-xs text-slate-400">Trường Đại học Kỹ thuật Công nghiệp (TNUT)</p>
                </div>
            </div>
            <div class="text-right bg-slate-800/80 px-4 py-2 rounded-lg border border-slate-700/60 text-xs">
                <div class="text-blue-400 font-semibold"><i class="fa-solid fa-user-graduate mr-1"></i>Trần Hoàng Xuân Vũ</div>
                <div class="text-slate-400">MSSV: K235480106080 | Lớp: K59KMT</div>
            </div>
        </div>
    </header>

    <main class="max-w-6xl mx-auto px-4 mt-8">

        <!-- TAB BUTTONS -->
        <div class="flex border-b border-slate-800 mb-8 gap-2">
            <button onclick="switchTab('aes')" id="tab-aes" class="px-5 py-3 font-medium text-sm rounded-t-lg transition flex items-center gap-2 bg-blue-600 text-white">
                <i class="fa-solid fa-lock"></i> 1. Mã hóa AES-128
            </button>
            <button onclick="switchTab('rsa')" id="tab-rsa" class="px-5 py-3 font-medium text-sm rounded-t-lg transition flex items-center gap-2 text-slate-400 hover:text-slate-200 hover:bg-slate-900">
                <i class="fa-solid fa-key"></i> 2. Mã hóa Bất đối xứng RSA-2048
            </button>
            <button onclick="switchTab('hybrid')" id="tab-hybrid" class="px-5 py-3 font-medium text-sm rounded-t-lg transition flex items-center gap-2 text-slate-400 hover:text-slate-200 hover:bg-slate-900">
                <i class="fa-solid fa-bolt"></i> 3. Mã hóa Lai (Hybrid Encryption)
            </button>
        </div>

        <!-- TAB 1: AES -->
        <div id="section-aes" class="space-y-6">
            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 glow-card">
                <h2 class="text-lg font-bold text-blue-400 mb-4 flex items-center gap-2">
                    <i class="fa-solid fa-sliders"></i> Thuật toán đối xứng AES-128 (Chế độ CBC)
                </h2>
                <div class="space-y-4">
                    <div>
                        <label class="block text-xs font-semibold text-slate-400 mb-1">VĂN BẢN CẦN MÃ HÓA (PLAINTEXT)</label>
                        <textarea id="aes-input" rows="3" class="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-sm focus:border-blue-500 focus:outline-none code-font" placeholder="Nhập chuỗi văn bản bất kỳ...">Sinh vien: Tran Hoang Xuan Vu - K235480106080 - TNUT</textarea>
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-400 mb-1">KHÓA BÍ MẬT AES (16 KÝ TỰ / 128 BITS)</label>
                        <input id="aes-key" type="text" class="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-sm focus:border-blue-500 focus:outline-none code-font" value="1234567890123456">
                    </div>
                    <div class="flex gap-3">
                        <button onclick="processAES('encrypt')" class="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold px-6 py-2.5 rounded-xl text-sm transition flex items-center gap-2">
                            <i class="fa-solid fa-lock"></i> Thực hiện Mã hóa
                        </button>
                        <button onclick="processAES('decrypt')" class="bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold px-6 py-2.5 rounded-xl text-sm transition flex items-center gap-2 border border-slate-700">
                            <i class="fa-solid fa-unlock"></i> Thực hiện Giải mã
                        </button>
                    </div>
                </div>
            </div>

            <!-- RESULT DISPLAY -->
            <div id="aes-result-box" class="hidden bg-slate-900 border border-slate-800 rounded-2xl p-6">
                <div class="flex justify-between items-center mb-3">
                    <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">KẾT QUẢ XỬ LÝ</span>
                    <span id="aes-time" class="text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-3 py-1 rounded-full font-mono">0.00 ms</span>
                </div>
                <div class="bg-slate-950 p-4 rounded-xl border border-slate-800 code-font text-sm break-all text-blue-300" id="aes-output"></div>
            </div>
        </div>

        <!-- TAB 2: RSA -->
        <div id="section-rsa" class="hidden space-y-6">
            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 glow-card">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-lg font-bold text-indigo-400 flex items-center gap-2">
                        <i class="fa-solid fa-key"></i> Thuật toán Bất đối xứng RSA-2048
                    </h2>
                    <button onclick="generateRSAKeys()" class="bg-indigo-600/20 hover:bg-indigo-600/30 text-indigo-300 border border-indigo-500/30 font-semibold px-4 py-1.5 rounded-xl text-xs transition flex items-center gap-2">
                        <i class="fa-solid fa-rotate"></i> Sinh cặp khóa RSA mới
                    </button>
                </div>
                <div class="space-y-4">
                    <div>
                        <label class="block text-xs font-semibold text-slate-400 mb-1">DỮ LIỆU CẦN MÃ HÓA (Tối đa 190 Bytes)</label>
                        <input id="rsa-input" type="text" class="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-sm focus:border-indigo-500 focus:outline-none code-font" value="Tran Hoang Xuan Vu - K235480106080">
                    </div>
                    <div class="flex gap-3">
                        <button onclick="processRSA('encrypt')" class="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-semibold px-6 py-2.5 rounded-xl text-sm transition flex items-center gap-2">
                            <i class="fa-solid fa-lock"></i> Mã hóa bằng Public Key
                        </button>
                        <button onclick="processRSA('decrypt')" class="bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold px-6 py-2.5 rounded-xl text-sm transition flex items-center gap-2 border border-slate-700">
                            <i class="fa-solid fa-key"></i> Giải mã bằng Private Key
                        </button>
                    </div>
                </div>
            </div>

            <div id="rsa-result-box" class="hidden bg-slate-900 border border-slate-800 rounded-2xl p-6">
                <div class="flex justify-between items-center mb-3">
                    <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">BẢN MÃ RSA (HEX)</span>
                    <span id="rsa-time" class="text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-3 py-1 rounded-full font-mono">0.00 ms</span>
                </div>
                <div class="bg-slate-950 p-4 rounded-xl border border-slate-800 code-font text-xs break-all text-indigo-300" id="rsa-output"></div>
            </div>
        </div>

        <!-- TAB 3: HYBRID -->
        <div id="section-hybrid" class="hidden space-y-6">
            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 glow-card">
                <h2 class="text-lg font-bold text-purple-400 mb-2 flex items-center gap-2">
                    <i class="fa-solid fa-bolt"></i> Mô hình Mã hóa Lai (Hybrid Cryptosystem)
                </h2>
                <p class="text-xs text-slate-400 mb-6">Kết hợp tốc độ xử lý của AES-128 và tính năng bảo mật chia sẻ khóa của RSA-2048.</p>
                
                <div class="space-y-4">
                    <div>
                        <label class="block text-xs font-semibold text-slate-400 mb-1">TỆP DỮ LIỆU / VĂN BẢN DUNG LƯỢNG LỚN</label>
                        <textarea id="hybrid-input" rows="3" class="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-sm focus:border-purple-500 focus:outline-none code-font" placeholder="Nhập nội dung dữ liệu dung lượng tùy ý...">Báo cáo đồ án môn An toàn và Bảo mật thông tin - Sinh viên Trần Hoàng Xuân Vũ - K235480106080 - TNUT.</textarea>
                    </div>
                    <button onclick="processHybrid()" class="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white font-semibold px-6 py-2.5 rounded-xl text-sm transition flex items-center gap-2">
                        <i class="fa-solid fa-shield-cat"></i> Thực thi Mô hình Mã hóa Lai
                    </button>
                </div>
            </div>

            <div id="hybrid-result-box" class="hidden bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
                <div class="flex justify-between items-center">
                    <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">KẾT QUẢ QUÁ TRÌNH MÃ HÓA LAI</span>
                    <span id="hybrid-time" class="text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-3 py-1 rounded-full font-mono">0.00 ms</span>
                </div>
                <div>
                    <span class="text-xs text-slate-400 font-semibold">1. Khóa phiên AES (128-bit Random Session Key):</span>
                    <div class="bg-slate-950 p-3 rounded-lg border border-slate-800 code-font text-xs text-yellow-400 mt-1" id="hyb-session-key"></div>
                </div>
                <div>
                    <span class="text-xs text-slate-400 font-semibold">2. Khóa phiên AES sau khi Mã hóa bằng RSA Public Key:</span>
                    <div class="bg-slate-950 p-3 rounded-lg border border-slate-800 code-font text-xs text-purple-300 break-all mt-1" id="hyb-enc-key"></div>
                </div>
                <div>
                    <span class="text-xs text-slate-400 font-semibold">3. Bản mã Payload dữ liệu (Mã hóa bằng AES):</span>
                    <div class="bg-slate-950 p-3 rounded-lg border border-slate-800 code-font text-xs text-blue-300 break-all mt-1" id="hyb-enc-payload"></div>
                </div>
            </div>
        </div>

    </main>

    <script>
        function switchTab(tab) {
            ['aes', 'rsa', 'hybrid'].forEach(t => {
                document.getElementById('section-' + t).classList.add('hidden');
                document.getElementById('tab-' + t).className = "px-5 py-3 font-medium text-sm rounded-t-lg transition flex items-center gap-2 text-slate-400 hover:text-slate-200 hover:bg-slate-900";
            });
            document.getElementById('section-' + tab).classList.remove('hidden');
            document.getElementById('tab-' + tab).className = "px-5 py-3 font-medium text-sm rounded-t-lg transition flex items-center gap-2 bg-blue-600 text-white";
        }

        async function processAES(action) {
            const text = document.getElementById('aes-input').value;
            const key = document.getElementById('aes-key').value;
            const res = await fetch('/api/aes/' + action, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text, key})
            });
            const data = await res.json();
            document.getElementById('aes-result-box').classList.remove('hidden');
            document.getElementById('aes-output').innerText = data.result;
            document.getElementById('aes-time').innerText = data.time + ' ms';
        }

        async function generateRSAKeys() {
            const res = await fetch('/api/rsa/generate');
            const data = await res.json();
            alert('✅ Khởi tạo bộ khóa RSA-2048 mới thành công!');
        }

        async function processRSA(action) {
            const text = document.getElementById('rsa-input').value;
            const res = await fetch('/api/rsa/' + action, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text})
            });
            const data = await res.json();
            document.getElementById('rsa-result-box').classList.remove('hidden');
            document.getElementById('rsa-output').innerText = data.result;
            document.getElementById('rsa-time').innerText = data.time + ' ms';
        }

        async function processHybrid() {
            const text = document.getElementById('hybrid-input').value;
            const res = await fetch('/api/hybrid/encrypt', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text})
            });
            const data = await res.json();
            document.getElementById('hybrid-result-box').classList.remove('hidden');
            document.getElementById('hyb-session-key').innerText = data.session_key;
            document.getElementById('hyb-enc-key').innerText = data.enc_key;
            document.getElementById('hyb-enc-payload').innerText = data.enc_payload;
            document.getElementById('hybrid-time').innerText = data.time + ' ms';
        }
    </script>
</body>
</html>
"""

def init_rsa():
    if not rsa_key_store["key_pair"]:
        key = RSA.generate(2048)
        rsa_key_store["key_pair"] = key
        rsa_key_store["pub_key"] = key.publickey()

init_rsa()

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/aes/encrypt', methods=['POST'])
def aes_encrypt():
    data = request.json
    text = data.get('text', '').encode('utf-8')
    key = data.get('key', '1234567890123456').encode('utf-8')[:16]
    
    t0 = time.perf_counter()
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(text, AES.block_size))
    elapsed = (time.perf_counter() - t0) * 1000
    
    result = binascii.hexlify(cipher.iv + ct_bytes).decode('utf-8')
    return jsonify({"result": result, "time": f"{elapsed:.3f}"})

@app.route('/api/aes/decrypt', methods=['POST'])
def aes_decrypt():
    data = request.json
    try:
        raw_hex = binascii.unhexlify(data.get('text', ''))
        key = data.get('key', '1234567890123456').encode('utf-8')[:16]
        iv = raw_hex[:16]
        ct = raw_hex[16:]
        
        t0 = time.perf_counter()
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size).decode('utf-8')
        elapsed = (time.perf_counter() - t0) * 1000
        
        return jsonify({"result": pt, "time": f"{elapsed:.3f}"})
    except Exception as e:
        return jsonify({"result": f"Lỗi giải mã: {str(e)}", "time": "0.000"})

@app.route('/api/rsa/generate')
def rsa_gen():
    init_rsa()
    return jsonify({"status": "ok"})

@app.route('/api/rsa/encrypt', methods=['POST'])
def rsa_encrypt():
    data = request.json
    text = data.get('text', '').encode('utf-8')
    cipher = PKCS1_OAEP.new(rsa_key_store["pub_key"])
    
    t0 = time.perf_counter()
    ct = cipher.encrypt(text)
    elapsed = (time.perf_counter() - t0) * 1000
    
    return jsonify({"result": binascii.hexlify(ct).decode('utf-8'), "time": f"{elapsed:.3f}"})

@app.route('/api/rsa/decrypt', methods=['POST'])
def rsa_decrypt():
    data = request.json
    try:
        ct = binascii.unhexlify(data.get('text', ''))
        cipher = PKCS1_OAEP.new(rsa_key_store["key_pair"])
        
        t0 = time.perf_counter()
        pt = cipher.decrypt(ct).decode('utf-8')
        elapsed = (time.perf_counter() - t0) * 1000
        
        return jsonify({"result": pt, "time": f"{elapsed:.3f}"})
    except Exception as e:
        return jsonify({"result": f"Lỗi giải mã RSA: {str(e)}", "time": "0.000"})

@app.route('/api/hybrid/encrypt', methods=['POST'])
def hybrid_encrypt():
    data = request.json
    text = data.get('text', '').encode('utf-8')
    
    t0 = time.perf_counter()
    session_key = get_random_bytes(16)
    cipher_aes = AES.new(session_key, AES.MODE_CBC)
    enc_payload = cipher_aes.encrypt(pad(text, AES.block_size))
    
    cipher_rsa = PKCS1_OAEP.new(rsa_key_store["pub_key"])
    enc_session_key = cipher_rsa.encrypt(session_key)
    elapsed = (time.perf_counter() - t0) * 1000
    
    return jsonify({
        "session_key": binascii.hexlify(session_key).decode('utf-8'),
        "enc_key": binascii.hexlify(enc_session_key).decode('utf-8'),
        "enc_payload": binascii.hexlify(cipher_aes.iv + enc_payload).decode('utf-8'),
        "time": f"{elapsed:.3f}"
    })

if __name__ == '__main__':
    print("\n========================================================")
    print("🚀 Web App ATBM TNUT đang chạy tại: http://localhost:5000")
    print("========================================================\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
