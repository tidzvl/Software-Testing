"""
Sample test cases để minh họa cách sử dụng Selenium Service
"""

import pytest
import sys
import os
from time import sleep
# Thêm đường dẫn root vào sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.selenium_service import SeleniumService
from config.config import config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="class", autouse=True)
def selenium_driver(request):
    service = SeleniumService(browser="chrome", headless=False)
    driver = service.start_driver()
    request.cls.driver = driver
    request.cls.selenium_service = service
    yield driver
    service.quit_driver()

@pytest.mark.usefixtures("selenium_driver")
class TestAddToCart:

    @pytest.fixture(autouse=True)
    def clear_after_each(self):
        yield
        self.selenium_service.clear_storage()

    def test_TC_001_001(self):
        """BVA - Minimum Valid Quantity"""
        self.driver.get(config.BASE_URL)
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-id="1"]'))
        )
        logger.info(f"Tiến hành thêm sản phẩm 1 vào giỏ hàng.")
        element.click()
        badge = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".badge.badge-success"))
        )
        badge_text = badge.text.strip()
        logger.info(f"Badge giỏ hàng hiển thị: {badge_text}")
        assert badge_text == "1", f"FAIL: Badge giỏ hàng = {badge_text}, mong đợi = 1"
        logger.info("PASS: Badge giỏ hàng = 1")

    def test_TC_001_002(self):
        """BVA - Maximum Valid Quantity"""
        self.driver.get(config.BASE_URL)
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-id="1"]'))
        )
        logger.info(f"Tiến hành thêm sản phẩm 1 vào giỏ hàng 10 lần.")
        for i in range(10):
            element.click()
            logger.info(f"Đã click lần thứ {i+1}")
        badge = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".badge.badge-success"))
        )
        badge_text = badge.text.strip()
        logger.info(f"Badge giỏ hàng hiển thị: {badge_text}")
        assert badge_text == "10", f"FAIL: Badge giỏ hàng = {badge_text}, mong đợi = 10"
        logger.info("PASS: Badge giỏ hàng = 10")

    def test_TC_001_003(self):
        """ECP - Empty cart, Valid Product: Candy"""
        self.driver.get(config.BASE_URL)
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-id="9"]'))
        )
        logger.info(f"Tiến hành thêm Candy vào giỏ hàng.")
        element.click()

        badge = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".badge.badge-success"))
        )
        badge_text = badge.text.strip()
        logger.info(f"Badge giỏ hàng hiển thị: {badge_text}")

        assert badge_text == "1", f"FAIL: Badge giỏ hàng = {badge_text}, mong đợi = 1"
        logger.info("PASS: Badge giỏ hàng = 1")

    def test_TC_001_004(self):
        """ECP - Add Same Product to not empty cart"""
        self.driver.get(config.BASE_URL)
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-id="2"]'))
        )
        logger.info(f"Tiến hành thêm trước sản phẩm 2 (Rainbow) vào giỏ hàng.")
        element.click()

        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-id="1"]'))
        )
        logger.info(f"Tiến hành thêm tiếp sản phẩm 1 (Candy) vào giỏ hàng.")
        element.click()

        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-id="9"]'))
        )
        logger.info(f"Tiến hành thêm tiếp sản phẩm 9 (Candy) vào giỏ hàng.")
        element.click()
        logger.info(f"Truy cập giỏ hàng")

        self.driver.get("https://sweetshop.netlify.app/basket")


        basket = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "basketItems"))
        )

        items = basket.find_elements(By.TAG_NAME, "li")

        product_items = items[:-1]

        count = len(product_items)
        print(f"Số lượng sản phẩm trong giỏ hàng: {count}")

        assert count == 3, f"FAIL: Số lượng sản phẩm = {count}, mong đợi = 3"
        print("PASS: Số lượng sản phẩm = 3")

    def test_TC_001_005(self):
        """Use-Case - Add Multiple Products"""
        self.driver.get(config.BASE_URL)
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-id="2"]'))
        )
        logger.info(f"Tiến hành thêm trước sản phẩm 2 (Rainbow) vào giỏ hàng.")
        element.click()

        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-id="1"]'))
        )
        logger.info(f"Tiến hành thêm tiếp sản phẩm 1 (Candy) vào giỏ hàng.")
        element.click()

        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-id="9"]'))
        )
        logger.info(f"Tiến hành thêm tiếp sản phẩm 9 (Candy) vào giỏ hàng.")
        element.click()
        logger.info(f"Truy cập giỏ hàng")

        self.driver.get("https://sweetshop.netlify.app/basket")


        basket = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "basketItems"))
        )

        items = basket.find_elements(By.TAG_NAME, "li")

        product_items = items[:-1]

        count = len(product_items)
        print(f"Số lượng sản phẩm trong giỏ hàng: {count}")

        assert count == 3, f"FAIL: Số lượng sản phẩm = {count}, mong đợi = 3"
        print("PASS: Số lượng sản phẩm = 3")

    def test_TC_001_006(self):
        """Use-Case - Clear Cart Workflow"""
        self.driver.get(config.BASE_URL)
        for i in range(1, 11):
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-id="{i}"]'))
            )
            product_name = element.get_attribute("data-name")
            logger.info(f"Tiến hành thêm sản phẩm {i} - {product_name} vào giỏ hàng.")
            element.click()

        logger.info(f"Truy cập giỏ hàng")

        self.driver.get("https://sweetshop.netlify.app/basket")
        logger.info(f"Tiến hành xóa tất cả sản phẩm.")

        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[onclick="emptyBasket();"]'))
        )
        element.click()
        alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())

        alert.accept()
        basket = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "basketItems"))
        )

        items = basket.find_elements(By.TAG_NAME, "li")

        product_items = items[:-1]

        count = len(product_items)
        print(f"Số lượng sản phẩm trong giỏ hàng: {count}")

        assert count == 0, f"FAIL: Số lượng sản phẩm = {count}, mong đợi = 0"
        print("PASS: Số lượng sản phẩm = 3")

@pytest.mark.usefixtures("selenium_driver")
class TestCartCalculation:

    @pytest.fixture(autouse=True)
    def clear_after_each(self):
        yield
        self.selenium_service.clear_storage()

    def test_TC_002_001(self):
        """BVA - Empty Cart Total: Tính tổng khi giỏ rỗng (minimum)"""

        self.driver.get("https://sweetshop.netlify.app/basket")

        total_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li/span[text()="Total (GBP)"]/following-sibling::strong'))
        )
        total_text = total_element.text.strip()
        print(f'Total hiển thị: {total_text}')

        assert total_text == "£0.00", f"FAIL: Total = {total_text}, mong đợi = £0.00"
        print("PASS: Total (GBP) = £0.00 khi giỏ rỗng")

    def test_TC_002_002(self):
        """BVA - Single Item Total: Tính tổng 1 sản phẩm (minimum hợp lệ)"""

        self.driver.get(config.BASE_URL)

        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-id="1"]'))
        )
        product_name = element.get_attribute("data-name")
        product_price = element.get_attribute("data-price")
        logger.info(f"Tiến hành thêm sản phẩm {product_name} có giá {product_price} vào giỏ hàng.")
        element.click()
        logger.info(f"Kiểm tra giỏ hàng.")

        self.driver.get("https://sweetshop.netlify.app/basket")

        total_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li/span[text()="Total (GBP)"]/following-sibling::strong'))
        )
        total_text = total_element.text.strip()
        logger.info(f'Total hiển thị: {total_text}')

        assert total_text == "£1.00", f"FAIL: Total = {total_text}, mong đợi = £1.00"
        logger.info("PASS: Total (GBP) = £1.00 khi giỏ có 1 Chocolate Cups")

    def test_TC_002_003(self):
        """BVA - Typical Multi-Item: Chocolate Cups x1 (£1.00) + Sherbert Straws x2 (£0.75) = £2.50"""

        self.driver.get("https://sweetshop.netlify.app/sweets")

        # Thêm Chocolate Cups x1
        choc = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-id="1"]'))
        )
        choc.click()

        sherbert = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-id="2"]'))
        )
        sherbert.click()
        sherbert.click()

        self.driver.get("https://sweetshop.netlify.app/basket")
        total_text = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li/span[text()="Total (GBP)"]/following-sibling::strong'))
        ).text.strip()

        assert total_text == "£2.50", f"FAIL: Total = {total_text}, mong đợi = £2.50"

    def test_TC_002_004(self):
        """BVA - Large Quantity Total: Chocolate Cups x100 (£1.00) = £100.00"""

        self.driver.get("https://sweetshop.netlify.app/sweets")
        choc = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-id="1"]'))
        )
        for _ in range(100):
            choc.click()

        self.driver.get("https://sweetshop.netlify.app/basket")
        total_text = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li/span[text()="Total (GBP)"]/following-sibling::strong'))
        ).text.strip()

        assert total_text == "£100.00", f"FAIL: Total = {total_text}, mong đợi = £100.00"

    def test_TC_002_005(self):
        """ECP - Low Price Items: Bubble Gums x3 (£0.25) = £0.75"""

        self.driver.get("https://sweetshop.netlify.app/sweets")
        bubble = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-id="7"]')) 
        )
        for _ in range(3):
            bubble.click()

        self.driver.get("https://sweetshop.netlify.app/basket")
        total_text = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li/span[text()="Total (GBP)"]/following-sibling::strong'))
        ).text.strip()

        assert total_text == "£0.75", f"FAIL: Total = {total_text}, mong đợi = £0.75"

    def test_TC_002_006(self):
        """DTT - Formula: 1 Item, Total = Price × 1"""
        self.driver.get("https://sweetshop.netlify.app/sweets")

        choc = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-id="1"]'))
        )
        choc.click()
        choc_price = float(choc.get_attribute("data-price"))

        self.driver.get("https://sweetshop.netlify.app/basket")
        price = self.driver.find_element(By.CSS_SELECTOR, "#basketItems li span.text-muted").text.strip()
        qty = self.driver.find_element(By.CSS_SELECTOR, "#basketItems li small.text-muted").text.strip().replace("x ", "")
        total_text = self.driver.find_element(By.XPATH, '//li/span[text()="Total (GBP)"]/following-sibling::strong').text.strip()

        price_val = float(price.replace("£", ""))
        qty_val = int(qty)
        expected_total = f"£{choc_price:.2f}"

        assert total_text == expected_total, f"FAIL: Total = {total_text}, mong đợi = {expected_total}"

    def test_TC_002_007(self):
        """DTT - Formula: Multi-Type, Total = Σ(Price × Qty)"""
        self.driver.get(config.BASE_URL)

        for i in range(1, 11):
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-id="{i}"]'))
            )
            product_name = element.get_attribute("data-name")
            logger.info(f"Tiến hành thêm sản phẩm {i} - {product_name} vào giỏ hàng.")
            element.click()
        self.driver.get("https://sweetshop.netlify.app/basket")

        items = self.driver.find_elements(By.CSS_SELECTOR, "#basketItems li.list-group-item.d-flex.justify-content-between.lh-condensed")

        calc_total = 0.0
        for item in items:
            qty_text = item.find_element(By.CSS_SELECTOR, "small.text-muted").text.strip().replace("x ", "")
            price_text = item.find_element(By.CSS_SELECTOR, "span.text-muted").text.strip()
            qty_val = int(qty_text)
            price_val = float(price_text.replace("£", ""))
            calc_total += qty_val * price_val

        total_text = self.driver.find_element(By.XPATH, '//li/span[text()="Total (GBP)"]/following-sibling::strong').text.strip()
        expected_total = f"£{calc_total:.2f}"

        assert total_text == expected_total, f"FAIL: Total = {total_text}, mong đợi = {expected_total}"

    def test_TC_002_008(self):
        """Use-Case - Delete item: Total price bị trừ đi"""

        self.driver.get("https://sweetshop.netlify.app/sweets")
        for i in range(1, 4):
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-id="{i}"]'))
            )
            product_name = element.get_attribute("data-name")
            logger.info(f"Thêm sản phẩm {product_name} (id={i}) vào giỏ hàng.")
            element.click()

        self.driver.get("https://sweetshop.netlify.app/basket")

        total_before_text = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li/span[text()="Total (GBP)"]/following-sibling::strong'))
        ).text.strip()
        total_before_val = float(total_before_text.replace("£", ""))
        logger.info(f"Total trước khi xóa: {total_before_val}")

        basket_items = self.driver.find_elements(By.CSS_SELECTOR, "#basketItems li.list-group-item.d-flex.justify-content-between.lh-condensed")
        target_item = None
        for item in basket_items:
            name = item.find_element(By.CSS_SELECTOR, "h6.my-0").text.strip()
            if name == "Sherbet Discs":
                target_item = item
                break
        assert target_item is not None, "FAIL: Không tìm thấy sản phẩm Sherbet Discs trong giỏ hàng"

        qty_text = target_item.find_element(By.CSS_SELECTOR, "small.text-muted").text.strip().replace("x ", "")
        price_text = target_item.find_element(By.CSS_SELECTOR, "span.text-muted").text.strip()
        qty_val = int(qty_text)
        price_val = float(price_text.replace("£", ""))
        logger.info(f"Sản phẩm Sherbet Discs: qty={qty_val}, price={price_val}")

        delete_link = target_item.find_element(By.CSS_SELECTOR, "a.small")
        delete_link.click()
        alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())

        alert.accept()

        total_after_text = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li/span[text()="Total (GBP)"]/following-sibling::strong'))
        ).text.strip()
        total_after_val = float(total_after_text.replace("£", ""))
        logger.info(f"Total sau khi xóa: {total_after_val}")

        expected_total = total_before_val - (price_val * qty_val)

        expected_total = round(expected_total, 2)
        total_after_val = round(total_after_val, 2)

        assert total_after_val == expected_total, f"FAIL: Total sau khi xóa = {total_after_val}, mong đợi = {expected_total}"

        assert total_after_val == expected_total, f"FAIL: Total sau khi xóa = {total_after_val}, mong đợi = {expected_total}"
        logger.info("PASS: Total sau khi xóa đúng bằng total_before - giá sản phẩm đã xóa")


    def test_TC_002_009(self):
        """Use-Case - Standard Shipping: Thêm phí ship (£1.99)"""

        self.driver.get("https://sweetshop.netlify.app/sweets")
        choc = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-id="1"]'))
        )
        choc.click()

        self.driver.get("https://sweetshop.netlify.app/basket")

        shipping_option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//label[contains(text(),"Standard Shipping (£1.99)")]'))
        )
        shipping_option.click()

        total_text = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li/span[text()="Total (GBP)"]/following-sibling::strong'))
        ).text.strip()

        assert total_text == "£2.99", f"FAIL: Total = {total_text}, mong đợi = £2.99"

if __name__ == "__main__":
    # pytest.main([__file__, "-v", "--html=reports/report.html", "--self-contained-html"])
    pytest.main([__file__ + "::TestCartCalculation",
             "-v", "--html=reports/report.html", "--self-contained-html"])

