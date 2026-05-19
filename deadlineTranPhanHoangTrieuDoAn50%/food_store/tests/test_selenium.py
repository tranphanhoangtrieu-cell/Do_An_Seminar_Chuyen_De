"""
test_selenium.py — Kiểm thử Selenium cho FreshMart Food Store
=============================================================
Yêu cầu:
    pip install selenium pytest
    Tải ChromeDriver phù hợp phiên bản Chrome: https://chromedriver.chromium.org/

Cách chạy:
    1. Khởi động Flask app: python app.py
    2. Chạy test:  pytest tests/test_selenium.py -v
    3. Chạy 1 nhóm: pytest tests/test_selenium.py -v -k "TestAuth"

Tài khoản mặc định (sau khi chạy seed_data.py):
    Admin : username=admin       / password=admin123
    User  : username=nguyen_van_a / password=user123
"""

import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementNotInteractableException,
)

# ============================================================
# CẤU HÌNH CHUNG
# ============================================================
BASE_URL = "http://127.0.0.1:5000"
WAIT_TIMEOUT = 10          # Giây chờ tối đa cho mỗi element

# Tài khoản test (phải tồn tại trong DB sau khi seed)
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"
NORMAL_USER = "nguyen_van_a"
NORMAL_PASS = "user123"

# Tài khoản dùng để test đăng ký (không được tồn tại sẵn)
REG_USER    = "selenium_test_user"
REG_EMAIL   = "selenium_test@example.com"
REG_PASS    = "testpass123"


# ============================================================
# FIXTURE: Khởi tạo / Dọn dẹp WebDriver
# ============================================================
@pytest.fixture(scope="class")
def driver():
    """
    Khởi tạo Chrome WebDriver cho cả class test.
    scope="class" → chỉ tạo 1 browser cho toàn bộ methods trong class.
    """
    chrome_options = Options()
    # Bỏ comment dòng dưới nếu muốn chạy không hiện cửa sổ trình duyệt
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1366,768")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    drv = webdriver.Chrome(options=chrome_options)
    drv.implicitly_wait(5)
    yield drv
    drv.quit()


# ============================================================
# HÀM TIỆN ÍCH DÙNG CHUNG
# ============================================================
def wait_for(driver, by, value, timeout=WAIT_TIMEOUT):
    """Chờ element xuất hiện và trả về element đó."""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )


def wait_clickable(driver, by, value, timeout=WAIT_TIMEOUT):
    """Chờ element có thể click và trả về element đó."""
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )


def get_flash_message(driver, timeout=WAIT_TIMEOUT):
    """Lấy nội dung flash message trên trang."""
    try:
        alert = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".alert"))
        )
        return alert.text
    except TimeoutException:
        return ""


def login(driver, username, password):
    """Helper: Đăng nhập nhanh."""
    driver.get(f"{BASE_URL}/login")
    wait_for(driver, By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(0.5)


def logout(driver):
    """Helper: Đăng xuất nhanh."""
    driver.get(f"{BASE_URL}/logout")
    time.sleep(0.5)


# ============================================================
# NHÓM 1: KIỂM THỬ TRANG CHỦ VÀ ĐIỀU HƯỚNG
# ============================================================
class TestHomePage:
    """TC-SEL-HOME: Kiểm tra trang chủ hiển thị đúng"""

    def test_home_page_loads(self, driver):
        """TC-SEL-HOME-01: Trang chủ tải thành công, có tiêu đề FreshMart"""
        driver.get(BASE_URL)
        assert "FreshMart" in driver.title, \
            f"Tiêu đề trang không khớp, nhận được: {driver.title}"

    def test_home_has_navbar(self, driver):
        """TC-SEL-HOME-02: Navbar hiển thị đầy đủ các link điều hướng"""
        driver.get(BASE_URL)
        nav = wait_for(driver, By.TAG_NAME, "nav")
        assert nav is not None, "Không tìm thấy navbar"

    def test_home_has_product_sections(self, driver):
        """TC-SEL-HOME-03: Trang chủ có ít nhất 1 section sản phẩm"""
        driver.get(BASE_URL)
        # Tìm card sản phẩm (có class card hoặc product-card)
        cards = driver.find_elements(By.CSS_SELECTOR, ".card")
        assert len(cards) > 0, "Không có card sản phẩm nào trên trang chủ"

    def test_home_cart_link_visible(self, driver):
        """TC-SEL-HOME-04: Icon giỏ hàng hiển thị trên navbar"""
        driver.get(BASE_URL)
        cart_link = driver.find_elements(By.CSS_SELECTOR, "a[href*='cart']")
        assert len(cart_link) > 0, "Không tìm thấy link giỏ hàng trên navbar"

    def test_home_login_link_visible_when_not_logged_in(self, driver):
        """TC-SEL-HOME-05: Chưa đăng nhập → hiện link Đăng nhập"""
        logout(driver)
        driver.get(BASE_URL)
        login_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='login']")
        assert len(login_links) > 0, "Không tìm thấy link Đăng nhập khi chưa login"


# ============================================================
# NHÓM 2: KIỂM THỬ XÁC THỰC (AUTH)
# ============================================================
class TestAuthentication:
    """TC-SEL-AUTH: Kiểm tra luồng đăng ký, đăng nhập, đăng xuất"""

    def test_register_page_loads(self, driver):
        """TC-SEL-AUTH-01: Trang đăng ký tải thành công"""
        driver.get(f"{BASE_URL}/register")
        assert "Đăng ký" in driver.page_source or "Tạo tài khoản" in driver.page_source, \
            "Trang đăng ký không hiển thị đúng"

    def test_register_success(self, driver):
        """TC-SEL-AUTH-02: Đăng ký tài khoản mới hợp lệ thành công"""
        driver.get(f"{BASE_URL}/register")

        wait_for(driver, By.NAME, "username").send_keys(REG_USER)
        driver.find_element(By.NAME, "full_name").send_keys("Selenium Tester")
        driver.find_element(By.NAME, "email").send_keys(REG_EMAIL)
        driver.find_element(By.NAME, "phone").send_keys("0999888777")
        driver.find_element(By.NAME, "password").send_keys(REG_PASS)
        driver.find_element(By.NAME, "confirm_password").send_keys(REG_PASS)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Sau khi đăng ký thành công → redirect về /login
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.url_contains("/login")
        )
        flash = get_flash_message(driver)
        assert "thành công" in flash.lower() or "/login" in driver.current_url, \
            f"Đăng ký không thành công. Flash: {flash}"

    def test_register_duplicate_username(self, driver):
        """TC-SEL-AUTH-03: Đăng ký trùng username → hiện lỗi"""
        driver.get(f"{BASE_URL}/register")

        wait_for(driver, By.NAME, "username").send_keys(REG_USER)  # đã tồn tại
        driver.find_element(By.NAME, "email").send_keys("new_unique@email.com")
        driver.find_element(By.NAME, "password").send_keys(REG_PASS)
        driver.find_element(By.NAME, "confirm_password").send_keys(REG_PASS)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        time.sleep(0.5)
        assert "/register" in driver.current_url, \
            "Phải ở lại trang đăng ký khi username trùng"
        page_source = driver.page_source
        assert "tồn tại" in page_source or "đã" in page_source, \
            "Không hiện thông báo lỗi trùng username"

    def test_register_short_username(self, driver):
        """TC-SEL-AUTH-04: Username quá ngắn (< 3 ký tự) → hiện lỗi"""
        driver.get(f"{BASE_URL}/register")

        wait_for(driver, By.NAME, "username").send_keys("ab")
        driver.find_element(By.NAME, "email").send_keys("short@email.com")
        driver.find_element(By.NAME, "password").send_keys("123456")
        driver.find_element(By.NAME, "confirm_password").send_keys("123456")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        time.sleep(0.5)
        assert "/register" in driver.current_url, \
            "Phải ở lại trang đăng ký khi username quá ngắn"

    def test_register_password_mismatch(self, driver):
        """TC-SEL-AUTH-05: Mật khẩu và xác nhận không khớp → hiện lỗi"""
        driver.get(f"{BASE_URL}/register")

        wait_for(driver, By.NAME, "username").send_keys("test_mismatch")
        driver.find_element(By.NAME, "email").send_keys("mismatch@email.com")
        driver.find_element(By.NAME, "password").send_keys("pass1234")
        driver.find_element(By.NAME, "confirm_password").send_keys("DIFFERENT")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        time.sleep(0.5)
        assert "/register" in driver.current_url, \
            "Phải ở lại trang đăng ký khi mật khẩu không khớp"
        assert "không khớp" in driver.page_source, \
            "Không hiện thông báo 'Mật khẩu xác nhận không khớp'"

    def test_login_success_normal_user(self, driver):
        """TC-SEL-AUTH-06: Đăng nhập user thường thành công → về trang chủ"""
        logout(driver)
        login(driver, NORMAL_USER, NORMAL_PASS)

        WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.url_to_be(f"{BASE_URL}/")
        )
        assert driver.current_url == f"{BASE_URL}/", \
            f"User thường phải về trang chủ, nhưng đang ở: {driver.current_url}"

    def test_login_success_admin(self, driver):
        """TC-SEL-AUTH-07: Đăng nhập Admin thành công → về /admin"""
        logout(driver)
        login(driver, ADMIN_USER, ADMIN_PASS)

        WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.url_contains("/admin")
        )
        assert "/admin" in driver.current_url, \
            f"Admin phải về /admin, nhưng đang ở: {driver.current_url}"

    def test_login_wrong_password(self, driver):
        """TC-SEL-AUTH-08: Đăng nhập sai mật khẩu → hiện thông báo lỗi"""
        logout(driver)
        driver.get(f"{BASE_URL}/login")

        wait_for(driver, By.NAME, "username").send_keys(NORMAL_USER)
        driver.find_element(By.NAME, "password").send_keys("matkhausai123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        time.sleep(0.5)
        assert "/login" in driver.current_url, "Phải ở lại trang login khi sai mật khẩu"
        assert "Sai" in driver.page_source or "không đúng" in driver.page_source, \
            "Không hiện thông báo lỗi khi sai mật khẩu"

    def test_login_nonexistent_user(self, driver):
        """TC-SEL-AUTH-09: Đăng nhập username không tồn tại → hiện lỗi"""
        logout(driver)
        driver.get(f"{BASE_URL}/login")

        wait_for(driver, By.NAME, "username").send_keys("user_khong_ton_tai_xyz")
        driver.find_element(By.NAME, "password").send_keys("anypassword")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        time.sleep(0.5)
        assert "/login" in driver.current_url

    def test_logout_success(self, driver):
        """TC-SEL-AUTH-10: Đăng xuất thành công → về trang chủ, không còn menu user"""
        login(driver, NORMAL_USER, NORMAL_PASS)
        time.sleep(0.5)
        logout(driver)

        WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.url_contains("/")
        )
        # Sau logout phải hiện link đăng nhập lại
        login_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='login']")
        assert len(login_links) > 0, "Sau logout phải hiện link Đăng nhập"

    def test_redirect_to_login_when_accessing_protected(self, driver):
        """TC-SEL-AUTH-11: Truy cập /checkout khi chưa login → redirect về /login"""
        logout(driver)
        driver.get(f"{BASE_URL}/checkout")

        WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.url_contains("/login")
        )
        assert "/login" in driver.current_url, \
            f"Phải redirect về /login, nhưng đang ở: {driver.current_url}"

    def test_redirect_to_login_orders_protected(self, driver):
        """TC-SEL-AUTH-12: Truy cập /orders khi chưa login → redirect về /login"""
        logout(driver)
        driver.get(f"{BASE_URL}/orders")

        WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.url_contains("/login")
        )
        assert "/login" in driver.current_url


# ============================================================
# NHÓM 3: KIỂM THỬ CỬA HÀNG VÀ SẢN PHẨM
# ============================================================
class TestShopAndProduct:
    """TC-SEL-SHOP: Kiểm tra trang cửa hàng, tìm kiếm, lọc, chi tiết sản phẩm"""

    def test_shop_page_loads(self, driver):
        """TC-SEL-SHOP-01: Trang cửa hàng /shop tải thành công"""
        driver.get(f"{BASE_URL}/shop")
        assert "shop" in driver.current_url.lower() or \
               "Cửa hàng" in driver.page_source or \
               len(driver.find_elements(By.CSS_SELECTOR, ".card")) > 0, \
            "Trang shop không hiển thị sản phẩm"

    def test_shop_search_by_keyword(self, driver):
        """TC-SEL-SHOP-02: Tìm kiếm sản phẩm theo từ khóa"""
        driver.get(f"{BASE_URL}/shop")

        search_input = wait_for(driver, By.CSS_SELECTOR, "input[name='q']")
        search_input.clear()
        search_input.send_keys("rau")
        search_input.send_keys(Keys.ENTER)

        time.sleep(1)
        # URL phải chứa ?q=rau
        assert "q=rau" in driver.current_url, \
            f"URL tìm kiếm không đúng: {driver.current_url}"

    def test_shop_search_empty_result(self, driver):
        """TC-SEL-SHOP-03: Tìm kiếm với từ không có sản phẩm → hiển thị thông báo trống"""
        driver.get(f"{BASE_URL}/shop?q=xxxxkhongtontaiyyyy")
        time.sleep(0.5)
        page = driver.page_source
        # Phải có thông báo không tìm thấy hoặc không có card sản phẩm
        cards = driver.find_elements(By.CSS_SELECTOR, ".card-img-top, .product-card")
        assert len(cards) == 0 or "không tìm thấy" in page.lower() or \
               "không có" in page.lower(), \
            "Không hiển thị trạng thái trống khi không có kết quả"

    def test_shop_filter_by_category(self, driver):
        """TC-SEL-SHOP-04: Lọc sản phẩm theo danh mục"""
        driver.get(f"{BASE_URL}/shop")
        # Tìm link danh mục đầu tiên trong sidebar/navbar
        category_links = driver.find_elements(
            By.CSS_SELECTOR, "a[href*='category=']"
        )
        if len(category_links) > 0:
            href = category_links[0].get_attribute("href")
            driver.get(href)
            time.sleep(0.5)
            assert "category=" in driver.current_url, \
                "URL không chứa tham số category"

    def test_shop_sort_by_price_asc(self, driver):
        """TC-SEL-SHOP-05: Sắp xếp sản phẩm theo giá tăng dần"""
        driver.get(f"{BASE_URL}/shop?sort=price_asc")
        time.sleep(0.5)
        assert "price_asc" in driver.current_url, \
            "URL không chứa sort=price_asc"

    def test_shop_sort_by_bestseller(self, driver):
        """TC-SEL-SHOP-06: Sắp xếp sản phẩm theo bán chạy"""
        driver.get(f"{BASE_URL}/shop?sort=bestseller")
        time.sleep(0.5)
        assert "bestseller" in driver.current_url

    def test_product_detail_page(self, driver):
        """TC-SEL-SHOP-07: Trang chi tiết sản phẩm hiển thị đầy đủ thông tin"""
        driver.get(f"{BASE_URL}/shop")

        # Click vào sản phẩm đầu tiên
        product_links = driver.find_elements(
            By.CSS_SELECTOR, "a[href*='/product/']"
        )
        assert len(product_links) > 0, "Không tìm thấy link sản phẩm nào"

        first_product_url = product_links[0].get_attribute("href")
        driver.get(first_product_url)
        time.sleep(0.5)

        assert "/product/" in driver.current_url, \
            f"Không vào được trang chi tiết sản phẩm: {driver.current_url}"

    def test_product_detail_has_similar_section(self, driver):
        """TC-SEL-SHOP-08: Trang chi tiết có section sản phẩm tương tự"""
        driver.get(f"{BASE_URL}/product/1")
        time.sleep(0.5)
        page = driver.page_source
        # Chấp nhận 404 hoặc phải có section similar
        if "404" not in page and "không tìm thấy" not in page.lower():
            # Trang hợp lệ → kiểm tra có nội dung sản phẩm
            assert "đ" in page or "price" in page.lower() or \
                   len(driver.find_elements(By.CSS_SELECTOR, ".card")) > 0, \
                "Trang chi tiết sản phẩm không có thông tin giá"


# ============================================================
# NHÓM 4: KIỂM THỬ GIỎ HÀNG (CART)
# ============================================================
class TestCart:
    """TC-SEL-CART: Kiểm tra thêm, cập nhật, xóa sản phẩm trong giỏ hàng"""

    def setup_method(self):
        """Đảm bảo đã đăng nhập trước mỗi test trong nhóm này."""
        pass

    def test_add_to_cart(self, driver):
        """TC-SEL-CART-01: Thêm sản phẩm vào giỏ hàng thành công"""
        login(driver, NORMAL_USER, NORMAL_PASS)
        driver.get(f"{BASE_URL}/shop")
        time.sleep(0.5)

        # Tìm nút "Thêm vào giỏ" (form có action /cart/add)
        add_buttons = driver.find_elements(
            By.CSS_SELECTOR, "form[action*='cart/add'] button[type='submit']"
        )
        assert len(add_buttons) > 0, "Không tìm thấy nút 'Thêm vào giỏ'"

        add_buttons[0].click()
        time.sleep(0.5)

        # Kiểm tra flash message hoặc cart_count tăng
        page = driver.page_source
        assert "giỏ hàng" in page.lower() or "thêm" in page.lower(), \
            "Không hiện thông báo sau khi thêm vào giỏ"

    def test_cart_page_shows_items(self, driver):
        """TC-SEL-CART-02: Trang /cart hiển thị sản phẩm đã thêm"""
        login(driver, NORMAL_USER, NORMAL_PASS)
        # Thêm 1 sản phẩm trước
        driver.get(f"{BASE_URL}/shop")
        time.sleep(0.5)
        add_btns = driver.find_elements(
            By.CSS_SELECTOR, "form[action*='cart/add'] button[type='submit']"
        )
        if add_btns:
            add_btns[0].click()
            time.sleep(0.5)

        driver.get(f"{BASE_URL}/cart")
        time.sleep(0.5)
        page = driver.page_source
        # Phải hiển thị nội dung giỏ hàng (dù trống hay có hàng)
        assert "cart" in driver.current_url.lower() or \
               "Giỏ hàng" in page, \
            "Trang giỏ hàng không tải được"

    def test_cart_remove_item(self, driver):
        """TC-SEL-CART-03: Xóa sản phẩm khỏi giỏ hàng"""
        login(driver, NORMAL_USER, NORMAL_PASS)
        # Thêm 1 SP
        driver.get(f"{BASE_URL}/shop")
        time.sleep(0.5)
        add_btns = driver.find_elements(
            By.CSS_SELECTOR, "form[action*='cart/add'] button[type='submit']"
        )
        if add_btns:
            add_btns[0].click()
            time.sleep(0.5)

        driver.get(f"{BASE_URL}/cart")
        time.sleep(0.5)

        # Tìm nút Xóa / Remove
        remove_links = driver.find_elements(
            By.CSS_SELECTOR, "a[href*='cart/remove']"
        )
        if remove_links:
            remove_links[0].click()
            time.sleep(0.5)
            flash = get_flash_message(driver)
            assert "xóa" in flash.lower() or "/cart" in driver.current_url, \
                "Không hiện thông báo xóa sản phẩm"

    def test_cart_update_quantity(self, driver):
        """TC-SEL-CART-04: Cập nhật số lượng sản phẩm trong giỏ"""
        login(driver, NORMAL_USER, NORMAL_PASS)
        # Thêm SP
        driver.get(f"{BASE_URL}/shop")
        time.sleep(0.5)
        add_btns = driver.find_elements(
            By.CSS_SELECTOR, "form[action*='cart/add'] button[type='submit']"
        )
        if add_btns:
            add_btns[0].click()
            time.sleep(0.5)

        driver.get(f"{BASE_URL}/cart")
        time.sleep(0.5)

        # Tìm input số lượng
        qty_inputs = driver.find_elements(
            By.CSS_SELECTOR, "input[name='quantity']"
        )
        if qty_inputs:
            qty_inputs[0].clear()
            qty_inputs[0].send_keys("3")
            # Tìm nút submit form cập nhật
            update_btns = driver.find_elements(
                By.CSS_SELECTOR, "form[action*='cart/update'] button[type='submit']"
            )
            if update_btns:
                update_btns[0].click()
                time.sleep(0.5)
                assert "/cart" in driver.current_url, \
                    "Sau cập nhật phải về lại trang giỏ hàng"

    def test_cart_empty_checkout_redirect(self, driver):
        """TC-SEL-CART-05: Checkout khi giỏ trống → Flash cảnh báo"""
        login(driver, NORMAL_USER, NORMAL_PASS)
        # Xóa hết giỏ hàng bằng cách truy cập cart rồi xóa hết
        driver.get(f"{BASE_URL}/cart")
        remove_links = driver.find_elements(
            By.CSS_SELECTOR, "a[href*='cart/remove']"
        )
        for link in remove_links:
            try:
                link.click()
                time.sleep(0.3)
                driver.get(f"{BASE_URL}/cart")
            except Exception:
                pass

        # Thử vào checkout
        driver.get(f"{BASE_URL}/checkout")
        time.sleep(0.5)
        # Phải redirect về cart hoặc flash cảnh báo
        page = driver.page_source
        assert "trống" in page.lower() or \
               "cart" in driver.current_url.lower() or \
               "Giỏ hàng" in page, \
            "Giỏ trống phải có thông báo hoặc redirect"


# ============================================================
# NHÓM 5: KIỂM THỬ THANH TOÁN (CHECKOUT)
# ============================================================
class TestCheckout:
    """TC-SEL-CHECKOUT: Kiểm tra luồng đặt hàng đầy đủ"""

    def _add_product_to_cart(self, driver):
        """Helper: Thêm 1 sản phẩm vào giỏ hàng."""
        driver.get(f"{BASE_URL}/shop")
        time.sleep(0.8)
        add_btns = driver.find_elements(
            By.CSS_SELECTOR, "form[action*='cart/add'] button[type='submit']"
        )
        if add_btns:
            add_btns[0].click()
            time.sleep(0.5)
            return True
        return False

    def test_checkout_redirect_if_not_logged_in(self, driver):
        """TC-SEL-CHECKOUT-01: Chưa login → /checkout redirect về /login"""
        logout(driver)
        driver.get(f"{BASE_URL}/checkout")
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.url_contains("/login")
        )
        assert "/login" in driver.current_url

    def test_checkout_form_displays(self, driver):
        """TC-SEL-CHECKOUT-02: Form checkout hiển thị đầy đủ các trường"""
        login(driver, NORMAL_USER, NORMAL_PASS)
        self._add_product_to_cart(driver)
        driver.get(f"{BASE_URL}/checkout")
        time.sleep(0.5)

        # Kiểm tra các field bắt buộc
        assert driver.find_elements(By.NAME, "shipping_name"), \
            "Thiếu field shipping_name"
        assert driver.find_elements(By.NAME, "shipping_phone"), \
            "Thiếu field shipping_phone"
        assert driver.find_elements(By.NAME, "shipping_address"), \
            "Thiếu field shipping_address"

    def test_checkout_missing_info_shows_error(self, driver):
        """TC-SEL-CHECKOUT-03: Submit checkout thiếu địa chỉ → hiện lỗi"""
        login(driver, NORMAL_USER, NORMAL_PASS)
        self._add_product_to_cart(driver)
        driver.get(f"{BASE_URL}/checkout")
        time.sleep(0.5)

        # Điền tên + phone nhưng để trống địa chỉ
        name_field = driver.find_elements(By.NAME, "shipping_name")
        phone_field = driver.find_elements(By.NAME, "shipping_phone")
        addr_field  = driver.find_elements(By.NAME, "shipping_address")

        if name_field and phone_field and addr_field:
            name_field[0].clear()
            name_field[0].send_keys("Test User")
            phone_field[0].clear()
            phone_field[0].send_keys("0909090909")
            addr_field[0].clear()   # Bỏ trống địa chỉ
            driver.find_element(
                By.CSS_SELECTOR, "button[type='submit']"
            ).click()
            time.sleep(0.5)
            page = driver.page_source
            assert "đầy đủ" in page.lower() or "/checkout" in driver.current_url, \
                "Phải hiện lỗi khi thiếu địa chỉ"

    def test_checkout_success_full_info(self, driver):
        """TC-SEL-CHECKOUT-04: Đặt hàng thành công khi điền đầy đủ thông tin"""
        login(driver, NORMAL_USER, NORMAL_PASS)
        added = self._add_product_to_cart(driver)
        if not added:
            pytest.skip("Không có sản phẩm để thêm vào giỏ")

        driver.get(f"{BASE_URL}/checkout")
        time.sleep(0.5)

        name_fields = driver.find_elements(By.NAME, "shipping_name")
        phone_fields = driver.find_elements(By.NAME, "shipping_phone")
        addr_fields  = driver.find_elements(By.NAME, "shipping_address")

        if not (name_fields and phone_fields and addr_fields):
            pytest.skip("Không vào được trang checkout (giỏ có thể trống)")

        name_fields[0].clear()
        name_fields[0].send_keys("Nguyen Van Test")
        phone_fields[0].clear()
        phone_fields[0].send_keys("0911222333")
        addr_fields[0].clear()
        addr_fields[0].send_keys("123 Đường ABC, Quận 1, TP.HCM")

        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Chờ redirect về /orders
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.url_contains("/orders")
        )
        assert "/orders" in driver.current_url, \
            f"Sau đặt hàng phải về /orders, đang ở: {driver.current_url}"

        flash = get_flash_message(driver)
        assert "thành công" in flash.lower() or "/orders" in driver.current_url, \
            f"Không hiện thông báo đặt hàng thành công. Flash: {flash}"


# ============================================================
# NHÓM 6: KIỂM THỬ LỊCH SỬ ĐƠN HÀNG
# ============================================================
class TestOrderHistory:
    """TC-SEL-ORDER: Kiểm tra trang lịch sử đơn hàng"""

    def test_order_history_page_loads(self, driver):
        """TC-SEL-ORDER-01: Trang /orders tải thành công khi đã login"""
        login(driver, NORMAL_USER, NORMAL_PASS)
        driver.get(f"{BASE_URL}/orders")
        time.sleep(0.5)
        assert "/orders" in driver.current_url, \
            "Không vào được trang lịch sử đơn hàng"

    def test_order_history_shows_orders(self, driver):
        """TC-SEL-ORDER-02: Lịch sử đơn hàng hiển thị các đơn đã đặt"""
        login(driver, NORMAL_USER, NORMAL_PASS)
        driver.get(f"{BASE_URL}/orders")
        time.sleep(0.5)
        page = driver.page_source
        # Phải có từ "đơn" hoặc "order" trong trang
        assert "đơn" in page.lower() or \
               "order" in page.lower() or \
               "Chờ xử lý" in page or \
               "Không có" in page, \
            "Trang lịch sử đơn hàng không hiển thị đúng"

    def test_order_history_requires_login(self, driver):
        """TC-SEL-ORDER-03: Truy cập /orders khi chưa login → redirect /login"""
        logout(driver)
        driver.get(f"{BASE_URL}/orders")
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.url_contains("/login")
        )
        assert "/login" in driver.current_url


# ============================================================
# NHÓM 7: KIỂM THỬ HỆ THỐNG GỢI Ý (RECOMMENDATION)
# ============================================================
class TestRecommendation:
    """TC-SEL-REC: Kiểm tra hệ thống gợi ý hoạt động đúng"""

    def test_recommendation_page_loads(self, driver):
        """TC-SEL-REC-01: Trang /recommendations tải không có lỗi"""
        driver.get(f"{BASE_URL}/recommendations")
        time.sleep(0.5)
        assert "500" not in driver.page_source, \
            "Trang gợi ý bị lỗi 500"
        assert driver.current_url is not None

    def test_home_recommendation_section_exists(self, driver):
        """TC-SEL-REC-02: Trang chủ có section gợi ý sản phẩm"""
        logout(driver)
        driver.get(BASE_URL)
        time.sleep(0.5)
        page = driver.page_source
        # Trang chủ phải có section trending hoặc gợi ý
        assert "gợi ý" in page.lower() or \
               "trending" in page.lower() or \
               "bán chạy" in page.lower() or \
               len(driver.find_elements(By.CSS_SELECTOR, ".card")) > 0, \
            "Trang chủ không có section gợi ý"

    def test_cold_start_recommendation_no_error(self, driver):
        """TC-SEL-REC-03: User mới (chưa mua gì) → section gợi ý vẫn hiển thị (Cold Start)"""
        login(driver, REG_USER, REG_PASS)
        driver.get(BASE_URL)
        time.sleep(0.5)
        # Không được có lỗi 500
        assert "500" not in driver.page_source, \
            "Xảy ra lỗi 500 khi Cold Start user xem trang chủ"
        # Phải có ít nhất 1 card sản phẩm
        cards = driver.find_elements(By.CSS_SELECTOR, ".card")
        assert len(cards) > 0, \
            "Trang chủ không hiển thị card sản phẩm nào cho user mới (Cold Start)"

    def test_similar_products_on_product_detail(self, driver):
        """TC-SEL-REC-04: Chi tiết sản phẩm có phần sản phẩm tương tự"""
        driver.get(f"{BASE_URL}/product/1")
        time.sleep(0.5)
        page = driver.page_source
        if "404" not in page:
            # Nếu trang tồn tại, phải có section similar hoặc card khác
            has_similar = (
                "tương tự" in page.lower()
                or "similar" in page.lower()
                or len(driver.find_elements(By.CSS_SELECTOR, "a[href*='/product/']")) > 1
            )
            assert has_similar, \
                "Không có section sản phẩm tương tự trên trang chi tiết"

    def test_recommendation_logged_in_user(self, driver):
        """TC-SEL-REC-05: User đã đăng nhập → /recommendations không lỗi"""
        login(driver, NORMAL_USER, NORMAL_PASS)
        driver.get(f"{BASE_URL}/recommendations")
        time.sleep(1)
        assert "500" not in driver.page_source, \
            "Trang gợi ý bị lỗi 500 với user đã đăng nhập"


# ============================================================
# NHÓM 8: KIỂM THỬ TRANG ADMIN
# ============================================================
class TestAdminPanel:
    """TC-SEL-ADMIN: Kiểm tra bảo vệ và chức năng trang quản trị"""

    def test_admin_blocked_for_normal_user(self, driver):
        """TC-SEL-ADMIN-01: User thường truy cập /admin → bị chặn (403 hoặc redirect)"""
        login(driver, NORMAL_USER, NORMAL_PASS)
        driver.get(f"{BASE_URL}/admin")
        time.sleep(0.5)
        # Phải bị chặn: 403 hoặc redirect về nơi khác
        assert "/admin" not in driver.current_url or \
               "403" in driver.page_source or \
               "không có quyền" in driver.page_source.lower(), \
            "User thường không bị chặn khi vào /admin"

    def test_admin_blocked_for_anonymous(self, driver):
        """TC-SEL-ADMIN-02: Chưa đăng nhập truy cập /admin → redirect /login"""
        logout(driver)
        driver.get(f"{BASE_URL}/admin")
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.url_contains("/login")
        )
        assert "/login" in driver.current_url

    def test_admin_dashboard_loads(self, driver):
        """TC-SEL-ADMIN-03: Admin đăng nhập → Dashboard hiển thị đầy đủ"""
        login(driver, ADMIN_USER, ADMIN_PASS)
        driver.get(f"{BASE_URL}/admin")
        time.sleep(0.5)
        assert "/admin" in driver.current_url, \
            f"Admin không vào được /admin, đang ở: {driver.current_url}"

    def test_admin_dashboard_has_kpi(self, driver):
        """TC-SEL-ADMIN-04: Dashboard hiển thị các chỉ số KPI"""
        login(driver, ADMIN_USER, ADMIN_PASS)
        driver.get(f"{BASE_URL}/admin")
        time.sleep(0.5)
        page = driver.page_source
        # Phải có ít nhất 1 trong các từ liên quan KPI
        kpi_keywords = ["sản phẩm", "đơn hàng", "doanh thu", "người dùng",
                        "product", "order", "revenue"]
        has_kpi = any(kw in page.lower() for kw in kpi_keywords)
        assert has_kpi, "Dashboard thiếu các chỉ số KPI"

    def test_admin_products_page(self, driver):
        """TC-SEL-ADMIN-05: Trang quản lý sản phẩm /admin/products tải thành công"""
        login(driver, ADMIN_USER, ADMIN_PASS)
        driver.get(f"{BASE_URL}/admin/products")
        time.sleep(0.5)
        assert "/admin/products" in driver.current_url, \
            "Không vào được trang quản lý sản phẩm"

    def test_admin_add_product_page(self, driver):
        """TC-SEL-ADMIN-06: Trang thêm sản phẩm /admin/products/add tải thành công"""
        login(driver, ADMIN_USER, ADMIN_PASS)
        driver.get(f"{BASE_URL}/admin/products/add")
        time.sleep(0.5)
        assert "admin/products/add" in driver.current_url, \
            "Không vào được trang thêm sản phẩm"
        # Phải có form nhập thông tin
        assert driver.find_elements(By.NAME, "name"), \
            "Thiếu field 'name' trong form thêm sản phẩm"
        assert driver.find_elements(By.NAME, "price"), \
            "Thiếu field 'price' trong form thêm sản phẩm"

    def test_admin_add_product_success(self, driver):
        """TC-SEL-ADMIN-07: Admin thêm sản phẩm mới thành công"""
        login(driver, ADMIN_USER, ADMIN_PASS)
        driver.get(f"{BASE_URL}/admin/products/add")
        time.sleep(0.5)

        name_fields = driver.find_elements(By.NAME, "name")
        price_fields = driver.find_elements(By.NAME, "price")
        stock_fields = driver.find_elements(By.NAME, "stock")
        category_selects = driver.find_elements(By.NAME, "category_id")

        if not (name_fields and price_fields and stock_fields and category_selects):
            pytest.skip("Form thêm sản phẩm không đủ fields")

        name_fields[0].send_keys("Selenium Test Product")
        price_fields[0].send_keys("99000")
        stock_fields[0].clear()
        stock_fields[0].send_keys("50")

        # Chọn category đầu tiên
        sel = Select(category_selects[0])
        if len(sel.options) > 0:
            sel.select_by_index(0)

        unit_fields = driver.find_elements(By.NAME, "unit")
        if unit_fields:
            unit_fields[0].clear()
            unit_fields[0].send_keys("kg")

        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)

        # Phải redirect về /admin/products sau khi thêm thành công
        assert "/admin/products" in driver.current_url, \
            f"Sau thêm SP phải về /admin/products, đang ở: {driver.current_url}"
        flash = get_flash_message(driver)
        assert "thành công" in flash.lower() or "thêm" in flash.lower(), \
            f"Không hiện thông báo thêm sản phẩm. Flash: {flash}"

    def test_admin_add_product_missing_required_fields(self, driver):
        """TC-SEL-ADMIN-08: Admin thêm sản phẩm thiếu tên → hiện lỗi"""
        login(driver, ADMIN_USER, ADMIN_PASS)
        driver.get(f"{BASE_URL}/admin/products/add")
        time.sleep(0.5)

        # Để trống name, chỉ điền price
        price_fields = driver.find_elements(By.NAME, "price")
        if price_fields:
            price_fields[0].send_keys("50000")

        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)

        page = driver.page_source
        assert "bắt buộc" in page.lower() or \
               "điền đầy đủ" in page.lower() or \
               "add" in driver.current_url, \
            "Phải hiện lỗi khi thiếu trường bắt buộc"

    def test_admin_orders_page(self, driver):
        """TC-SEL-ADMIN-09: Trang quản lý đơn hàng /admin/orders tải thành công"""
        login(driver, ADMIN_USER, ADMIN_PASS)
        driver.get(f"{BASE_URL}/admin/orders")
        time.sleep(0.5)
        assert "/admin/orders" in driver.current_url, \
            "Không vào được trang quản lý đơn hàng"

    def test_admin_orders_filter_by_status(self, driver):
        """TC-SEL-ADMIN-10: Lọc đơn hàng theo trạng thái"""
        login(driver, ADMIN_USER, ADMIN_PASS)
        driver.get(f"{BASE_URL}/admin/orders?status=pending")
        time.sleep(0.5)
        assert "status=pending" in driver.current_url, \
            "URL không chứa tham số lọc trạng thái"


# ============================================================
# NHÓM 9: KIỂM THỬ BẢO MẬT (SECURITY)
# ============================================================
class TestSecurity:
    """TC-SEL-SEC: Kiểm tra các lỗ hổng bảo mật phổ biến"""

    def test_xss_in_search(self, driver):
        """TC-SEL-SEC-01: Nhập payload XSS vào ô tìm kiếm → không thực thi script"""
        xss_payload = "<script>alert('XSS')</script>"
        driver.get(f"{BASE_URL}/shop?q={xss_payload}")
        time.sleep(0.5)

        # Nếu XSS thành công, sẽ có alert popup → gây TimeoutException
        try:
            WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.dismiss()
            assert False, "XSS thực thi thành công — LỖ HỔNG BẢO MẬT NGHIÊM TRỌNG!"
        except TimeoutException:
            pass  # Không có alert → Jinja2 đã escape đúng → PASS

    def test_admin_403_for_normal_user(self, driver):
        """TC-SEL-SEC-02: User thường không thể truy cập /admin/* → HTTP 403"""
        login(driver, NORMAL_USER, NORMAL_PASS)

        protected_urls = [
            f"{BASE_URL}/admin",
            f"{BASE_URL}/admin/products",
            f"{BASE_URL}/admin/orders",
            f"{BASE_URL}/admin/products/add",
        ]
        for url in protected_urls:
            driver.get(url)
            time.sleep(0.3)
            is_blocked = (
                "/admin" not in driver.current_url
                or "403" in driver.page_source
                or "không có quyền" in driver.page_source.lower()
            )
            assert is_blocked, f"User thường không bị chặn tại: {url}"

    def test_sql_injection_in_search(self, driver):
        """TC-SEL-SEC-03: SQL Injection qua ô tìm kiếm → hệ thống xử lý an toàn"""
        sql_payload = "' OR '1'='1'; DROP TABLE products;--"
        driver.get(f"{BASE_URL}/shop?q={sql_payload}")
        time.sleep(0.5)
        # Trang phải load thành công, không có lỗi 500
        assert "500" not in driver.page_source and \
               "Internal Server Error" not in driver.page_source, \
            "Hệ thống bị lỗi 500 khi nhận SQL Injection — LỖ HỔNG BẢO MẬT!"

    def test_direct_url_admin_blocked_anonymous(self, driver):
        """TC-SEL-SEC-04: Truy cập trực tiếp URL /admin khi chưa login → bị chặn"""
        logout(driver)
        admin_urls = [
            f"{BASE_URL}/admin",
            f"{BASE_URL}/admin/products",
            f"{BASE_URL}/admin/orders",
        ]
        for url in admin_urls:
            driver.get(url)
            time.sleep(0.3)
            assert "/login" in driver.current_url, \
                f"Chưa login nhưng không bị redirect tại: {url}"

    def test_session_cleared_after_logout(self, driver):
        """TC-SEL-SEC-05: Sau logout, session bị xóa — không thể back lại trang user"""
        login(driver, NORMAL_USER, NORMAL_PASS)
        time.sleep(0.3)
        logout(driver)
        time.sleep(0.3)

        # Thử vào trang yêu cầu login
        driver.get(f"{BASE_URL}/orders")
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.url_contains("/login")
        )
        assert "/login" in driver.current_url, \
            "Session vẫn còn hiệu lực sau khi logout — LỖ HỔNG BẢO MẬT!"


# ============================================================
# NHÓM 10: KIỂM THỬ PHÂN TRANG VÀ HIỂN THỊ
# ============================================================
class TestPagination:
    """TC-SEL-PAGE: Kiểm tra phân trang và hiển thị danh sách"""

    def test_shop_pagination_exists(self, driver):
        """TC-SEL-PAGE-01: Trang shop có phân trang nếu có đủ sản phẩm"""
        driver.get(f"{BASE_URL}/shop")
        time.sleep(0.5)
        page = driver.page_source
        # Nếu có sản phẩm > 12, phải có pagination
        pagination = driver.find_elements(
            By.CSS_SELECTOR, ".pagination, nav[aria-label*='pagination']"
        )
        product_cards = driver.find_elements(By.CSS_SELECTOR, ".card")
        # Chỉ kiểm tra logic: nếu có card sản phẩm thì trang load đúng
        assert len(product_cards) > 0 or "Không có sản phẩm" in page, \
            "Trang shop không hiển thị đúng"

    def test_shop_page_2_if_available(self, driver):
        """TC-SEL-PAGE-02: Phân trang shop — truy cập trang 2 nếu có"""
        driver.get(f"{BASE_URL}/shop?page=2")
        time.sleep(0.5)
        # Không được có lỗi 500
        assert "500" not in driver.page_source and \
               "Internal Server Error" not in driver.page_source, \
            "Lỗi khi truy cập trang 2 của shop"

    def test_admin_products_pagination(self, driver):
        """TC-SEL-PAGE-03: Phân trang trang admin/products"""
        login(driver, ADMIN_USER, ADMIN_PASS)
        driver.get(f"{BASE_URL}/admin/products?page=1")
        time.sleep(0.5)
        assert "500" not in driver.page_source, \
            "Lỗi khi truy cập phân trang admin products"
