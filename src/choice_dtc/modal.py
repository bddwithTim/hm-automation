from logging import getLogger

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from src.common.browser import Browser


class Modal:
    """
    Utility class for interacting with modals.
    """

    def __init__(self, test_name: str, driver: WebDriver) -> None:
        self.test_name = test_name
        self.driver = driver
        self.rest = WebDriverWait(self.driver, 30)
        self.browser = Browser(self.test_name, self.driver)

    def is_modal_displayed(self, modal_title: str = None, timeout: int = 30) -> bool:
        log = getLogger(f"{self.test_name}.is_modal_displayed")
        modal = self.browser.get_web_element(
            "//div[@class='MuiDialogContent-root']", locator_type="xpath", timeout=timeout
        )
        if modal_title is None:
            return modal.is_displayed()
        if not modal:
            log.error(f"Modal '{modal_title}' not found")
            assert False, f"Modal '{modal_title}' not found"

        _modal_title = self.browser.get_web_element(
            f"//*[contains(text(), '{modal_title}')]", locator_type="xpath", timeout=timeout
        )
        return bool(_modal_title)

    def close_modal(self) -> None:
        log = getLogger(f"{self.test_name}.close_modal")
        modal = self.browser.get_web_element("//div[@class='MuiDialogContent-root']", locator_type="xpath")
        if modal:
            self.browser.get_web_element('//*[@id="remove-button-icon"]', locator_type="xpath").click()
            log.info("Modal closed")
