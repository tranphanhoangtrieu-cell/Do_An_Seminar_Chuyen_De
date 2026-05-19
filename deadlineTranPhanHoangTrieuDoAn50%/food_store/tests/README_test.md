# Hướng dẫn Chạy Kiểm thử Selenium — FreshMart

## Yêu cầu cài đặt

```bash
pip install selenium pytest
```

Ngoài ra cần tải **ChromeDriver** đúng phiên bản với Chrome đang dùng:
- Kiểm tra phiên bản Chrome: `chrome://settings/help`
- Tải ChromeDriver: https://chromedriver.chromium.org/downloads

Sau khi tải, đặt `chromedriver.exe` vào thư mục đã có trong `PATH` hệ thống
(ví dụ: `C:\Windows\System32\`) hoặc cùng thư mục với file test.

---

## Bước chuẩn bị

### 1. Tạo database và seed dữ liệu mẫu
```bash
cd food_store
python seed_data.py
```
Lệnh này tạo:
- Tài khoản Admin: `admin / admin123`
- Tài khoản User: `nguyen_van_a / user123`
- 8 danh mục + 40 sản phẩm + đơn hàng mẫu

### 2. Khởi động Flask App
```bash
python app.py
```
Đảm bảo app đang chạy tại `http://127.0.0.1:5000` trước khi chạy test.

---

## Cách chạy test

### Chạy toàn bộ test Selenium
```bash
cd food_store
pytest tests/test_selenium.py -v
```

### Chạy với báo cáo HTML (khuyến nghị)
```bash
pip install pytest-html
pytest tests/test_selenium.py -v --html=tests/report.html --self-contained-html
```

### Chạy ở chế độ Headless (không hiện cửa sổ Chrome)
```bash
pytest tests/test_selenium.py -v --headless
```

### Chạy từng nhóm test
```bash
# Chỉ test xác thực
pytest tests/test_selenium.py -v -k "TestAuthentication"

# Chỉ test Admin
pytest tests/test_selenium.py -v -k "TestAdminPanel"

# Chỉ test bảo mật
pytest tests/test_selenium.py -v -k "TestSecurity"

# Chỉ test gợi ý
pytest tests/test_selenium.py -v -k "TestRecommendation"

# Chỉ test giỏ hàng
pytest tests/test_selenium.py -v -k "TestCart"

# Chỉ test thanh toán
pytest tests/test_selenium.py -v -k "TestCheckout"
```

### Chạy test theo tên cụ thể
```bash
pytest tests/test_selenium.py -v -k "test_login_success_admin"
```

### Chạy với base URL khác (ví dụ port khác)
```bash
pytest tests/test_selenium.py -v --base-url=http://127.0.0.1:8080
```

---

## Cấu trúc test

```
tests/
├── conftest.py          # Cấu hình fixtures và markers cho pytest
├── test_selenium.py     # File test chính (10 nhóm, 50+ ca test)
└── README_test.md       # File này
```

### Danh sách 10 nhóm kiểm thử

| Nhóm | Class | Số ca | Mô tả |
|---|---|---|---|
| 1 | `TestHomePage` | 5 ca | Trang chủ và điều hướng |
| 2 | `TestAuthentication` | 12 ca | Đăng ký, đăng nhập, đăng xuất |
| 3 | `TestShopAndProduct` | 8 ca | Cửa hàng, tìm kiếm, lọc, chi tiết SP |
| 4 | `TestCart` | 5 ca | Thêm, cập nhật, xóa giỏ hàng |
| 5 | `TestCheckout` | 4 ca | Luồng thanh toán |
| 6 | `TestOrderHistory` | 3 ca | Lịch sử đơn hàng |
| 7 | `TestRecommendation` | 5 ca | Hệ thống gợi ý Hybrid |
| 8 | `TestAdminPanel` | 10 ca | Dashboard, CRUD sản phẩm, đơn hàng |
| 9 | `TestSecurity` | 5 ca | XSS, SQL Injection, phân quyền |
| 10 | `TestPagination` | 3 ca | Phân trang sản phẩm và admin |

---

## Tài khoản dùng trong test

| Vai trò | Username | Password |
|---|---|---|
| Admin | `admin` | `admin123` |
| User thường | `nguyen_van_a` | `user123` |
| User Selenium (tự tạo) | `selenium_test_user` | `testpass123` |

> **Lưu ý:** Tài khoản `selenium_test_user` được tạo tự động trong test `TC-SEL-AUTH-02`.
> Nếu chạy lại test nhiều lần, test đăng ký có thể bị FAIL vì username đã tồn tại.
> Cách xử lý: Chạy lại `seed_data.py` để reset database, hoặc đổi `REG_USER` và `REG_EMAIL`
> trong file `test_selenium.py` thành giá trị khác.

---

## Xử lý lỗi thường gặp

### ChromeDriver version mismatch
```
SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version XX
```
**Giải quyết:** Tải đúng ChromeDriver khớp phiên bản Chrome đang dùng.

### Flask app chưa khởi động
```
ConnectionRefusedError: [WinError 10061]
```
**Giải quyết:** Chạy `python app.py` trước rồi mới chạy test.

### Test đăng ký bị FAIL do username đã tồn tại
**Giải quyết:** Chạy `python seed_data.py` để reset DB, hoặc sửa `REG_USER` trong test.

### Selenium không tìm thấy element
```
NoSuchElementException hoặc TimeoutException
```
**Giải quyết:** Tăng `WAIT_TIMEOUT` lên 15-20 giây nếu máy chạy chậm.
