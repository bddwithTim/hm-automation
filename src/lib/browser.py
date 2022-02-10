import traceback
import time

from typing import List
from logging import getLogger

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException

from src.utils.utils import get_config

LOCATOR_TYPE = ["css selector", "xpath", "id", "name", "class name", "link text", "partial link text"]


class Browser:
    """
    Utility class for handling Browser operations.
    """

    def __init__(self, test_name: str, driver: WebDriver) -> None:
        self.test_name = test_name
        self.driver = driver
        self.rest = WebDriverWait(self.driver, 30)

    def get_url(self, page_title: str, url: str, clear_cookie: bool) -> None:
        """Open an absolute URL."""
        data = get_config("config.yaml")
        log = getLogger(f"{self.test_name}.get_url")
        log.info(f"Param page title: {page_title}")
        log.info(f"Param url: {url}")
        if clear_cookie and data["execution_mode"] == "local":
            self.driver.delete_all_cookies()
            self.driver.refresh()
        self.driver.get(url)

    def click(self, element_description: str, element_value: str, locator_type: str) -> None:
        log = getLogger(f"{self.test_name}.click")
        log.info(f"Param element_description: {element_description}")
        web_element = self.wait_for_element_to_be_clickable(element_value, locator_type)
        time.sleep(0.8)
        web_element.click()

    def double_click(self, element_description: str, element_value: str, locator_type: str) -> None:
        # performs double click on the element
        log = getLogger(f"{self.test_name}.double_click")
        log.info(f"Param element_description: {element_description}")
        web_element = self.wait_for_element_to_be_clickable(element_value, locator_type)
        self.scroll_to_element(web_element)
        action = ActionChains(self.driver)
        action.double_click(web_element).perform()

    def enter(self, data: str, web_element: str, mask: bool, locator_type: str) -> None:
        log = getLogger(f"{self.test_name}.enter")
        if mask:
            data = data[-4:].rjust(len(data), "*")
        log.info(f"Param data: {data}")
        element = self.get_web_element(web_element, locator_type)
        element.send_keys(f"{Keys.CONTROL}A{Keys.DELETE}")
        element.send_keys(data)

    def hover(self, element_description: str, web_element: WebElement):
        log = getLogger(f"{self.test_name}.hover")
        log.info(f"Param element_description: {element_description}")
        self.scroll_to_element(web_element)

    def wait(self, timeout: float):
        log = getLogger(f"{self.test_name}.wait")
        log.info(f"Wait: {timeout} second(s)")
        time.sleep(timeout)

    def get_web_element(self, element: str, locator_type: str = "css selector", timeout: int = 30) -> WebElement:
        """
        Get the element using the locators css, xpath, id, name, class, link text, partial link text
        default locator type is 'css selector'

        :param element: element to find
        :param locator_type: The values can be any of the following:
            'css selector',
            'xpath',
            'id',
            'name',
            'class name',
            'link text',
            'partial link text'
        :param timeout: timeout to wait for element to be found
        :return: WebElement
        """
        log = getLogger(f"{self.test_name}.get_web_element")
        log.info(f"Param element: {element}")
        log.info(f"Param locator_type: {locator_type}")
        if locator_type not in LOCATOR_TYPE:
            log.error(f"Locator type: {locator_type} is invalid. Valid values: {LOCATOR_TYPE}")
            assert False, f"Locator type: {locator_type} is invalid. Valid values: {LOCATOR_TYPE}"

        self.rest = WebDriverWait(self.driver, timeout)
        try:
            return self.rest.until(ec.presence_of_element_located((locator_type, element)))
        except TimeoutException:
            log.error(f"web element '{element}' not found within timeout: {timeout} second(s)")
            assert False, f"web element '{element}' not found within timeout: {timeout} second(s)"

    def get_web_elements(self, element: str, locator_type: str = "css selector", timeout: int = 30) -> List[WebElement]:
        log = getLogger(f"{self.test_name}.get_web_elements")
        log.info(f"Param element: {element}")
        log.info(f"Param locator_type: {locator_type}")
        if locator_type not in LOCATOR_TYPE:
            log.error(f"Locator type: {locator_type} is invalid. Valid values: {LOCATOR_TYPE}")
            assert False, f"Locator type: {locator_type} is invalid. Valid values: {LOCATOR_TYPE}"

        self.rest = WebDriverWait(self.driver, timeout)
        try:
            return self.rest.until(ec.presence_of_all_elements_located((locator_type, element)))
        except TimeoutException:
            log.error(f"web element '{element}' not found within timeout: {timeout} second(s)")
            assert False, f"web element '{element}' not found within timeout: {timeout} second(s)"

    def wait_for_element_to_be_clickable(
        self, element: str, locator_type: str = "css selector", timeout: int = 30
    ) -> WebElement:
        log = getLogger(f"{self.test_name}.wait_for_element_to_be_clickable")
        log.info(f"Param element: {element}")
        log.info(f"Param locator_type: {locator_type}")
        if locator_type not in LOCATOR_TYPE:
            log.error(f"Locator type: {locator_type} is invalid. Valid values: {LOCATOR_TYPE}")
            assert False, f"Locator type: {locator_type} is invalid. Valid values: {LOCATOR_TYPE}"

        self.rest = WebDriverWait(self.driver, timeout)
        try:
            return self.rest.until(ec.element_to_be_clickable((locator_type, element)))
        except TimeoutException:
            log.error(traceback.format_exc())
            assert False, f"web element '{element}' not found"

    def verify_page_is_displayed(self, page_description, page_title, timeout: int) -> bool:
        log = getLogger(f"{self.test_name}.verify_page_loaded")
        log.info(f"Param page_description: {page_description}")
        self.rest = WebDriverWait(self.driver, timeout)
        try:
            return bool(self.rest.until(ec.title_contains(page_title)))
        except TimeoutException:
            log.error(traceback.format_exc())
            assert 0, f"{page_description} page did not load in {timeout} seconds"

    def scroll_to_element(self, web_element) -> None:
        log = getLogger(f"{self.test_name}.scroll_to_element")
        log.info(f"Param web_element: {web_element}")
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", web_element)
        except WebDriverException:
            log.error(traceback.format_exc())
            assert False, f"Unable to scroll to the element: '{web_element}'"

    def verify_text(self, text: str, description: str, timeout: int) -> None:
        log = getLogger(f"{self.test_name}.verify_text")
        log.info(f"param text = {text}")
        log.info(f"param description = {description}")
        self.rest = WebDriverWait(self.driver, timeout=timeout)
        web_element = WebDriverWait
        try:
            web_element = self.rest.until(
                ec.visibility_of_element_located((By.XPATH, f'//*[contains(text(), "{text}")]'))
            )
        except TimeoutException:
            log.error(f"web element '{web_element}' not found within timeout: {timeout} second(s)")
            assert False, f"web element '{web_element}' not found within timeout: {timeout} second(s)"


def get_driver(browser_name: str) -> webdriver:
    data = get_config("config.yaml")
    headless = data["browser"]["headless"]
    window_size = data["browser"]["size"]
    if browser_name == "chrome":
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        if window_size:
            chrome_options.add_argument("--window-size={}".format(window_size))
        else:
            chrome_options.add_argument("--start-maximized")

        if headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--remote-debugging-port=9222")
        return webdriver.Chrome(executable_path=".\\src\\drivers\\chromedriver.exe", options=chrome_options)
    elif browser_name == "firefox":
        return webdriver.Firefox(executable_path=".\\src\\drivers\\geckodriver.exe", log_path=".\\logs\\gecko.log")
    elif browser_name == "mobile":
        mobile_emulation = {"deviceName": data["device"]}
        chrome_opts = webdriver.ChromeOptions()
        chrome_opts.add_experimental_option("mobileEmulation", mobile_emulation)
        return webdriver.Chrome(
            executable_path=".\\src\\drivers\\chromedriver.exe",
            chrome_options=chrome_opts,
            service_log_path=".\\logs\\mobile.log",
        )
    elif browser_name == "safari":
        return webdriver.Safari()
