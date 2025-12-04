import pytest
import sys
import os
from datetime import datetime

def main():
    test_file = os.path.join(os.path.dirname(__file__), "tests", "test.py")

    reports_dir = os.path.join(os.path.dirname(__file__), "reports")
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(reports_dir, f"report_{timestamp}.html")

    print("=" * 70)
    print("BẮT ĐẦU CHẠY TEST SUITE")
    print("=" * 70)
    print(f"Test file: {test_file}")
    print(f"Report file: {report_file}")
    print("=" * 70)
    print()

    pytest_args = [
        test_file,
        "-v",
        "--html=" + report_file,
        "--self-contained-html",
        "--tb=short",
        "-s"
    ]

    exit_code = pytest.main(pytest_args)

    print()
    print("=" * 70)
    print("KẾT THÚC TEST SUITE")
    print("=" * 70)
    print(f"Exit code: {exit_code}")
    print(f"Report đã được tạo tại: {report_file}")
    print("=" * 70)

    return exit_code


def run_specific_class(test_class_name):
    test_file = os.path.join(os.path.dirname(__file__), "tests", "test.py")

    reports_dir = os.path.join(os.path.dirname(__file__), "reports")
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(reports_dir, f"report_{test_class_name}_{timestamp}.html")

    print("=" * 70)
    print(f"BẮT ĐẦU CHẠY TEST CLASS: {test_class_name}")
    print("=" * 70)
    print(f"Test file: {test_file}")
    print(f"Report file: {report_file}")
    print("=" * 70)
    print()

    pytest_args = [
        f"{test_file}::{test_class_name}",
        "-v",
        "--html=" + report_file,
        "--self-contained-html",
        "--tb=short",
        "-s"
    ]

    exit_code = pytest.main(pytest_args)

    print()
    print("=" * 70)
    print(f"KẾT THÚC TEST CLASS: {test_class_name}")
    print("=" * 70)
    print(f"Exit code: {exit_code}")
    print(f"Report đã được tạo tại: {report_file}")
    print("=" * 70)

    return exit_code


def run_specific_test(test_name):
    test_file = os.path.join(os.path.dirname(__file__), "tests", "test.py")

    reports_dir = os.path.join(os.path.dirname(__file__), "reports")
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(reports_dir, f"report_{test_name.replace('::', '_')}_{timestamp}.html")

    print("=" * 70)
    print(f"BẮT ĐẦU CHẠY TEST: {test_name}")
    print("=" * 70)
    print(f"Test file: {test_file}")
    print(f"Report file: {report_file}")
    print("=" * 70)
    print()

    pytest_args = [
        f"{test_file}::{test_name}",
        "-v",
        "--html=" + report_file,
        "--self-contained-html",
        "--tb=short",
        "-s"
    ]

    exit_code = pytest.main(pytest_args)

    print()
    print("=" * 70)
    print(f"KẾT THÚC TEST: {test_name}")
    print("=" * 70)
    print(f"Exit code: {exit_code}")
    print(f"Report đã được tạo tại: {report_file}")
    print("=" * 70)

    return exit_code


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--class":
            if len(sys.argv) > 2:
                run_specific_class(sys.argv[2])
            else:
                print("Vui lòng cung cấp tên test class. Ví dụ: python main.py --class TestAddToCart")
        elif sys.argv[1] == "--test":
            if len(sys.argv) > 2:
                run_specific_test(sys.argv[2])
            else:
                print("Vui lòng cung cấp tên test. Ví dụ: python main.py --test TestAddToCart::test_TC_001_001")
        else:
            print("Lệnh không hợp lệ. Sử dụng:")
            print("  python main.py                                    # Chạy tất cả test")
            print("  python main.py --class TestAddToCart              # Chạy một test class")
            print("  python main.py --test TestAddToCart::test_TC_001_001  # Chạy một test case")
    else:
        main()
