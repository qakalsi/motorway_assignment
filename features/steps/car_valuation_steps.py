import time
import pandas as pd
import re
from playwright.sync_api import sync_playwright
from pages.car_valuation_page import CarValuationPage
from behave import given, when, then


@given("I open the car valuation website")
def open_valuation_website(context):
    """Setup Playwright browser"""
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=False)
    context.page = context.browser.new_page()
    context.car_page = CarValuationPage(context.page)
    context.car_page.open()


@when('I enter "{registration_number}"')
def enter_registration_number(context, registration_number):
    context.car_page.search_vehicle(registration_number)
    time.sleep(2)
    context.fetched_details = context.car_page.get_vehicle_details()


@then('I should see the vehicle details "{expected_details}"')
def validate_vehicle_details(context, expected_details):
    print("expected_details}"+expected_details)
    assert context.fetched_details == expected_details, (
        f"Mismatch: Expected={expected_details}, Fetched={context.fetched_details}"
    )
    context.browser.close()
    context.playwright.stop()
