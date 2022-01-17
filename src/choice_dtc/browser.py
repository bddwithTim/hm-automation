import traceback

from typing import List
from logging import getLogger

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import WebDriverException

from selenium.common.exceptions import TimeoutException

import src.lib.base as base

LOCATOR_TYPE = ['css selector', 'xpath', 'id', 'name', 'class name', 'link text', 'partial link text']


class Browser:
    """
    Utility class for handling Browser operations.
    """

    def __init__(self, test_name, driver: WebDriver) -> None:
        self.test_name = test_name
        self.driver = driver
        self.rest = WebDriverWait(self.driver, 30)

    def get_web_element(self, element: str, locator_type: str = 'css selector',
                        timeout: int = 30) -> WebElement:
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
        log = getLogger(f'{self.test_name}.get_web_element')
        log.info(f"Param element: {element}")
        log.info(f"Param locator_type: {locator_type}")
        if locator_type not in LOCATOR_TYPE:
            log.error(f'Locator type: {locator_type} is invalid. Valid values: {LOCATOR_TYPE}')
            assert False, f'Locator type: {locator_type} is invalid. Valid values: {LOCATOR_TYPE}'

        self.rest = WebDriverWait(self.driver, timeout)
        try:
            return self.rest.until(ec.presence_of_element_located((locator_type, element)))
        except TimeoutException:
            log.error(f"web element '{element}' not found within timeout: {timeout} second(s)")
            assert False, f"web element '{element}' not found within timeout: {timeout} second(s)"

    def get_web_elements(self, element: str, locator_type: str = 'css selector',
                         timeout: int = 30) -> List[WebElement]:
        log = getLogger(f'{self.test_name}.get_web_elements')
        log.info(f"Param element: {element}")
        log.info(f"Param locator_type: {locator_type}")
        if locator_type not in LOCATOR_TYPE:
            log.error(f'Locator type: {locator_type} is invalid. Valid values: {LOCATOR_TYPE}')
            assert False, f'Locator type: {locator_type} is invalid. Valid values: {LOCATOR_TYPE}'

        self.rest = WebDriverWait(self.driver, timeout)
        try:
            return self.rest.until(ec.presence_of_all_elements_located((locator_type, element)))
        except TimeoutException:
            log.error(f"web element '{element}' not found within timeout: {timeout} second(s)")
            assert False, f"web element '{element}' not found within timeout: {timeout} second(s)"

    def wait_for_element_to_be_clickable(self, element: str, locator_type: str = 'css selector',
                                         timeout: int = 30) -> WebElement:
        log = getLogger(f'{self.test_name}.wait_for_element_to_be_clickable')
        log.info(f"Param element: {element}")
        log.info(f"Param locator_type: {locator_type}")
        if locator_type not in LOCATOR_TYPE:
            log.error(f'Locator type: {locator_type} is invalid. Valid values: {LOCATOR_TYPE}')
            assert False, f'Locator type: {locator_type} is invalid. Valid values: {LOCATOR_TYPE}'

        self.rest = WebDriverWait(self.driver, timeout)
        try:
            return self.rest.until(ec.element_to_be_clickable((locator_type, element)))
        except TimeoutException:
            log.error(traceback.format_exc())
            assert False, f"web element '{element}' not found"

    def verify_page_is_displayed(self, page_description, page_title, timeout: int) -> bool:
        log = getLogger(f'{self.test_name}.verify_page_loaded')
        log.info(f"Param page_description: {page_description}")
        self.rest = WebDriverWait(self.driver, timeout)
        try:
            return bool(self.rest.until(ec.title_contains(page_title)))
        except TimeoutException:
            log.error(traceback.format_exc())
            assert 0, f"{page_description} page did not load in {timeout} seconds"

    def is_modal_displayed(self, modal_title: str = None,
                           timeout: int = 30) -> bool:
        log = getLogger(f'{self.test_name}.is_modal_displayed')
        modal = self.get_web_element("//div[@class='MuiDialogContent-root']",
                                     locator_type='xpath', timeout=timeout)
        if modal_title is None:
            return modal.is_displayed()
        if not modal:
            log.error(f"Modal '{modal_title}' not found")
            assert False, f"Modal '{modal_title}' not found"

        _modal_title = self.get_web_element(f"//*[contains(text(), '{modal_title}')]",
                                            locator_type='xpath', timeout=timeout)
        return bool(_modal_title)

    def close_modal(self) -> None:
        log = getLogger(f'{self.test_name}.close_modal')
        modal = self.get_web_element("//div[@class='MuiDialogContent-root']", locator_type='xpath')
        if modal:
            self.get_web_element('//*[@id="remove-button-icon"]', locator_type='xpath').click()
            log.info("Modal closed")

    def select_county(self, county, county_selection, timeout):
        log = getLogger(f'{self.test_name}.select_county')
        log.info(f"Param county: {county}")
        log.info(f"Param county_selection: {county_selection}")
        if county_selection.lower() == 'nan':  # Excel returns `Nan` for empty cell
            return
        county_dropdown = self.get_web_element("//div[@id='county']",
                                               locator_type='xpath', timeout=timeout)
        county_dropdown.click()
        county = self.get_web_element(f"//li[contains(text(), '{county_selection}')]",
                                      locator_type='xpath', timeout=timeout)
        county.click()

    def scroll_to_element(self, web_element) -> None:
        log = getLogger(f'{self.test_name}.scroll_to_element')
        log.info(f"Param web_element: {web_element}")
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", web_element)
        except WebDriverException:
            log.error(traceback.format_exc())
            assert False, f"Unable to scroll to the element: '{web_element}'"


def get_driver(browser_name: str = 'chrome', headless: bool = False) -> webdriver:
    if browser_name == 'chrome':
        chrome_options = ChromeOptions()
        # chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        # set headless to True to run tests in headless mode
        if headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--remote-debugging-port=9222")
        return webdriver.Chrome(executable_path='.\\src\\drivers\\chromedriver.exe',
                                options=chrome_options)
    elif browser_name == 'firefox':
        return webdriver.Firefox(executable_path=".\\src\\drivers\\geckodriver.exe",
                                 log_path='.\\logs\\gecko.log')
    elif browser_name == 'ie':
        caps = webdriver.DesiredCapabilities.INTERNETEXPLORER
        caps['ignoreProtectedModeSettings'] = True
        caps['ignoreZoomSetting'] = True
        return webdriver.Ie('.\\src\\drivers\\IEDriverServer.exe',
                            log_file=".\\logs\\ie.log", capabilities=caps)
    elif browser_name == 'mobile':
        mobile_emulation = {'deviceName': base.config['device']}
        chrome_opts = webdriver.ChromeOptions()
        chrome_opts.add_experimental_option('mobileEmulation', mobile_emulation)
        return webdriver.Chrome(executable_path='.\\src\\drivers\\chromedriver.exe',
                                chrome_options=chrome_opts, service_log_path='.\\logs\\mobile.log')
    elif browser_name == 'safari':
        return webdriver.Safari()
