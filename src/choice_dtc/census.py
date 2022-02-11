from logging import getLogger

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from src.lib.browser import Browser


class Census:
    """
    Utility class for handling census/landing page operations
    """

    def __init__(self, test_name: str, driver: webdriver) -> None:
        self.test_name = test_name
        self.driver = driver
        self.browser = Browser(self.test_name, self.driver)

    def lob_default_state(self, driver: webdriver) -> None:
        log = getLogger(f"{self.test_name}.lob_default_state")
        log.info("Ensuring census page is in default state")
        browser = Browser("lob_default_state", driver)
        browser.verify_page_is_displayed("Landing Page", "HealthMarkets Marketplace", timeout=30)
        try:
            modal = WebDriverWait(driver, timeout=2).until(
                ec.presence_of_element_located((By.XPATH, "//div[@class='MuiDialogContent-root']"))
            )
            # if 'Warning!' modal is displayed in landing page, click continue button
            if "Warning!" in modal.text:
                self.browser.click("Continue button", "//span[contains(text(),'Continue')]", locator_type="xpath")
        except TimeoutException:
            # indicates no modal is displayed
            pass
        self.lob_clean_state(driver)

    def lob_clean_state(self, driver) -> None:
        log = getLogger(f"{self.test_name}.lob_clean_state")
        log.info("Ensuring LOBs are in default state")
        browser = Browser("lob_clean_state", driver)
        lob_list = [
            "Medicare Insurance",
            "Short Term Health Insurance",
            "ACA Health Insurance",
            "Dental Insurance",
            "Vision Insurance",
            "Supplemental Insurance",
        ]
        for lob in lob_list:
            lob_element = browser.get_web_element(f"//h6[text() = '{lob}']", locator_type="xpath")
            # if lob is already on a checked state, uncheck it.
            if "font-weight: bold" in lob_element.get_attribute("style"):
                lob_element.click()

    def select_county(self, county: str, county_selection: str, timeout: int) -> None:
        log = getLogger(f"{self.test_name}.select_county")
        log.info(f"Param county: {county}")
        log.info(f"Param county_selection: {county_selection}")
        if county_selection.lower() == "nan":  # Excel returns `Nan` for empty cell
            return
        county_dropdown = self.browser.get_web_element("//div[@id='county']", locator_type="xpath", timeout=timeout)
        county_dropdown.click()
        county = self.browser.get_web_element(
            f"//li[contains(text(), '{county_selection}')]", locator_type="xpath", timeout=timeout
        )
        county.click()
