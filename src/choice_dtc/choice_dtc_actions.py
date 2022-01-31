from logging import getLogger

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

from src.lib.browser import Browser
from src.choice_dtc.census import Census
from src.choice_dtc.demographics import Demographics
from src.choice_dtc.modal import Modal
from src.choice_dtc.quotes import Quotes
from src.utils.util import compare_values

LOCATOR_TYPE = ["css selector", "xpath", "id", "name", "class name", "link text", "partial link text"]


class ChoiceDTCActions:
    """Action Class contains all the action methods to test the Application"""

    def __init__(self, test_name: str, driver: webdriver):
        self.test_name = test_name
        self.driver = driver
        self.browser = Browser(self.test_name, self.driver)
        self.census = Census(self.test_name, self.driver)
        self.demographics = Demographics(self.test_name, self.driver)
        self.quotes = Quotes(self.test_name, self.driver)
        self.modal = Modal(self.test_name, self.driver)

    def get_url(self, page_title: str, url: str, clear_cookie: bool = True) -> None:
        """Open an absolute URL."""
        self.browser.get_url(page_title, url, clear_cookie)

    def click(self, element_description: str, element_value: str, locator_type: str = "css selector") -> None:
        """Performs a click operation on the element."""
        self.browser.click(element_description, element_value, locator_type)

    def double_click(self, element_description: str, element_value: str, locator_type: str = "css selector") -> None:
        """Performs a double click operation on the element."""
        self.browser.double_click(element_description, element_value, locator_type)

    def enter(self, data: str, web_element: str, mask: bool = False, locator_type: str = "css selector"):
        """ Performs a send_keys operation on the element."""
        self.browser.enter(data, web_element, mask, locator_type)

    def hover(self, element_description: str, web_element: WebElement):
        """Performs a mouse hover operation on the element."""
        self.browser.hover(element_description, web_element)

    def wait(self, timeout: float):
        """ Waits for timeout seconds"""
        self.browser.wait(timeout)

    def verify_page_loaded(self, page_description: str, page_title: str, timeout: int = 30) -> None:
        self.browser.verify_page_is_displayed(page_description, page_title, timeout)

    def verify_modal_displayed(self, insurance_type: str, modal_title: str = None, timeout: int = 30) -> None:
        """Verifies that a modal is displayed."""

        # STM and supplemental doesn't have modals
        if "short term" in insurance_type.lower() or "supplemental" in insurance_type.lower():
            return
        self.modal.is_modal_displayed(modal_title, timeout)

    def close_modal(self, insurance_type: str) -> None:
        """Closes the modal."""

        # STM and supplemental doesn't have modals
        if "short term" in insurance_type.lower() or "supplemental" in insurance_type.lower():
            return
        self.modal.close_modal()

    def switch(self, frame_description: str, frame_value: str, locator_type: str = "css selector") -> None:
        # TODO: Implement switching of tabs
        pass

    def lob_default_state(self, driver):
        """Ensures Census page is at default state"""
        self.census.lob_default_state(driver)

    def input_demographics(
        self,
        insurance_type: str,
        phone: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
        date_of_birth: str = None,
        gender: str = None,
        tobacco: str = None,
        parent: str = None,
        annual_income: str = None,
        household_members: str = None,
        medicare_coverage_year: str = None,
        locator_type: str = "xpath",
    ) -> None:
        """
        Input demographics details
        """
        log = getLogger(f"{self.test_name}.input_demographics")
        log.info(f"Inputting demographics for {insurance_type}")
        if locator_type not in LOCATOR_TYPE:
            log.error(f"Locator type: {locator_type} is invalid. Valid values: {LOCATOR_TYPE}")
            assert False, f"Locator type: {locator_type} is invalid. Valid values: {LOCATOR_TYPE}"
        self.demographics.fill_out_details(
            insurance_type,
            phone=phone,
            email=email,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            gender=gender,
            tobacco=tobacco,
            parent=parent,
            annual_income=annual_income,
            household_members=household_members,
            medicare_coverage_year=medicare_coverage_year,
            locator_type=locator_type,
        )

    def verify_text(self, text: str, description: str = None, timeout: int = 20) -> None:
        """Verifies that the text is present in the page."""
        self.browser.verify_text(text, description, timeout)

    def wait_plans_to_load(self, timeout: int = 60) -> None:
        self.quotes.wait_for_plans_to_load(timeout)

    def select_plan(self, plan_name: str, action: str, timeout: int = 30) -> None:
        """
        action values:
        - "see plan details"
        - "compare plans"
        - "add to cart"
        """
        self.quotes.plan_selection(plan_name, action, timeout)

    def select_county(self, county: str, county_selection: str, timeout: int = 10) -> None:
        """Checks if county selection is displayed and selects county"""
        self.census.select_county(county, county_selection, timeout)

    def get_plan_with_popular_ribbon(self, timeout: int = 30) -> None:
        """Gets the images of the plans with popular ribbon and save it in the images directory"""
        self.quotes.get_plan_with_popular_ribbon(timeout)

    def get_plans(self, plan_name: str, file_name: str, timeout: int = 30) -> None:
        """Gets the images of the plans and save it in the images directory"""
        self.quotes.get_plans(plan_name, file_name, timeout)

    def compare(self, expected: str, actual: str) -> None:
        """ Compares the expected and actual values """
        compare_values(expected, actual)

    def verify_plan_id(self, plan_id: str) -> None:
        """ Verifies the correct plan id is selected """
        self.quotes.verify_plan_id(plan_id)
