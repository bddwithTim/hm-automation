from typing import List
from logging import getLogger
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException

from src.choice_dtc.browser import Browser
from src.choice_dtc.image import ChoiceDTCImage


class Quotes:
    """
    Utility class for handling Quotes page actions.
    """

    def __init__(self, test_name, driver: WebDriver) -> None:
        self.test_name = test_name
        self.driver = driver
        self.rest = WebDriverWait(self.driver, 30)
        self.browser = Browser(self.test_name, self.driver)
        self.image = ChoiceDTCImage(self.test_name, self.driver)

    def wait_for_plans_to_load(self, timeout: int) -> None:
        log = getLogger(f'{self.test_name}.wait_plans_to_load')
        log.info(f'Waiting for plans to load, timeout: {timeout}')
        self.rest = WebDriverWait(self.driver, timeout)
        self.browser.verify_page_is_displayed("Quotes page", page_title='Quotes', timeout=30)
        plans = "//div[@class = 'MuiTypography-root MuiTypography-h6 MuiTypography-colorTextPrimary']"
        self.browser.get_web_elements(plans, locator_type='xpath', timeout=timeout)

    # define an async function that will check if the plans are loaded
    def _no_plans_loaded(self) -> None:
        log = getLogger(f'{self.test_name}._no_plans_loaded')
        log.info('Checking if plans are loaded')
        # checks if the text 'Call us Today!' is present within 20 seconds
        # if the text is present, it means there are no plans loaded
        self.rest = WebDriverWait(self.driver, 20)
        try:
            self.rest.until(ec.presence_of_element_located((
                By.XPATH,
                "//h6[contains(text(), 'Call us Today!')]"
            )))
            log.info('No plans were loaded')
            assert False, 'No plans were loaded'
        except TimeoutException:
            pass

    def plan_selection(self, plan_name: str, action: str, timeout: int) -> None:
        log = getLogger(f'{self.test_name}.select_plan')
        log.info(f'Plan selected {plan_name}, action taken: {action}, timeout: {timeout}')
        actions = {
            'see plan details': self._click_plan_details,
            'compare': self._click_compare_plans,
            'add to cart': self.click_add_to_cart,
        }
        if action.lower() not in actions:
            log.error(f'Action {action} not found. Valid actions are: {actions.keys()}')
            assert False, f'Action {action} not found. Valid actions are: {actions.keys()}'
        # execute action
        actions[action.lower()](plan_name, timeout)

    def _click_plan_details(self, plan_name: str, timeout: int) -> None:
        # Get's the first element that contains the plan name
        plan_container = self._get_plan_container(plan_name, timeout)[0]
        plan_container.find_element_by_xpath("//a[text()='See Plan Details']").click()

    def _click_compare_plans(self, plan_name: str, timeout: int) -> None:
        # Get's the first element that contains the plan name
        plan_container = self._get_plan_container(plan_name, timeout)[0]
        # click the plan container for "compare" to be visible
        plan_container.click()
        plan_container.find_element_by_xpath("//span[text()='Compare']").click()

    def click_add_to_cart(self, plan_name: str, timeout: int) -> None:
        # Get's the first element that contains the plan name
        plan_container = self._get_plan_container(plan_name, timeout)[0]
        plan_container.find_element_by_xpath("//span[text()='Add To Cart']").click()

    def _get_plan_container(self, plan_name: str, timeout: int) -> List[WebElement]:
        log = getLogger(f'{self.test_name}._get_plan_container')
        plan_container = self.browser.get_web_elements(
            "//div[@class='MuiCardContent-root']",
            locator_type='xpath',
            timeout=timeout
        )
        plans = [
            plan
            for plan in plan_container
            if plan_name in plan.text.replace('\n', ' ')
        ]
        if not plans:
            log.error(f'"{plan_name}" plan not found')
            assert False, f'"{plan_name}" plan not found'
        return plans

    def get_most_popular_plans(self, plan_name: str, file_name: str, timeout: int) -> None:
        log = getLogger(f'{self.test_name}.get_most_popular_plans')
        log.info(f'Getting most popular plans for {plan_name}')
        plans = self._get_plan_container(plan_name, timeout)
        for plan in plans:
            plan_image = self.image.capture_image(plan)
            _file_name = f"{file_name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S.%f')[:-3]}"
            self.image.save_image(plan_image, f'{_file_name}')
            log.info(f"File name: '{_file_name} saved to directory: {self.image.image_dir}'")

    def get_plan_with_popular_ribbon(self, file_name: str, timeout: int) -> None:
        log = getLogger(f'{self.test_name}.get_popular_ribbon')
        log.info('Getting plan with the popular ribbon')
        # getting plan/s with popular ribbon
        plans = self._get_plan_container("Most Popular", timeout)
        for plan in plans:
            plan_image = self.image.capture_image(plan)
            _file_name = f"{file_name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S.%f')[:-3]}"
            self.image.save_image(plan_image, f'{_file_name}')
            log.info(f"File name: '{_file_name} saved to directory: {self.image.image_dir}'")

    def get_plans(self, plans_containing_string: str, file_name: str, timeout: int) -> None:
        log = getLogger(f'{self.test_name}.get_plans')
        log.info(f"Getting plans containing the string: '{plans_containing_string}'")
        plans = self._get_plan_container(plans_containing_string, timeout)
        if not plans:
            log.error(f"There are no plans containing the string: '{plans_containing_string}'")
            assert False, f"There are no plans containing the string: '{plans_containing_string}'"
        for plan in plans:
            plan_image = self.image.capture_image(plan)
            _file_name = f"{file_name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S.%f')[:-3]}"
            self.image.save_image(plan_image, f'{_file_name}')
            log.info(f"File name: '{_file_name} saved to directory: {self.image.image_dir}'")

    def identify_most_popular_plan(self, timeout: int) -> str:
        log = getLogger(f'{self.test_name}.identify_most_popular_plan')
        log.info('Identifying the most popular plan')
        # getting plan/s with popular ribbon
        plans = self._get_plan_container("Most Popular", timeout)
        if not plans:
            log.error('No plan with the popular ribbon found')
            assert False, 'No plan with the popular ribbon found'
        # Gets the name of the plan
        plan_name = plans[0].text.split('Deductible')[0].strip().replace('\n', ' ')
        log.info(f'Most popular plan: {plan_name}')
        return plan_name





