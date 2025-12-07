#
# File: test_cart_calculation.py
# Author: TiDz
# Contact: nguyentinvs123@gmail.com
# Created on Sun Dec 07 2025
# Description: 
# Useage: 
#

import csv
import os
import sys
from datetime import datetime
from time import sleep
from typing import List, Dict

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SeleniumHelper:
    """Helper class for Selenium operations"""

    def __init__(self, headless: bool = False):
        self.driver = None
        self.headless = headless

    def start_driver(self):
        """Start Chrome WebDriver"""
        options = ChromeOptions()
        if self.headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")

        options.add_argument("--log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        self.driver.set_page_load_timeout(30)
        self.driver.maximize_window()
        logger.info("WebDriver started successfully")
        return self.driver

    def quit_driver(self):
        """Quit WebDriver"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("WebDriver closed")
            except Exception as e:
                logger.error(f"Error closing WebDriver: {e}")

    def clear_storage(self):
        """Clear browser storage"""
        if self.driver:
            try:
                self.driver.execute_script("window.localStorage.clear();")
                self.driver.execute_script("window.sessionStorage.clear();")
                self.driver.delete_all_cookies()
                logger.info("Storage cleared")
            except Exception as e:
                logger.error(f"Error clearing storage: {e}")


class CartCalculationTest:
    """Test class for Cart Calculation functionality"""

    BASE_URL = "https://sweetshop.netlify.app/sweets"
    BASKET_URL = "https://sweetshop.netlify.app/basket"

    def __init__(self):
        self.helper = SeleniumHelper(headless=False)
        self.driver = None
        self.test_results = []

    def setup(self):
        """Setup test environment"""
        self.driver = self.helper.start_driver()

    def teardown(self):
        """Cleanup test environment"""
        self.helper.quit_driver()

    def clear_cart(self):
        """Clear cart before each test"""
        self.helper.clear_storage()

    def load_test_data(self) -> List[Dict]:
        """Load test data from CSV file"""
        csv_path = os.path.join(os.path.dirname(__file__), "test_data.csv")
        test_data = []

        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                test_data.append(row)

        logger.info(f"Loaded {len(test_data)} test cases from CSV")
        return test_data

    def get_total_from_basket(self) -> str:
        """Get total amount from basket page"""
        total_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li/span[text()="Total (GBP)"]/following-sibling::strong'))
        )
        return total_element.text.strip()

    def test_TC_002_001(self, test_case: Dict):
        """BVA - Empty Cart Total"""
        logger.info(f"Running {test_case['TestID']}: {test_case['Description']}")

        try:
            self.driver.get(self.BASKET_URL)

            total_text = self.get_total_from_basket()
            logger.info(f"Total displayed: {total_text}")

            expected_total = test_case['Expected_Total']
            assert total_text == expected_total, f"FAIL: Total = {total_text}, expected = {expected_total}"

            logger.info(f"PASS: {test_case['TestID']}")
            return "PASS"

        except AssertionError as e:
            logger.error(f"FAIL: {test_case['TestID']} - {str(e)}")
            return "FAIL"
        except Exception as e:
            logger.error(f"ERROR: {test_case['TestID']} - {str(e)}")
            return "ERROR"

    def test_TC_002_002(self, test_case: Dict):
        """BVA - Single Item Total"""
        logger.info(f"Running {test_case['TestID']}: {test_case['Description']}")

        try:
            self.driver.get(self.BASE_URL)

            product_id = test_case['Product_IDs']
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-id="{product_id}"]'))
            )
            product_name = element.get_attribute("data-name")
            product_price = element.get_attribute("data-price")
            logger.info(f"Adding product {product_name} with price {product_price} to cart")
            element.click()

            self.driver.get(self.BASKET_URL)

            total_text = self.get_total_from_basket()
            logger.info(f"Total displayed: {total_text}")

            expected_total = test_case['Expected_Total']
            assert total_text == expected_total, f"FAIL: Total = {total_text}, expected = {expected_total}"

            logger.info(f"PASS: {test_case['TestID']}")
            return "PASS"

        except AssertionError as e:
            logger.error(f"FAIL: {test_case['TestID']} - {str(e)}")
            return "FAIL"
        except Exception as e:
            logger.error(f"ERROR: {test_case['TestID']} - {str(e)}")
            return "ERROR"

    def test_TC_002_003(self, test_case: Dict):
        """BVA - Typical Multi-Item"""
        logger.info(f"Running {test_case['TestID']}: {test_case['Description']}")

        try:
            self.driver.get(self.BASE_URL)

            product_ids = test_case['Product_IDs'].split('|')
            quantities = [int(q) for q in test_case['Product_Quantities'].split('|')]

            for i, product_id in enumerate(product_ids):
                element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-id="{product_id}"]'))
                )
                qty = quantities[i]
                logger.info(f"Adding product {product_id} x{qty} to cart")
                for _ in range(qty):
                    element.click()

            self.driver.get(self.BASKET_URL)

            total_text = self.get_total_from_basket()
            logger.info(f"Total displayed: {total_text}")

            expected_total = test_case['Expected_Total']
            assert total_text == expected_total, f"FAIL: Total = {total_text}, expected = {expected_total}"

            logger.info(f"PASS: {test_case['TestID']}")
            return "PASS"

        except AssertionError as e:
            logger.error(f"FAIL: {test_case['TestID']} - {str(e)}")
            return "FAIL"
        except Exception as e:
            logger.error(f"ERROR: {test_case['TestID']} - {str(e)}")
            return "ERROR"

    def test_TC_002_004(self, test_case: Dict):
        """BVA - Large Quantity Total"""
        logger.info(f"Running {test_case['TestID']}: {test_case['Description']}")

        try:
            self.driver.get(self.BASE_URL)

            product_id = test_case['Product_IDs']
            quantity = int(test_case['Product_Quantities'])

            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-id="{product_id}"]'))
            )

            logger.info(f"Adding product {product_id} x{quantity} to cart")
            for i in range(quantity):
                element.click()
                if (i + 1) % 10 == 0:
                    logger.info(f"Progress: {i + 1}/{quantity}")

            self.driver.get(self.BASKET_URL)

            total_text = self.get_total_from_basket()
            logger.info(f"Total displayed: {total_text}")

            expected_total = test_case['Expected_Total']
            assert total_text == expected_total, f"FAIL: Total = {total_text}, expected = {expected_total}"

            logger.info(f"PASS: {test_case['TestID']}")
            return "PASS"

        except AssertionError as e:
            logger.error(f"FAIL: {test_case['TestID']} - {str(e)}")
            return "FAIL"
        except Exception as e:
            logger.error(f"ERROR: {test_case['TestID']} - {str(e)}")
            return "ERROR"

    def test_TC_002_005(self, test_case: Dict):
        """ECP - Low Price Items"""
        logger.info(f"Running {test_case['TestID']}: {test_case['Description']}")

        try:
            self.driver.get(self.BASE_URL)

            product_id = test_case['Product_IDs']
            quantity = int(test_case['Product_Quantities'])

            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-id="{product_id}"]'))
            )

            logger.info(f"Adding product {product_id} (Bubble Gums) x{quantity} to cart")
            for _ in range(quantity):
                element.click()

            self.driver.get(self.BASKET_URL)

            total_text = self.get_total_from_basket()
            logger.info(f"Total displayed: {total_text}")

            expected_total = test_case['Expected_Total']
            assert total_text == expected_total, f"FAIL: Total = {total_text}, expected = {expected_total}"

            logger.info(f"PASS: {test_case['TestID']}")
            return "PASS"

        except AssertionError as e:
            logger.error(f"FAIL: {test_case['TestID']} - {str(e)}")
            return "FAIL"
        except Exception as e:
            logger.error(f"ERROR: {test_case['TestID']} - {str(e)}")
            return "ERROR"

    def test_TC_002_006(self, test_case: Dict):
        """DTT - Formula: 1 Item, Total = Price × 1"""
        logger.info(f"Running {test_case['TestID']}: {test_case['Description']}")

        try:
            self.driver.get(self.BASE_URL)

            product_id = test_case['Product_IDs']
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-id="{product_id}"]'))
            )
            element.click()
            product_price = float(element.get_attribute("data-price"))

            self.driver.get(self.BASKET_URL)

            price_element = self.driver.find_element(By.CSS_SELECTOR, "#basketItems li span.text-muted")
            qty_element = self.driver.find_element(By.CSS_SELECTOR, "#basketItems li small.text-muted")
            total_text = self.get_total_from_basket()

            price_val = float(price_element.text.strip().replace("£", ""))
            qty_val = int(qty_element.text.strip().replace("x ", ""))

            expected_total = f"£{product_price:.2f}"

            logger.info(f"Price: {price_val}, Quantity: {qty_val}, Total: {total_text}")
            assert total_text == expected_total, f"FAIL: Total = {total_text}, expected = {expected_total}"

            logger.info(f"PASS: {test_case['TestID']}")
            return "PASS"

        except AssertionError as e:
            logger.error(f"FAIL: {test_case['TestID']} - {str(e)}")
            return "FAIL"
        except Exception as e:
            logger.error(f"ERROR: {test_case['TestID']} - {str(e)}")
            return "ERROR"

    def test_TC_002_007(self, test_case: Dict):
        """DTT - Formula: Multi-Type, Total = Σ(Price × Qty)"""
        logger.info(f"Running {test_case['TestID']}: {test_case['Description']}")

        try:
            self.driver.get(self.BASE_URL)

            for i in range(1, 11):
                element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-id="{i}"]'))
                )
                product_name = element.get_attribute("data-name")
                logger.info(f"Adding product {i} - {product_name} to cart")
                element.click()

            self.driver.get(self.BASKET_URL)

            items = self.driver.find_elements(By.CSS_SELECTOR, "#basketItems li.list-group-item.d-flex.justify-content-between.lh-condensed")

            calc_total = 0.0
            for item in items:
                qty_text = item.find_element(By.CSS_SELECTOR, "small.text-muted").text.strip().replace("x ", "")
                price_text = item.find_element(By.CSS_SELECTOR, "span.text-muted").text.strip()
                qty_val = int(qty_text)
                price_val = float(price_text.replace("£", ""))
                calc_total += qty_val * price_val
                logger.info(f"Item: qty={qty_val}, price={price_val}")

            total_text = self.get_total_from_basket()
            expected_total = f"£{calc_total:.2f}"

            logger.info(f"Calculated total: {expected_total}, Displayed total: {total_text}")
            assert total_text == expected_total, f"FAIL: Total = {total_text}, expected = {expected_total}"

            logger.info(f"PASS: {test_case['TestID']}")
            return "PASS"

        except AssertionError as e:
            logger.error(f"FAIL: {test_case['TestID']} - {str(e)}")
            return "FAIL"
        except Exception as e:
            logger.error(f"ERROR: {test_case['TestID']} - {str(e)}")
            return "ERROR"

    def test_TC_002_008(self, test_case: Dict):
        """Use-Case - Delete item: Total price updates correctly"""
        logger.info(f"Running {test_case['TestID']}: {test_case['Description']}")

        try:
            self.driver.get(self.BASE_URL)

            for i in range(1, 4):
                element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-id="{i}"]'))
                )
                product_name = element.get_attribute("data-name")
                logger.info(f"Adding product {product_name} (id={i}) to cart")
                element.click()

            self.driver.get(self.BASKET_URL)

            total_before_text = self.get_total_from_basket()
            total_before_val = float(total_before_text.replace("£", ""))
            logger.info(f"Total before delete: {total_before_val}")

            basket_items = self.driver.find_elements(By.CSS_SELECTOR, "#basketItems li.list-group-item.d-flex.justify-content-between.lh-condensed")
            target_item = None
            for item in basket_items:
                name = item.find_element(By.CSS_SELECTOR, "h6.my-0").text.strip()
                if name == "Sherbet Discs":
                    target_item = item
                    break

            assert target_item is not None, "FAIL: Sherbet Discs not found in cart"

            qty_text = target_item.find_element(By.CSS_SELECTOR, "small.text-muted").text.strip().replace("x ", "")
            price_text = target_item.find_element(By.CSS_SELECTOR, "span.text-muted").text.strip()
            qty_val = int(qty_text)
            price_val = float(price_text.replace("£", ""))
            logger.info(f"Sherbet Discs: qty={qty_val}, price={price_val}")

            delete_link = target_item.find_element(By.CSS_SELECTOR, "a.small")
            delete_link.click()

            alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert.accept()

            total_after_text = self.get_total_from_basket()
            total_after_val = float(total_after_text.replace("£", ""))
            logger.info(f"Total after delete: {total_after_val}")

            expected_total = round(total_before_val - (price_val * qty_val), 2)

            assert round(total_after_val, 2) == expected_total, f"FAIL: Total after delete = {total_after_val}, expected = {expected_total}"

            logger.info(f"PASS: {test_case['TestID']}")
            return "PASS"

        except AssertionError as e:
            logger.error(f"FAIL: {test_case['TestID']} - {str(e)}")
            return "FAIL"
        except Exception as e:
            logger.error(f"ERROR: {test_case['TestID']} - {str(e)}")
            return "ERROR"

    def test_TC_002_009(self, test_case: Dict):
        """Use-Case - Standard Shipping: Add shipping fee"""
        logger.info(f"Running {test_case['TestID']}: {test_case['Description']}")

        try:
            self.driver.get(self.BASE_URL)

            product_id = test_case['Product_IDs']
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-id="{product_id}"]'))
            )
            element.click()

            self.driver.get(self.BASKET_URL)

            shipping_option = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//label[contains(text(),"Standard Shipping (£1.99)")]'))
            )
            shipping_option.click()

            total_text = self.get_total_from_basket()
            logger.info(f"Total with shipping: {total_text}")

            expected_total = test_case['Expected_Total']
            assert total_text == expected_total, f"FAIL: Total = {total_text}, expected = {expected_total}"

            logger.info(f"PASS: {test_case['TestID']}")
            return "PASS"

        except AssertionError as e:
            logger.error(f"FAIL: {test_case['TestID']} - {str(e)}")
            return "FAIL"
        except Exception as e:
            logger.error(f"ERROR: {test_case['TestID']} - {str(e)}")
            return "ERROR"

    def run_all_tests(self):
        """Run all test cases from CSV"""
        test_data = self.load_test_data()

        print("=" * 80)
        print("CART CALCULATION - TEST EXECUTION")
        print("=" * 80)

        for test_case in test_data:
            test_id = test_case['TestID']

            self.clear_cart()

            test_method_name = f"test_{test_id}"
            test_method = getattr(self, test_method_name, None)

            if test_method:
                result = test_method(test_case)
            else:
                logger.warning(f"Test method {test_method_name} not found")
                result = "SKIP"

            self.test_results.append({
                'TestID': test_id,
                'Description': test_case['Description'],
                'Expected': test_case['Expected_Result'],
                'Actual': result,
                'Status': 'PASS' if result == test_case['Expected_Result'] else 'FAIL'
            })

            print("-" * 80)

        self.print_summary()

    def print_summary(self):
        """Print test execution summary"""
        print("\n" + "=" * 80)
        print("TEST EXECUTION SUMMARY")
        print("=" * 80)

        for result in self.test_results:
            status_symbol = "✓" if result['Status'] == 'PASS' else "✗"
            print(f"{status_symbol} {result['TestID']}: {result['Description']}")
            print(f"  Expected: {result['Expected']} | Actual: {result['Actual']} | Status: {result['Status']}")

        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r['Status'] == 'PASS')
        failed = total - passed

        print("=" * 80)
        print(f"Total: {total} | Passed: {passed} | Failed: {failed}")
        print(f"Pass Rate: {(passed/total*100):.2f}%")
        print("=" * 80)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"test_report_{timestamp}.txt"

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("CART CALCULATION - TEST EXECUTION REPORT\n")
            f.write("=" * 80 + "\n\n")
            for result in self.test_results:
                f.write(f"{result['TestID']}: {result['Description']}\n")
                f.write(f"Expected: {result['Expected']} | Actual: {result['Actual']} | Status: {result['Status']}\n\n")
            f.write("=" * 80 + "\n")
            f.write(f"Total: {total} | Passed: {passed} | Failed: {failed}\n")
            f.write(f"Pass Rate: {(passed/total*100):.2f}%\n")

        logger.info(f"Test report saved to {report_file}")


def main():
    """Main function to run tests"""
    test = CartCalculationTest()

    try:
        test.setup()
        test.run_all_tests()
    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        test.teardown()


if __name__ == "__main__":
    main()
