import pytest
import re
import pandas as pd
from playwright.sync_api import sync_playwright
# from pages.car_valuation_page import CarValuationPage
import sys
import os

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pages.car_valuation_page import CarValuationPage



@pytest.fixture(scope="class")
def setup(request):
    """Setup Playwright browser for tests"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Use headless mode
        context = browser.new_context()
        page = context.new_page()
        car_page = CarValuationPage(page)

        request.cls.page = car_page
        request.cls.browser = browser
        request.cls.context = context
        request.cls.page_obj = page
        car_page.open()

        yield

        browser.close()


@pytest.mark.usefixtures("setup")
class TestCarValuation:
    """Test class for car valuation automation"""

    def extract_registration_numbers(self, file_path):
        """Read file and extract vehicle registration numbers"""
        with open(file_path, "r") as file:
            text = file.read()
        pattern = r"[A-Z]{2}\d{2} [A-Z]{3}"
        return re.findall(pattern, text)

    def compare_results(self, fetched_data, expected_file):
        """Compare fetched data with expected results"""
        expected_df = pd.read_csv(expected_file)
        print("\nEXPECTED DATAFRAME:\n", expected_df)  # Debugging

        expected_df.set_index("VARIANT_REG", inplace=True)  # Correcting the index

        mismatches = []
        for reg, fetched_details in fetched_data.items():
            expected_details = expected_df.loc[reg, "MAKE_MODEL"] if reg in expected_df.index else "Not Found"
            print(f"Expected: {expected_details}, Fetched: {fetched_details}")  # Debugging

            if fetched_details.strip() != expected_details.strip():
                mismatches.append(f"Mismatch for {reg}: Expected={expected_details}, Fetched={fetched_details}")

        assert not mismatches, "\n".join(mismatches)

    def test_vehicle_details(self):
        """Test vehicle valuation lookup and validation"""
        reg_numbers = self.extract_registration_numbers("car_input.txt")
        fetched_data = {}

        for reg in reg_numbers:
            print(f"Processing: {reg}")  # Debugging
            
            self.page.search_vehicle(reg)  # Search for the vehicle
            
            fetched_data[reg] = self.page.get_vehicle_details()  # Get details
            print(f"Fetched: {fetched_data[reg]}")  # Debugging
            
            self.page.open()  # Go back to the home page before next search
            
        self.compare_results(fetched_data, "car_output.txt")

