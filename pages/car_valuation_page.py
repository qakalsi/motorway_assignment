from playwright.sync_api import Page, expect


class CarValuationPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://motorway.co.uk/"
        self.search_box = "input[name='vrm-input']"  # Adjust if needed
        self.car_details = '[data-cy="vehicleMakeAndModel"]'  # Adjust selector if needed


    def open(self):
        """Open Motorway car valuation website"""
        self.page.goto(self.url)
        expect(self.page).to_have_url(self.url)

    def search_vehicle(self, reg_number):
        """Enter vehicle registration number and search"""
        self.page.wait_for_selector(self.search_box, state="visible", timeout=5000)  # Ensure it's visible
        self.page.fill(self.search_box, "")
        self.page.fill(self.search_box, reg_number)
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(5000)  # Allow time for navigation


    def get_vehicle_details(self):
        """Scrape vehicle details from the results page"""
        try:
            carDet = self.page.text_content(self.car_details).strip()
            print("car mayank" + carDet)
            return self.page.text_content(self.car_details).strip()

        except:
            return "Not Found"
        
    def reset_page(self):
        """Go back to the home page"""
        self.page.goto(self.url)

