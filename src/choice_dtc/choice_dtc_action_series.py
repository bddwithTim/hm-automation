import time
from logging import getLogger

from src.choice_dtc.choice_dtc_actions import ChoiceDTCActions
from src.choice_dtc.browser import Browser
from src.utils.util import capture_image


class ChoiceDTCActionSeries(ChoiceDTCActions):
    def __init__(self, test_name, driver):
        ChoiceDTCActions.__init__(self, test_name, driver)
        self.test_name = test_name
        self.driver = driver
        self.browser = Browser(self.test_name, self.driver)

    def verify_image_displayed(self, description: str, web_element: str):
        log = getLogger(f'{self.test_name}.verify_image_displayed')
        log.info(f"Param description: {description}")
        image = self.browser.get_web_element(web_element, locator_type='xpath')
        temp = capture_image(self.driver, image)
        temp.save(f'image_{time.time()}.png')
