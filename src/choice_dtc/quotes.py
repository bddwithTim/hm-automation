import traceback
import time

from typing import List
from logging import getLogger

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

    def wait_for_plans_to_load(self, timeout: int = 30) -> None:
        log = getLogger(f'{self.test_name}.wait_plans_to_load')
        self.rest = WebDriverWait(self.driver, timeout)
        try:
            self.rest.until(ec.presence_of_all_elements_located((
                By.XPATH,
                "//div[@class = 'MuiTypography-root MuiTypography-h6 MuiTypography-colorTextPrimary']"
            )))
        except TimeoutException:
            log.error(traceback.format_exc())
            assert False, f"Plans did not load in {timeout} seconds"

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
            log.error(f'Plan {plan_name} not found')
            assert False, f'Plan {plan_name} not found'
        return plans

    def get_most_popular_plans(self, plan_name, file_name: str, timeout: int = 10) -> None:
        log = getLogger(f'{self.test_name}.get_most_popular_plans')
        log.info(f'Getting most popular plans for {plan_name}')
        plans = self._get_plan_container(plan_name, timeout)
        if not plans:
            log.error(f'Plan {plan_name} not found')
            assert False, f'Plan {plan_name} not found'
        for plan in plans:
            plan_image = self.image.capture_image(plan)
            _file_name = f'{file_name}_{time.time()}'
            self.image.save_image(plan_image, f'{_file_name}')
            log.info(f"File name: '{_file_name} saved to directory: {self.image.image_dir}'")

    def get_plans(self, plans_containing_string: str, file_name: str, timeout: int = 10) -> None:
        log = getLogger(f'{self.test_name}.get_plans')
        log.info(f"Getting plans containing the string: '{plans_containing_string}'")
        plans = self._get_plan_container(plans_containing_string, timeout)
        if not plans:
            log.error(f"There are no plans containing the string: '{plans_containing_string}'")
            assert False, f"There are no plans containing the string: '{plans_containing_string}'"
        for plan in plans:
            plan_image = self.image.capture_image(plan)
            _file_name = f'{file_name}_{time.time()}'
            self.image.save_image(plan_image, f'{_file_name}')
            log.info(f"File name: '{_file_name} saved to directory: {self.image.image_dir}'")
