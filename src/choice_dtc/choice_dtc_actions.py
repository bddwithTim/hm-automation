import time

from logging import getLogger

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException

import src.lib.base as base

from src.choice_dtc.demographics import Demographics
from src.choice_dtc.browser import Browser
from src.choice_dtc.quotes import Quotes
from src.utils.util import lob_clean_state, compare_values

LOCATOR_TYPE = ['css selector', 'xpath', 'id', 'name', 'class name', 'link text', 'partial link text']


class ChoiceDTCActions:
    """Action Class contains all the action methods to test the Application"""

    def __init__(self, test_name: str, driver: webdriver):
        self.test_name = test_name
        self.test_type = None
        self.log = getLogger(test_name + ".Actions")
        self.driver = driver
        self.rest = WebDriverWait(self.driver, timeout=30)
        self.plan = None
        self.plan_dom = None
        self.plan_page = 0
        self.plan_found = False
        self.capture_ = {}
        self.uid = None
        self.browser = Browser(self.test_name, self.driver)
        self.demographics = Demographics(self.test_name, self.driver)
        self.quotes = Quotes(self.test_name, self.driver)

    def get_url(self, page_title: str, url, clear_cookie=True) -> None:
        """Open an absolute URL."""
        log = getLogger(f"{self.test_name}.get_url")
        log.info(f"Param page title: {page_title}")
        log.info(f"Param url: {url}")
        if clear_cookie and base.config['execution'] == 'local':
            self.driver.delete_all_cookies()
            self.driver.refresh()
        self.driver.get(url)

    def click(self, element_description, element_value, locator_type: str = 'css selector') -> None:
        log = getLogger(f'{self.test_name}.click')
        log.info(f"Param element_description: {element_description}")
        web_element = self.browser.wait_for_element_to_be_clickable(element_value, locator_type)
        time.sleep(0.8)
        web_element.click()

    def double_click(self, element_description, element_value, locator_type: str = 'css selector') -> None:
        # TODO: Implement double click
        pass

    def enter(self, data, web_element, mask=False, locator_type: str = 'css selector'):
        log = getLogger(f'{self.test_name}.enter')
        if mask:
            data = data[-4:].rjust(len(data), "*")
        log.info(f"Param data: {data}")
        element = self.browser.get_web_element(web_element, locator_type)
        element.send_keys(f'{Keys.CONTROL}A{Keys.DELETE}')
        element.send_keys(data)

    def hover(self, element_description: str, web_element: WebElement):
        log = getLogger(f'{self.test_name}.hover')
        log.info(f"Param element_description: {element_description}")
        self.browser.scroll_to_element(web_element)

    def wait(self, timeout: float):
        log = getLogger(f'{self.test_name}.wait')
        log.info(f"Wait: {timeout} second(s)")
        time.sleep(timeout)

    def verify_page_loaded(self, page_description: str, page_title: str,
                           timeout: int = 30) -> None:
        self.browser.verify_page_is_displayed(page_description, page_title, timeout)

    def verify_modal_displayed(self, insurance_type: str, modal_title: str = None,
                               timeout: int = 30) -> None:
        if 'short term' in insurance_type.lower() or 'supplemental' in insurance_type.lower():
            return
        self.browser.is_modal_displayed(modal_title, timeout)

    def close_modal(self, insurance_type: str) -> None:
        if 'short term' in insurance_type.lower() or 'supplemental' in insurance_type.lower():
            return
        self.browser.close_modal()

    def switch(self, frame_description: str, frame_value: str, locator_type: str = 'css selector') -> None:
        # TODO: Implement switching of tabs
        pass

    def input_demographics(self, insurance_type: str, phone: str = None, email: str = None,
                           first_name: str = None, last_name: str = None,
                           date_of_birth: str = None, gender: str = None,
                           tobacco: str = None, parent: str = None,
                           annual_income: str = None, household_members: str = None,
                           medicare_coverage_year: str = None, locator_type: str = 'xpath') -> None:
        """
        Input demographics details 
        """
        log = getLogger(f'{self.test_name}.input_demographics')
        log.info(f'Inputting demographics for {insurance_type}')
        if locator_type not in LOCATOR_TYPE:
            log.error(f'Locator type: {locator_type} is invalid. Valid values: {LOCATOR_TYPE}')
            assert False, f'Locator type: {locator_type} is invalid. Valid values: {LOCATOR_TYPE}'
        self.demographics.fill_out_details(insurance_type, phone=phone, email=email, first_name=first_name,
                                           last_name=last_name, date_of_birth=date_of_birth, gender=gender,
                                           tobacco=tobacco, parent=parent, annual_income=annual_income,
                                           household_members=household_members,
                                           medicare_coverage_year=medicare_coverage_year,
                                           locator_type=locator_type)

    def verify_text(self, text: str, description: str = None, timeout: int = 20) -> None:
        log = getLogger(f'{self.test_name}.verify_text')
        log.info(f'param text = {text}')
        log.info(f'param description = {description}')
        self.rest = WebDriverWait(self.driver, timeout=timeout)
        web_element = None
        try:
            web_element = self.rest.until(ec.visibility_of_element_located(
                (By.XPATH, f'//*[contains(text(), "{text}")]'))
            )
        except TimeoutException:
            assert text, web_element.text

    def lob_default_state(self, driver: webdriver) -> None:
        browser = Browser('lob_default_state', driver)
        browser.verify_page_is_displayed('Landing Page', 'HealthMarkets Marketplace',
                                         timeout=30)
        try:
            modal = WebDriverWait(driver, timeout=2).until(ec.presence_of_element_located(
                (By.XPATH, "//div[@class='MuiDialogContent-root']")))
            # if 'Warning!' modal is displayed in landing page, click continue button
            if 'Warning!' in modal.text:
                self.click('Continue button', "//span[contains(text(),'Continue')]", locator_type='xpath')
        except TimeoutException:
            # indicates no modal is displayed
            pass
        lob_clean_state(driver)

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
        self.browser.select_county(county, county_selection, timeout)

    def get_most_popular_plans(self, plan_name: str, file_name: str, timeout: int = 30) -> None:
        """Gets the images of the most popular plans and save it in the images directory"""
        self.quotes.get_most_popular_plans(plan_name, file_name, timeout)

    def get_plan_with_popular_ribbon(self, timeout: int = 30) -> None:
        """Gets the images of the plans with popular ribbon and save it in the images directory"""
        self.quotes.get_plan_with_popular_ribbon(timeout)

    def get_plans(self, plan_name: str, file_name: str, timeout: int = 30) -> None:
        """Gets the images of the plans and save it in the images directory"""
        self.quotes.get_plans(plan_name, file_name, timeout)

    def compare(self, expected: str, actual: str) -> None:
        """ Compares the expected and actual values """
        compare_values(expected, actual)

    def verify_plan_id(self, plan_id) -> None:
        """ Verifies the correct plan id is selected """
        self.quotes.verify_plan_id(plan_id)
