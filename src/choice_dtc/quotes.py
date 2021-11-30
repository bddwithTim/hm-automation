import traceback

from logging import getLogger

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException

from src.choice_dtc.browser import Browser


class Quotes:
    """
    Utility class for handling Quotes page actions.
    """

    def __init__(self, test_name, driver: WebDriver) -> None:
        self.test_name = test_name
        self.driver = driver
        self.rest = WebDriverWait(self.driver, 30)
        self.browser = Browser(self.test_name, self.driver)

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
        plan_container = self._get_plan_container(plan_name, timeout)
        plan_container.find_element_by_xpath("//a[text()='See Plan Details']").click()

    def _click_compare_plans(self, plan_name: str, timeout: int) -> None:
        plan_container = self._get_plan_container(plan_name, timeout)
        # click the plan container for "compare" to be visible
        plan_container.click()
        plan_container.find_element_by_xpath("//span[text()='Compare']").click()

    def click_add_to_cart(self, plan_name: str, timeout: int) -> None:
        plan_container = self._get_plan_container(plan_name, timeout)
        plan_container.find_element_by_xpath("//span[text()='Add To Cart']").click()

    def _get_plan_container(self, plan_name: str, timeout: int):
        log = getLogger(f'{self.test_name}._get_plan_container')
        plan_titles = self.browser.get_web_elements(
            "//div[@class = 'MuiTypography-root MuiTypography-h6 MuiTypography-colorTextPrimary']",
            locator_type='xpath',
            timeout=timeout
        )
        for plan_title in plan_titles:
            if plan_name in plan_title.text.replace('\n', ' '):
                return plan_title.find_element_by_xpath("..")
        log.error(f'Plan {plan_name} not found')
        assert False, f'Plan {plan_name} not found'
