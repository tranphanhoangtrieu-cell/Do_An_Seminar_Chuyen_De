"""
conftest.py — Cấu hình toàn cục cho pytest Selenium
=====================================================
File này được pytest tự động load trước khi chạy bất kỳ test nào.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    """Thêm tuỳ chọn dòng lệnh cho pytest."""
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Chạy Chrome ở chế độ headless (không hiện cửa sổ trình duyệt)"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default="http://127.0.0.1:5000",
        help="Base URL của ứng dụng Flask (mặc định: http://127.0.0.1:5000)"
    )


@pytest.fixture(scope="session")
def base_url(request):
    """Trả về base URL từ tham số dòng lệnh."""
    return request.config.getoption("--base-url")


@pytest.fixture(scope="session")
def chrome_driver(request):
    """
    Driver dùng chung cho toàn bộ session (tất cả test files).
    Dùng fixture này trong conftest, còn fixture 'driver' trong test_selenium.py
    là scope='class' cho từng nhóm test.
    """
    headless = request.config.getoption("--headless")

    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1366,768")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)

    yield driver

    driver.quit()


def pytest_configure(config):
    """Đăng ký markers tuỳ chỉnh để tránh warning."""
    config.addinivalue_line("markers", "slow: đánh dấu test chạy chậm")
    config.addinivalue_line("markers", "auth: đánh dấu test liên quan xác thực")
    config.addinivalue_line("markers", "admin: đánh dấu test liên quan Admin")
    config.addinivalue_line("markers", "security: đánh dấu test bảo mật")
    config.addinivalue_line("markers", "recommendation: đánh dấu test hệ thống gợi ý")
