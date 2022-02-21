from logging import getLogger
from typing import List

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from src.choice_dtc.image import ChoiceDTCImage
from src.common.browser import Browser


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
        log = getLogger(f"{self.test_name}.wait_plans_to_load")
        log.info(f"Waiting for plans to load, timeout: {timeout}")
        self.rest = WebDriverWait(self.driver, timeout)
        self.browser.verify_page_is_displayed("Quotes page", page_title="Quotes", timeout=30)
        plans = "//div[@class = 'MuiTypography-root MuiTypography-h6 MuiTypography-colorTextPrimary']"
        self.browser.get_web_elements(plans, locator_type="xpath", timeout=timeout)

    # define an async function that will check if the plans are loaded
    def _no_plans_loaded(self) -> None:
        log = getLogger(f"{self.test_name}._no_plans_loaded")
        log.info("Checking if plans are loaded")
        # checks if the text 'Call us Today!' is present within 20 seconds
        # if the text is present, it means there are no plans loaded
        self.rest = WebDriverWait(self.driver, 20)
        try:
            self.rest.until(ec.presence_of_element_located((By.XPATH, "//h6[contains(text(), 'Call us Today!')]")))
            log.info("No plans were loaded")
            assert False, "No plans were loaded"
        except TimeoutException:
            pass

    def plan_selection(self, plan_name: str, action: str, timeout: int) -> None:
        log = getLogger(f"{self.test_name}.select_plan")
        log.info(f"Plan selected {plan_name}, action taken: {action}, timeout: {timeout}")
        actions = {
            "see plan details": self._click_plan_details,
            "compare": self._click_compare_plans,
            "add to cart": self._click_add_to_cart,
        }
        if action.lower() not in actions:
            log.error(f"Action {action} not found. Valid actions are: {actions.keys()}")
            assert False, f"Action {action} not found. Valid actions are: {actions.keys()}"
        # execute action
        actions[action.lower()](plan_name, timeout)

    def _click_plan_details(self, plan_name: str, timeout: int) -> None:
        plan_index = self._get_plan_index(plan_name, timeout)
        self.browser.get_web_elements(element="//a[text()='See Plan Details']", locator_type="xpath", timeout=timeout)[
            plan_index
        ].click()

    def _click_compare_plans(self, plan_name: str, timeout: int) -> None:
        plan_index = self._get_plan_index(plan_name, timeout)
        # click the plan_container to make the 'Compare check box' visible
        plan_container = self.browser.get_web_elements(
            "//div[@class='MuiCardContent-root']", locator_type="xpath", timeout=timeout
        )[plan_index]
        plan_container.click()
        # click the visible 'Compare check box'
        compare_checkbox = "//label[contains(@style, 'opacity: 1')]"
        self.browser.get_web_elements(element=compare_checkbox, locator_type="xpath", timeout=timeout)[0].click()

    def _click_add_to_cart(self, plan_name: str, timeout: int) -> None:
        plan_index = self._get_plan_index(plan_name, timeout)
        self.browser.get_web_elements(element="//span[text()='Add To Cart']", locator_type="xpath", timeout=timeout)[
            plan_index
        ].click()

    def _get_plan_container(self, plan_name: str, timeout: int) -> List[WebElement]:
        log = getLogger(f"{self.test_name}._get_plan_container")
        plan_container = self.browser.get_web_elements(
            "//div[@class='MuiCardContent-root']", locator_type="xpath", timeout=timeout
        )
        plans = [plan for plan in plan_container if plan_name in plan.text.replace("\n", " ")]
        if not plans:
            log.error(f'"{plan_name}" plan not found')
            assert False, f'"{plan_name}" plan not found'
        return plans

    def _get_plan_index(self, string_name: str, timeout: int) -> int:
        """Gets the index of the plan that contains the string_name"""
        log = getLogger(f"{self.test_name}._get_plan_index")
        plan_container = self.browser.get_web_elements(
            "//div[@class='MuiCardContent-root']", locator_type="xpath", timeout=timeout
        )
        plans = [plan for plan in plan_container if string_name in plan.text.replace("\n", " ")]
        if not plans:
            log.error(f'"{string_name}" not found')
            assert False, f'"{string_name}" not found'
        return plan_container.index(plans[0])

    def get_plan_with_popular_ribbon(self, timeout: int) -> None:
        log = getLogger(f"{self.test_name}.get_popular_ribbon")
        log.info("Getting plan with the popular ribbon")
        # get the index of the plan that contains the text 'Most Popular'
        most_popular_index = self._get_plan_index("Most Popular", timeout)
        # get the web element that contains the text 'See Plan Details' using the index most_popular_index
        see_plan_details = self.browser.get_web_elements(
            "//a[text()='See Plan Details']", locator_type="xpath", timeout=timeout
        )[most_popular_index]
        see_plan_details.click()

    def verify_plan_id(self, plan_id: str) -> None:
        log = getLogger(f"{self.test_name}.verify_plan_id")
        log.info(f"Verifying plan id: {plan_id}")
        # check the url if it contains the text plan_id
        if plan_id not in self.driver.current_url:
            log.error(f"Plan id: {plan_id} not found in the url")
            assert False, f"Plan id: {plan_id} not found in the url"
        log.info(f'Plan id: {plan_id} found in the url "{self.driver.current_url}"')
