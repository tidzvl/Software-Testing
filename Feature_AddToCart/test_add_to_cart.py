#
# File: test_add_to_cart.py
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


class AddToCartTest:
    """Test class for Add to Cart functionality"""

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

    def test_TC_001_001(self, test_case: Dict):
        """BVA - Minimum Valid Quantity"""
        logger.info(f"Running {test_case['TestID']}: {test_case['Description']}")

        try:
            self.driver.get(self.BASE_URL)

            product_id = test_case['Product_ID']
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-id="{product_id}"]'))
            )

            logger.info(f"Adding product {product_id} to cart")
            element.click()

            badge = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".badge.badge-success"))
            )
            badge_text = badge.text.strip()
            logger.info(f"Cart badge shows: {badge_text}")

            expected_badge = test_case['Expected_Badge']
            assert badge_text == expected_badge, f"FAIL: Badge = {badge_text}, expected = {expected_badge}"

            logger.info(f"PASS: {test_case['TestID']}")
            return "PASS"

        except AssertionError as e:
            logger.error(f"FAIL: {test_case['TestID']} - {str(e)}")
            return "FAIL"
        except Exception as e:
            logger.error(f"ERROR: {test_case['TestID']} - {str(e)}")
            return "ERROR"

    def test_TC_001_002(self, test_case: Dict):
        """BVA - Maximum Valid Quantity"""
        logger.info(f"Running {test_case['TestID']}: {test_case['Description']}")

        try:
            self.driver.get(self.BASE_URL)

            product_id = test_case['Product_ID']
            add_count = int(test_case['Add_Count'])

            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-id="{product_id}"]'))
            )

            logger.info(f"Adding product {product_id} to cart {add_count} times")
            for i in range(add_count):
                element.click()
                logger.info(f"Click {i+1}/{add_count}")

            badge = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".badge.badge-success"))
            )
            badge_text = badge.text.strip()
            logger.info(f"Cart badge shows: {badge_text}")

            expected_badge = test_case['Expected_Badge']
            assert badge_text == expected_badge, f"FAIL: Badge = {badge_text}, expected = {expected_badge}"

            logger.info(f"PASS: {test_case['TestID']}")
            return "PASS"

        except AssertionError as e:
            logger.error(f"FAIL: {test_case['TestID']} - {str(e)}")
            return "FAIL"
        except Exception as e:
            logger.error(f"ERROR: {test_case['TestID']} - {str(e)}")
            return "ERROR"

    def test_TC_001_003(self, test_case: Dict):
        """ECP - Empty cart, Valid Product: Candy"""
        logger.info(f"Running {test_case['TestID']}: {test_case['Description']}")

        try:
            self.driver.get(self.BASE_URL)

            product_id = test_case['Product_ID']
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-id="{product_id}"]'))
            )

            logger.info(f"Adding product {product_id} ({test_case['Product_Name']}) to cart")
            element.click()

            badge = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".badge.badge-success"))
            )
            badge_text = badge.text.strip()
            logger.info(f"Cart badge shows: {badge_text}")

            expected_badge = test_case['Expected_Badge']
            assert badge_text == expected_badge, f"FAIL: Badge = {badge_text}, expected = {expected_badge}"

            logger.info(f"PASS: {test_case['TestID']}")
            return "PASS"

        except AssertionError as e:
            logger.error(f"FAIL: {test_case['TestID']} - {str(e)}")
            return "FAIL"
        except Exception as e:
            logger.error(f"ERROR: {test_case['TestID']} - {str(e)}")
            return "ERROR"

    def test_TC_001_004(self, test_case: Dict):
        """ECP - Add Same Product to not empty cart"""
        logger.info(f"Running {test_case['TestID']}: {test_case['Description']}")

        try:
            self.driver.get(self.BASE_URL)

            product_ids = test_case['Product_ID'].split('|')
            product_names = test_case['Product_Name'].split('|')

            for i, product_id in enumerate(product_ids):
                element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-id="{product_id}"]'))
                )
                logger.info(f"Adding product {product_id} ({product_names[i]}) to cart")
                element.click()

            logger.info("Navigating to basket page")
            self.driver.get(self.BASKET_URL)

            basket = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "basketItems"))
            )

            items = basket.find_elements(By.TAG_NAME, "li")
            product_items = items[:-1]
            count = len(product_items)

            logger.info(f"Number of products in cart: {count}")

            expected_count = int(test_case['Expected_Badge'])
            assert count == expected_count, f"FAIL: Product count = {count}, expected = {expected_count}"

            logger.info(f"PASS: {test_case['TestID']}")
            return "PASS"

        except AssertionError as e:
            logger.error(f"FAIL: {test_case['TestID']} - {str(e)}")
            return "FAIL"
        except Exception as e:
            logger.error(f"ERROR: {test_case['TestID']} - {str(e)}")
            return "ERROR"

    def test_TC_001_005(self, test_case: Dict):
        """Use-Case - Add Multiple Products"""
        return self.test_TC_001_004(test_case)

    def test_TC_001_006(self, test_case: Dict):
        """Use-Case - Clear Cart Workflow"""
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

            logger.info("Navigating to basket page")
            self.driver.get(self.BASKET_URL)

            logger.info("Clearing all products from cart")
            clear_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[onclick="emptyBasket();"]'))
            )
            clear_button.click()

            alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert.accept()

            basket = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "basketItems"))
            )

            items = basket.find_elements(By.TAG_NAME, "li")
            product_items = items[:-1]
            count = len(product_items)

            logger.info(f"Number of products in cart after clear: {count}")

            assert count == 0, f"FAIL: Product count = {count}, expected = 0"

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
        print("ADD TO CART - TEST EXECUTION")
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
            f.write("ADD TO CART - TEST EXECUTION REPORT\n")
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
    test = AddToCartTest()

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
