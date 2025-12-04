import os
from dataclasses import dataclass


@dataclass
class TestConfig:

    BROWSER: str = os.getenv("BROWSER", "chrome")
    HEADLESS: bool = os.getenv("HEADLESS", "False").lower() == "true"

    IMPLICIT_WAIT: int = int(os.getenv("IMPLICIT_WAIT", "10"))
    PAGE_LOAD_TIMEOUT: int = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))
    EXPLICIT_WAIT: int = int(os.getenv("EXPLICIT_WAIT", "10"))

    BASE_URL: str = os.getenv("BASE_URL", "https://example.com")
    LOGIN_URL: str = os.getenv("LOGIN_URL", f"{BASE_URL}/login")

    TEST_USERNAME: str = os.getenv("TEST_USERNAME", "testuser@example.com")
    TEST_PASSWORD: str = os.getenv("TEST_PASSWORD", "TestPassword123")

    SCREENSHOT_ON_FAILURE: bool = os.getenv("SCREENSHOT_ON_FAILURE", "True").lower() == "true"
    SCREENSHOT_DIR: str = os.getenv("SCREENSHOT_DIR", "./screenshots")

    REPORT_DIR: str = os.getenv("REPORT_DIR", "./reports")

    @classmethod
    def create_directories(cls):
        os.makedirs(cls.SCREENSHOT_DIR, exist_ok=True)
        os.makedirs(cls.REPORT_DIR, exist_ok=True)


config = TestConfig()
