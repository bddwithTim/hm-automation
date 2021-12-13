from src.choice_dtc.choice_dtc_actions import ChoiceDTCActions
from src.choice_dtc.browser import Browser


class ChoiceDTCActionSeries(ChoiceDTCActions):
    def __init__(self, test_name, driver):
        ChoiceDTCActions.__init__(self, test_name, driver)
        self.test_name = test_name
        self.driver = driver
        self.browser = Browser(self.test_name, self.driver)
