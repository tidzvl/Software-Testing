import os
import time
from datetime import datetime
from functools import wraps
import logging

logger = logging.getLogger(__name__)


def retry(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        logger.error(f"Đã thử {max_attempts} lần nhưng vẫn thất bại: {str(e)}")
                        raise
                    logger.warning(f"Lần thử {attempts} thất bại. Thử lại sau {delay}s...")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator


def generate_timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def take_screenshot_on_failure(driver, test_name: str, screenshot_dir: str = "./screenshots"):
    try:
        os.makedirs(screenshot_dir, exist_ok=True)
        timestamp = generate_timestamp()
        filename = f"{screenshot_dir}/{test_name}_{timestamp}.png"
        driver.save_screenshot(filename)
        logger.info(f"Screenshot lỗi đã được lưu: {filename}")
        return filename
    except Exception as e:
        logger.error(f"Không thể chụp screenshot: {str(e)}")
        return None


def wait_for_page_load(driver, timeout: int = 30):
    from selenium.webdriver.support.ui import WebDriverWait

    def page_loaded(driver):
        return driver.execute_script("return document.readyState") == "complete"

    try:
        WebDriverWait(driver, timeout).until(page_loaded)
        logger.info("Trang đã load hoàn toàn")
    except Exception as e:
        logger.warning(f"Timeout khi chờ trang load: {str(e)}")


def scroll_to_element(driver, element):
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)
        logger.info("Đã scroll đến element")
    except Exception as e:
        logger.error(f"Lỗi khi scroll đến element: {str(e)}")


def highlight_element(driver, element, duration: float = 2.0):
    try:
        original_style = element.get_attribute("style")
        driver.execute_script(
            "arguments[0].setAttribute('style', 'border: 3px solid red; background: yellow;');",
            element
        )
        time.sleep(duration)
        driver.execute_script(
            f"arguments[0].setAttribute('style', '{original_style}');",
            element
        )
    except Exception as e:
        logger.error(f"Lỗi khi highlight element: {str(e)}")


def get_element_text_safely(element) -> str:
    try:
        return element.text.strip()
    except Exception as e:
        logger.error(f"Lỗi khi lấy text: {str(e)}")
        return ""


def clear_and_send_keys(element, text: str):
    try:
        element.clear()
        time.sleep(0.2)
        element.send_keys(text)
        logger.info(f"Đã nhập text: {text}")
    except Exception as e:
        logger.error(f"Lỗi khi nhập text: {str(e)}")
        raise
