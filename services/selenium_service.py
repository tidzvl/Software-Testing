from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SeleniumService:

    def __init__(self, browser: str = "chrome", headless: bool = False,
                 implicit_wait: int = 10, page_load_timeout: int = 30):
        self.browser = browser.lower()
        self.headless = headless
        self.implicit_wait = implicit_wait
        self.page_load_timeout = page_load_timeout
        self.driver: Optional[webdriver.Remote] = None

    def start_driver(self) -> webdriver.Remote:
        try:
            if self.browser == "chrome":
                self.driver = self._setup_chrome()
            elif self.browser == "firefox":
                self.driver = self._setup_firefox()
            elif self.browser == "edge":
                self.driver = self._setup_edge()
            else:
                raise ValueError(f"Trình duyệt '{self.browser}' không được hỗ trợ")

            self.driver.implicitly_wait(self.implicit_wait)
            self.driver.set_page_load_timeout(self.page_load_timeout)
            self.driver.maximize_window()

            logger.info(f"WebDriver {self.browser} đã được khởi động thành công")
            return self.driver

        except Exception as e:
            logger.error(f"Lỗi khi khởi động WebDriver: {str(e)}")
            raise

    def _setup_chrome(self) -> webdriver.Chrome:
        options = ChromeOptions()
        if self.headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")


        options.add_argument("--log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        return webdriver.Chrome(options=options)

    def get_driver(self) -> webdriver.Remote:
        if self.driver is None:
            self.start_driver()
        return self.driver

    def quit_driver(self):
        if self.driver:
            try:
                self.driver.quit()
                logger.info("WebDriver đã được đóng")
            except Exception as e:
                logger.error(f"Lỗi khi đóng WebDriver: {str(e)}")
            finally:
                self.driver = None

    def clear_storage(self):
        if self.driver:
            try:
                self.driver.execute_script("window.localStorage.clear();")
                self.driver.execute_script("window.sessionStorage.clear();")
                self.driver.delete_all_cookies()
                logger.info("Đã clear localStorage, sessionStorage và cookies.")
            except Exception as e:
                logger.error(f"Lỗi khi clear storage: {e}")

    def wait_for_element(self, by: By, value: str, timeout: int = 10):
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located((by, value)))
            logger.info(f"Element '{value}' đã được tìm thấy")
            return element
        except Exception as e:
            logger.error(f"Không tìm thấy element '{value}': {str(e)}")
            raise

    def wait_for_element_clickable(self, by: By, value: str, timeout: int = 10):
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.element_to_be_clickable((by, value)))
            logger.info(f"Element '{value}' đã sẵn sàng để click")
            return element
        except Exception as e:
            logger.error(f"Element '{value}' không thể click: {str(e)}")
            raise

    def take_screenshot(self, filename: str):
        try:
            self.driver.save_screenshot(filename)
            logger.info(f"Screenshot đã được lưu: {filename}")
        except Exception as e:
            logger.error(f"Lỗi khi chụp screenshot: {str(e)}")

    def __enter__(self):
        self.start_driver()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit_driver()
