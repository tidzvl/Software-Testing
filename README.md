# Software Testing với Selenium

Dự án test automation sử dụng Selenium WebDriver và Python để thực hiện automated testing cho web applications.

## Cấu trúc dự án

```
Software-Testing/
├── config/                 # Cấu hình cho test environment
│   ├── __init__.py
│   └── config.py          # File cấu hình chính
├── services/              # Services và utilities
│   ├── __init__.py
│   └── selenium_service.py # Selenium WebDriver service
├── tests/                 # Test cases
│   ├── __init__.py
│   └── test_example.py    # Sample test cases
├── utils/                 # Helper functions
│   ├── __init__.py
│   └── helper.py          # Utility functions
├── screenshots/           # Screenshots từ tests (tự động tạo)
├── reports/              # Test reports (tự động tạo)
├── .env.example          # Template cho environment variables
├── pytest.ini            # Pytest configuration
└── requirements.txt      # Python dependencies

```

## Yêu cầu hệ thống

- Python 3.8 trở lên
- Chrome/Firefox/Edge browser
- pip (Python package manager)

## Cài đặt

### 1. Clone repository hoặc tải về

```bash
cd Software-Testing
```

### 2. Tạo virtual environment (khuyến nghị)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 4. Cấu hình environment variables

```bash
# Copy file .env.example thành .env
copy .env.example .env

# Chỉnh sửa .env theo nhu cầu của bạn
```

## Sử dụng Selenium Service

### Sử dụng cơ bản

```python
from services.selenium_service import SeleniumService
from selenium.webdriver.common.by import By

# Khởi tạo service
selenium_service = SeleniumService(
    browser="chrome",    # chrome, firefox, edge
    headless=False,      # True để chạy không hiển thị giao diện
    implicit_wait=10
)

# Khởi động driver
driver = selenium_service.start_driver()

# Thực hiện test
driver.get("https://www.google.com")
print(driver.title)

# Đóng driver
selenium_service.quit_driver()
```

### Sử dụng với Context Manager

```python
from services.selenium_service import SeleniumService

# Tự động đóng driver khi kết thúc
with SeleniumService(browser="chrome", headless=True) as selenium_service:
    driver = selenium_service.get_driver()
    driver.get("https://www.google.com")
    print(driver.title)
```

### Các tính năng của SeleniumService

```python
# Chờ element xuất hiện
element = selenium_service.wait_for_element(By.ID, "search-box", timeout=10)

# Chờ element có thể click
button = selenium_service.wait_for_element_clickable(By.XPATH, "//button[@type='submit']")

# Chụp screenshot
selenium_service.take_screenshot("screenshots/test_result.png")
```

## Chạy Tests

### Chạy tất cả tests

```bash
pytest
```

### Chạy test file cụ thể

```bash
pytest tests/test_example.py
```

### Chạy test với verbose output

```bash
pytest -v
```

### Chạy test và tạo HTML report

```bash
pytest --html=reports/report.html --self-contained-html
```

### Chạy test với markers

```bash
# Chạy chỉ smoke tests
pytest -m smoke

# Chạy chỉ regression tests
pytest -m regression
```

### Chạy test parallel (nhanh hơn)

```bash
pytest -n auto
```

## Cấu hình

### Browser Configuration

Trong [config/config.py](config/config.py) hoặc file `.env`:

```python
BROWSER=chrome        # chrome, firefox, edge
HEADLESS=False        # True/False
IMPLICIT_WAIT=10      # seconds
PAGE_LOAD_TIMEOUT=30  # seconds
```

### Test Data Configuration

```python
BASE_URL=https://example.com
TEST_USERNAME=testuser@example.com
TEST_PASSWORD=TestPassword123
```

## Các tính năng chính

### 1. SeleniumService

- Tự động quản lý WebDriver
- Hỗ trợ nhiều browsers (Chrome, Firefox, Edge)
- Tự động cài đặt driver với webdriver-manager
- Context manager support
- Wait utilities
- Screenshot capabilities

### 2. Helper Utilities

Trong [utils/helper.py](utils/helper.py):

- `retry`: Decorator để retry khi gặp lỗi
- `take_screenshot_on_failure`: Chụp screenshot khi test fail
- `wait_for_page_load`: Chờ page load hoàn toàn
- `scroll_to_element`: Scroll đến element
- `highlight_element`: Highlight element (debugging)
- `clear_and_send_keys`: Clear và nhập text

### 3. Test Configuration

Sử dụng pytest.ini để cấu hình:
- Test discovery patterns
- Output formats
- Markers cho test categories
- Logging configuration

## Ví dụ Test Cases

### Test đơn giản

```python
import pytest
from services.selenium_service import SeleniumService
from selenium.webdriver.common.by import By

class TestExample:
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        self.selenium_service = SeleniumService(browser="chrome")
        self.driver = self.selenium_service.start_driver()
        yield
        self.selenium_service.quit_driver()

    def test_open_website(self):
        self.driver.get("https://www.google.com")
        assert "Google" in self.driver.title
```

### Test với parametrize

```python
@pytest.mark.parametrize("url,expected_title", [
    ("https://www.google.com", "Google"),
    ("https://www.python.org", "Python"),
])
def test_multiple_urls(url, expected_title):
    with SeleniumService(browser="chrome") as selenium_service:
        driver = selenium_service.get_driver()
        driver.get(url)
        assert expected_title.lower() in driver.title.lower()
```

## Best Practices

1. **Sử dụng Page Object Model (POM)** cho tests phức tạp
2. **Sử dụng explicit waits** thay vì time.sleep()
3. **Chụp screenshots** khi tests fail để debug
4. **Sử dụng meaningful test names** và docstrings
5. **Tổ chức tests theo modules** và test suites
6. **Sử dụng fixtures** để tái sử dụng code setup
7. **Clean up resources** trong teardown

## Troubleshooting

### Driver không khởi động được

- Kiểm tra browser đã được cài đặt chưa
- Thử xóa cached drivers: `~/.wdm/` (Linux/Mac) hoặc `%USERPROFILE%\.wdm\` (Windows)
- Cập nhật webdriver-manager: `pip install --upgrade webdriver-manager`

### Tests chạy chậm

- Sử dụng `headless=True` mode
- Chạy parallel tests: `pytest -n auto`
- Tối ưu explicit waits thay vì implicit waits

### Element không tìm thấy

- Tăng timeout cho waits
- Kiểm tra selector có đúng không
- Sử dụng `wait_for_element` thay vì `find_element` trực tiếp

## Contributing

Khi thêm test mới:
1. Tạo test file trong thư mục `tests/`
2. Sử dụng naming convention: `test_*.py`
3. Thêm docstrings cho test functions
4. Sử dụng appropriate markers (@pytest.mark.smoke, etc.)

## Resources

- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [WebDriver Manager](https://github.com/SergeyPirogov/webdriver_manager)

## License

MIT License - xem file [LICENSE](LICENSE) để biết thêm chi tiết
