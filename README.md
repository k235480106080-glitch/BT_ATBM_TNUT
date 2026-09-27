# BÀI TẬP VỀ NHÀ MÔN AN TOÀN VÀ BẢO MẬT THÔNG TIN - TNUT

## 👤 THÔNG TIN SINH VIÊN

* **Họ và tên**: Trần Hoàng Xuân Vũ
* **Mã sinh viên**: K235480106080
* **Lớp**: K59KMT - Kĩ thuật máy tính
* **Môn học**: An toàn và bảo mật thông tin
* **Deadline**: 23h59 ngày 28/09/2026
* **GitHub Repository**: https://github.com/k235480106080-glitch/BT\_ATBM\_TNUT

\---

# 📌 MỤC 1. THUẬT TOÁN MÃ HÓA HIỆN ĐẠI DES VÀ AES

## 1.1. Thuật toán mã hóa DES (Data Encryption Standard)

### A. Mô tả thuật toán

* **Loại mã hóa**: Mã hóa đối xứng khối (Symmetric Block Cipher) dựa trên cấu trúc **Mạng Feistel (Feistel Network)**.
* **Kích thước khối dữ liệu**: **64 bits** cho mỗi khối mã hóa.
* **Độ dài khóa**: Khóa đầu vào dài 64 bits (8 bits kiểm tra chẵn lẻ parity check), độ dài khóa thực tế dùng để mã hóa là **56 bits**.

### B. Quy trình mã hóa (Encryption Process)

1. **Hoán vị ban đầu (Initial Permutation - IP)**: Sắp xếp lại thứ tự 64 bits đầu vào theo bảng hoán vị cố định.
2. **16 Vòng Feistel (16 Rounds)**:

   * Chia 64 bits thành 2 nửa 32 bits: Nửa trái **L<sub>0</sub>** và Nửa phải **R<sub>0</sub>**.
   * Tại mỗi vòng `i` (từ `i = 1` đến `16`), biến đổi theo công thức:

> \*\*L<sub>i</sub> = R<sub>i-1</sub>\*\*  
   > \*\*R<sub>i</sub> = L<sub>i-1</sub> ⊕ f(R<sub>i-1</sub>, K<sub>i</sub>)\*\*

   * **Hàm f(R<sub>i-1</sub>, K<sub>i</sub>)** bao gồm 4 bước: **Expansion (E-box) → XOR Key K<sub>i</sub> → S-Boxes Substitution → Permutation (P-box)**.
3. **Đảo ngược 2 nửa \& Hoán vị cuối (Final Permutation - IP⁻¹)**: Ghép **R<sub>16</sub>L<sub>16</sub>** và thực hiện hoán vị **IP⁻¹** thu được bản mã 64 bits.

### C. Quy trình giải mã (Decryption Process)

* Quy trình giải mã hoàn toàn giống hệt quy trình mã hóa.
* Khóa vòng **K<sub>i</sub>** được đưa vào theo thứ tự ngược lại: **K<sub>16</sub>, K<sub>15</sub>, ..., K<sub>1</sub>**.

\---

## 1.2. Thuật toán mã hóa AES (Advanced Encryption Standard)

### A. Mô tả thuật toán

* **Loại mã hóa**: Mã hóa đối xứng khối dựa trên cấu trúc **Mạng thế - hoán vị (Substitution-Permutation Network - SPN)**.
* **Kích thước khối dữ liệu**: Cố định **128 bits** (Ma trận trạng thái State 4x4 bytes).
* **Độ dài khóa \& Số vòng lặp**:

  * **AES-128**: Khóa **128 bits** (16 bytes) → **10 vòng mã hóa**.
  * **AES-192**: Khóa **192 bits** (24 bytes) → **12 vòng mã hóa**.
  * **AES-256**: Khóa **256 bits** (32 bytes) → **14 vòng mã hóa**.

### B. Quy trình mã hóa AES-128 (10 vòng)

1. **Mở rộng khóa (Key Expansion)**: Tạo 11 khóa vòng từ khóa chính 128 bits.
2. **Vòng khởi tạo (Initial Round)**: **AddRoundKey** (XOR State với K<sub>0</sub>).
3. **9 Vòng chuẩn (Rounds 1 đến 9)**: **SubBytes → ShiftRows → MixColumns → AddRoundKey**.
4. **Vòng cuối (Final Round - Vòng 10)**: Bỏ qua MixColumns (chỉ gồm **SubBytes → ShiftRows → AddRoundKey**).

\---

## 1.3. VÍ DỤ CHẠY THỰC TẾ CHO MÃ HÓA AES

Thông số trích xuất trực tiếp từ file thực thi `aes\_rsa\_demo.py`:

* **Văn bản gốc (Plaintext)**: `Sinh vien: Tran Hoang Xuan Vu - MSSV: K235480106080 - Lop: K59KMT`
* **Bản mã AES thu được (Hex)**: `11106de1ca5032d79ccb50f3726a80f770cd1364b49c819df5c834e1a9bd...`
* **Thời gian mã hóa AES**: `0.2466 ms`
* **Thời gian giải mã AES**: `0.0245 ms`

### 📸 Ảnh minh chứng kết quả chạy chương trình demo:

!\[Python Demo Result](./images/01\_python\_demo.png)

\---

# 📌 MỤC 2. THUẬT TOÁN MÃ HÓA BẤT ĐỐI XỨNG RSA

## 2.1. Giới thiệu thuật toán RSA

RSA (Rivest–Shamir–Adleman) dựa trên tính chất toán học: **Phép nhân hai số nguyên tố lớn thì rất dễ, nhưng phân tích tích của chúng ra thừa số nguyên tố thì vô cùng khó**.

## 2.2. Quy trình sinh cặp khóa Bí mật (Private Key) và Công khai (Public Key)

1. **Chọn hai số nguyên tố lớn**: Chọn ngẫu nhiên **p** và **q** (với `p ≠ q`).
2. **Tính Modulo n**: **n = p × q** *(Độ dài bit của n chính là độ dài khóa RSA)*.
3. **Tính hàm số Euler ϕ(n)**: **ϕ(n) = (p - 1) × (q - 1)**
4. **Chọn Số mũ công khai e**: Chọn e sao cho **1 < e < ϕ(n)** và **gcd(e, ϕ(n)) = 1** *(thường chọn e = 65537)*.
5. **Tính Số mũ bí mật d**: Tìm d sao cho **(d × e) ≡ 1 (mod ϕ(n))**.

\---

## 2.3. VÍ DỤ SỐ BẰNG TÍNH TOÁN CỤ THỂ CHO RSA

Để minh họa nguyên lý RSA, ta thực hiện tính toán từng bước với hai số nguyên tố nhỏ **p = 7** và **q = 11**:

### Bước 1: Sinh bộ khóa (Key Generation)

1. **Tính n**: `n = p × q = 7 × 11 = 77`
2. **Tính hàm Euler ϕ(n)**: `ϕ(n) = (7 - 1) × (11 - 1) = 6 × 10 = 60`
3. **Chọn Số mũ công khai e**: Chọn `e = 13` (Thỏa mãn `1 < 13 < 60` và `gcd(13, 60) = 1`).
4. **Tính Số mũ bí mật d**:

   * Tìm d sao cho: `(d × 13) ≡ 1 (mod 60)`
   * Ta có: `37 × 13 = 481 = (8 × 60) + 1 ≡ 1 (mod 60)` → Suy ra **d = 37**.

> 🔑 \*\*Khóa công khai (Public Key)\*\*: `PU = {e, n} = {13, 77}`  
> 🗝️ \*\*Khóa bí mật (Private Key)\*\*: `PR = {d, n} = {37, 77}`

\---

### Bước 2: Quá trình Mã hóa \& Giải mã

* **Mã hóa (với M = 9)**: `C = 9¹³ mod 77 = 58`
* **Giải mã (với C = 58)**: `M = 58³⁷ mod 77 = 9` (Thu lại chính xác thông điệp gốc).

\---

# 📌 MỤC 3. CÁC MÔ HÌNH ÁP DỤNG RSA VÀ KẾT HỢP SỨC MẠNH RSA \& AES

## 3.1. Các mô hình áp dụng thuật toán RSA

### Mô hình 1: Bảo mật / Xác thực người nhận (Receiver Authentication)

* **Bên gửi (A)**: Dùng **Public Key của B (PU<sub>B</sub>)** để mã hóa: **C = M<sup>e<sub>B</sub></sup> mod n<sub>B</sub>**
* **Bên nhận (B)**: Dùng **Private Key của B (PR<sub>B</sub>)** để giải mã: **M = C<sup>d<sub>B</sub></sup> mod n<sub>B</sub>**
* **Ý nghĩa**: Đạt được tính **Bảo mật (Confidentiality)**.

### Mô hình 2: Xác thực người gửi / Chữ ký số (Sender Authentication)

* **Bên gửi (A)**: Dùng **Private Key của A (PR<sub>A</sub>)** để mã hóa/ký: **S = M<sup>d<sub>A</sub></sup> mod n<sub>A</sub>**
* **Bên nhận (B)**: Dùng **Public Key của A (PU<sub>A</sub>)** để giải mã/xác minh: **M = S<sup>e<sub>A</sub></sup> mod n<sub>A</sub>**
* **Ý nghĩa**: Đạt được tính **Xác thực người gửi** và **Chống chối bỏ**.

### Mô hình 3: Kết hợp cả Xác thực người gửi và Xác thực người nhận

* **Bên gửi (A)**: Ký bằng PR<sub>A</sub> trước, sau đó mã hóa tiếp bằng PU<sub>B</sub>.
* **Bên nhận (B)**: Giải mã bằng PR<sub>B</sub> trước, sau đó xác minh chữ ký bằng PU<sub>A</sub>.
* **Ý nghĩa**: Đạt được đồng thời cả **Tính bảo mật** lẫn **Tính xác thực nguồn gốc**.

\---

## 3.2. So sánh thời gian mã hóa / giải mã của RSA và AES

|Tiêu chí so sánh|Thuật toán đối xứng AES|Thuật toán bất đối xứng RSA|
|-|-|-|
|**Bản chất toán học**|Phép thế S-Box, dịch hàng, nhân ma trận Galois GF(2<sup>8</sup>).|Phép lũy thừa modulo trên các số nguyên rất lớn (2048 - 4096 bits).|
|**Tốc độ xử lý**|**Cực kỳ nhanh** (vài microsecond). Hỗ trợ phần cứng CPU AES-NI.|**Rất chậm** (chậm hơn AES từ **1.000 đến 10.000 lần**).|
|**Kích thước dữ liệu**|Không giới hạn (mã hóa tập tin gigabyte mượt mà).|Bị giới hạn (dữ liệu mã hóa phải nhỏ hơn độ dài khóa RSA).|
|**Quản lý khóa**|Khó phân phối khóa bí mật an toàn trên kênh truyền mở.|Dễ dàng chia sẻ Public Key công khai.|

\---

## 3.3. VÍ DỤ KẾT HỢP CHẠY THỰC TẾ MÃ HÓA LAI (HYBRID)

Kết quả thực thi mô hình Mã hóa lai (RSA-2048 + AES-128) trong ảnh minh chứng:

* **Khóa phiên AES ngẫu nhiên (128-bit Hex)**: `5e00be24d7298191e92b16c3f4d399fc`
* **Khóa AES giải mã bằng RSA Private Key**: `5e00be24d7298191e92b16c3f4d399fc`
* **Kiểm tra độ chính xác**: Khóa khớp 100% (`True`).

\---

# 📌 MỤC 4. THỰC NGHIỆM ĐÁNH GIÁ HIỆU NĂNG (BENCHMARK)

Để phân tích chuyên sâu hiệu năng giữa các giải pháp mã hóa, chương trình thực nghiệm `benchmark.py` được xây dựng để đo đạc thời gian xử lý thực tế trên các gói dữ liệu có dung lượng từ **64 Bytes** đến **1 MegaByte (1 MB)**.

### 📸 Ảnh chụp kết quả đo đạc thực nghiệm Terminal:

!\[Benchmark Results](./images/02\_benchmark\_results.png)

### 📊 Nhận xét \& Đánh giá kết quả thực nghiệm:

1. **Hạn chế kích thước của RSA**: Khi kích thước gói dữ liệu vượt quá **190 Bytes**, thuật toán mã hóa trực tiếp RSA-2048 bị lỗi ngay lập tức (`LỖI: >190B (Quá tải)`) vì vượt quá dung lượng khối tối đa cho phép của chuẩn padding PKCS1-OAEP.
2. **Ưu thế tuyệt đối của AES**: Tốc độ mã hóa AES vô cùng nhanh và tăng trưởng tuyến tính theo dung lượng dữ liệu (mã hóa file 1MB chỉ mất vài milisecond).
3. **Hiệu quả của Mã hóa lai (Hybrid)**: Vừa giải quyết triệt để bài toán giới hạn dung lượng của RSA, vừa giữ được tốc độ xử lý nhanh xấp xỉ AES thuần túy, đồng thời đảm bảo an toàn tuyệt đối cho việc phân phối khóa qua kênh truyền công khai.

\---

\---

# 📌 MỤC 5. LÝ THUYẾT VÀ KIẾN TRÚC PHÁT TRIỂN WEB DASHBOARD

\## 5.1. Kiến trúc hệ thống (System Architecture)

Ứng dụng được thiết kế theo mô hình \*\*Client-Server\*\* kết hợp kiến trúc \*\*RESTful API\*\*:

\* \*\*Backend Framework\*\*: Sử dụng \*\*Python Flask\*\* đóng vai trò xử lý logic trung tâm, tiếp nhận các HTTP Request và trực tiếp gọi các thư viện mã hóa `PyCryptodome` trong bộ nhớ RAM.

\* \*\*Frontend Interface\*\*: Xây dựng bằng \*\*HTML5\*\*, \*\*Tailwind CSS\*\* (Giao diện Cyberpunk Dark Mode) và \*\*JavaScript (Fetch API)\*\* giúp gửi/nhận dữ liệu bất đồng bộ (AJAX) không cần tải lại trang.



\## 5.2. Danh sách API Endpoints và Cơ chế xử lý



| Endpoint | Phương thức | Chức năng | Quy trình xử lý tại Backend |

| :--- | :--- | :--- | :--- |

| `/api/aes/encrypt` | `POST` | Mã hóa AES-128 | Nhận Plaintext \& Key $\\rightarrow$ PKCS7 Padding $\\rightarrow$ AES-CBC Encrypt $\\rightarrow$ Trả về Hex \& Thời gian ($ms$) |

| `/api/aes/decrypt` | `POST` | Giải mã AES-128 | Nhận Ciphertext (Hex) \& Key $\\rightarrow$ AES-CBC Decrypt $\\rightarrow$ Unpadding $\\rightarrow$ Trả về Plaintext |

| `/api/rsa/generate`| `GET` | Sinh cặp khóa RSA | Khởi tạo ngẫu nhiên cặp khóa RSA 2048-bit lưu trữ tạm thời trong bộ nhớ RAM |

| `/api/rsa/encrypt` | `POST` | Mã hóa RSA | Mã hóa dữ liệu đầu vào bằng Public Key theo chuẩn padding PKCS1-OAEP |

| `/api/rsa/decrypt` | `POST` | Giải mã RSA | Giải mã bản mã Hex đầu vào bằng Private Key theo chuẩn PKCS1-OAEP |

| `/api/hybrid/encrypt`| `POST` | Mã hóa Lai (Hybrid)| Sinh khóa phiên AES 128-bit ngẫu nhiên $\\rightarrow$ Mã hóa Data bằng AES $\\rightarrow$ Mã hóa Khóa phiên bằng RSA Public Key |



\## 5.3. Luồng xử lý dữ liệu và Đo đạc hiệu năng

1\. \*\*Client-side\*\*: Người dùng nhập dữ liệu trên giao diện $\\rightarrow$ JavaScript bắt sự kiện click $\\rightarrow$ Đóng gói JSON gửi tới API tương ứng.

2\. \*\*Server-side\*\*: 

&#x20;  \* Đánh dấu thời gian bắt đầu xử lý $t\_0 = \\text{time.perf\\\_counter()}$.

&#x20;  \* Thực thi thuật toán mã hóa/giải mã trong RAM.

&#x20;  \* Tính toán thời gian phản hồi: $\\Delta t = (t\_{end} - t\_0) \\times 1000 \\quad (ms)$.

3\. \*\*Response\*\*: Flask trả về kết quả định dạng JSON gồm bản mã Hex và tham số thời gian $\\Delta t$ để hiển thị trực quan lên UI.

