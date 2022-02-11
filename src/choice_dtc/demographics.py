from logging import getLogger

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from src.lib.browser import Browser
from src.utils.utils import get_config, is_legal_age, parse_str


class Demographics:
    """
    Utility class for handling demographics page operations
    """

    def __init__(self, test_name: str, driver: webdriver) -> None:
        self.test_name = test_name
        self.driver = driver
        self.phone_number = None
        self.email = None
        self.first_name = None
        self.last_name = None
        self.date_of_birth = None
        self.gender = None
        self.annual_income = None
        self.household_members = None
        self.parent = None
        self.tobacco = None
        self.medicare_coverage_year = None
        self.browser = Browser(self.test_name, self.driver)

    def fill_out_details(
        self,
        insurance_type: str,
        locator_type: str,
        phone: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
        date_of_birth: str = None,
        gender: str = None,
        tobacco: str = None,
        parent: str = None,
        annual_income: str = None,
        household_members: str = None,
        medicare_coverage_year: str = None,
    ) -> None:
        self.phone_number = phone
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.tobacco = tobacco
        self.parent = parent
        self.annual_income = annual_income
        self.household_members = household_members
        self.medicare_coverage_year = medicare_coverage_year

        data = get_config("choice_dtc.yaml")["demographics"]
        log = getLogger(f"{self.test_name}.fill_out_details")
        log.info(f"Param app_type: {insurance_type}")

        if "short term" in insurance_type.lower():
            self._fill_out_stm(data, locator_type)
        elif "medicare" in insurance_type.lower():
            self._fill_out_medicare(data, locator_type)
        elif "aca" in insurance_type.lower():
            self._fill_out_aca(data, locator_type)
        elif "dental" in insurance_type.lower():
            self._fill_out_dental(data, locator_type)
        elif "vision" in insurance_type.lower():
            self._fill_out_vision(data, locator_type)
        elif "supplemental" in insurance_type.lower():
            self._fill_out_supplemental(data, locator_type)

    def _fill_out_stm(self, data: dict, locator_type: str) -> None:
        log = getLogger(f"{self.test_name}._fill_out_stm")
        log.info(f"Param data: {data}")
        dob = self.browser.get_web_element(data["date_of_birth"][parse_str(locator_type)], locator_type)
        _clean_textbox_data(dob)
        dob.send_keys(self.date_of_birth)
        # click the dropdown listbox
        self.browser.get_web_element(data["gender"][parse_str(locator_type)], locator_type).click()
        # click the option from the dropdown listbox
        self.browser.get_web_element(data["gender"][self.gender.lower()], locator_type="xpath").click()
        email = self.browser.get_web_element(data["email"][parse_str(locator_type)], locator_type)
        _clean_textbox_data(email)
        email.send_keys(self.email)
        self.browser.get_web_element(
            data["parent_radio_button"][f"{self.parent.lower()}_option"], locator_type="xpath"
        ).click()
        if not is_legal_age(self.date_of_birth):
            self.browser.get_web_element(
                data["tobacco_radio_button"][f"{self.parent.lower()}_option"], locator_type="xpath"
            ).click()

    def _fill_out_medicare(self, data: dict, locator_type: str) -> None:
        log = getLogger(f"{self.test_name}._fill_out_medicare")
        log.info(f"Param data: {data}")
        if self.medicare_coverage_year is not None:
            self.browser.get_web_element(data["medicare_coverage_year"][self.medicare_coverage_year]).click()

        phone = self.browser.get_web_element(data["phone"][parse_str(locator_type)], locator_type)
        _clean_textbox_data(phone)
        phone.send_keys(self.phone_number)
        email = self.browser.get_web_element(data["email"][parse_str(locator_type)], locator_type)
        _clean_textbox_data(email)
        email.send_keys(self.email)
        first_name = self.browser.get_web_element(data["first_name"][parse_str(locator_type)], locator_type)
        _clean_textbox_data(first_name)
        first_name.send_keys(self.first_name)
        last_name = self.browser.get_web_element(data["last_name"][parse_str(locator_type)], locator_type)
        _clean_textbox_data(last_name)
        last_name.send_keys(self.last_name)
        dob = self.browser.get_web_element(data["date_of_birth"][parse_str(locator_type)], locator_type)
        _clean_textbox_data(dob)
        dob.send_keys(self.date_of_birth)

    def _fill_out_aca(self, data: dict, locator_type: str) -> None:
        log = getLogger(f"{self.test_name}._fill_out_aca")
        log.info(f"Param data: {data}")
        dob = self.browser.get_web_element(data["date_of_birth"][parse_str(locator_type)], locator_type)
        _clean_textbox_data(dob)
        dob.send_keys(self.date_of_birth)
        phone = self.browser.get_web_element(data["phone"][parse_str(locator_type)], locator_type)
        _clean_textbox_data(phone)
        phone.send_keys(self.phone_number)
        email = self.browser.get_web_element(data["email"][parse_str(locator_type)], locator_type)
        _clean_textbox_data(email)
        email.send_keys(self.email)
        first_name = self.browser.get_web_element(data["first_name"][parse_str(locator_type)], locator_type)
        _clean_textbox_data(first_name)
        first_name.send_keys(self.first_name)
        last_name = self.browser.get_web_element(data["last_name"][parse_str(locator_type)], locator_type)
        _clean_textbox_data(last_name)
        last_name.send_keys(self.last_name)
        # click the dropdown listbox
        self.browser.get_web_element(data["gender"][parse_str(locator_type)], locator_type).click()
        # click the option from the dropdown listbox
        self.browser.get_web_element(data["gender"][self.gender.lower()], locator_type="xpath").click()
        self.browser.get_web_element(
            data["parent_radio_button"][f"{self.parent.lower()}_option"], locator_type="xpath"
        ).click()
        if not is_legal_age(self.date_of_birth):
            self.browser.get_web_element(
                data["tobacco_radio_button"][f"{self.parent.lower()}_option"], locator_type="xpath"
            ).click()
        if self.annual_income is not None:
            annual_income = self.browser.get_web_element(data["annual_income"][parse_str(locator_type)], locator_type)
            _clean_textbox_data(annual_income)
            annual_income.send_keys(self.annual_income)

            household_members = self.browser.get_web_element(
                data["household_members"][parse_str(locator_type)], locator_type
            )
            _clean_textbox_data(household_members)
            household_members.send_keys(self.household_members)

    def _fill_out_dental(self, data: dict, locator_type: str) -> None:
        log = getLogger(f"{self.test_name}._fill_out_dental")
        log.info(f"Param data: {data}")
        phone = self.browser.get_web_element(data["phone"][parse_str(locator_type)], locator_type)
        _clean_textbox_data(phone)
        phone.send_keys(self.phone_number)
        email = self.browser.get_web_element(data["email"][parse_str(locator_type)], locator_type)
        _clean_textbox_data(email)
        email.send_keys(self.email)
        first_name = self.browser.get_web_element(data["first_name"][parse_str(locator_type)], locator_type)
        _clean_textbox_data(first_name)
        first_name.send_keys(self.first_name)
        last_name = self.browser.get_web_element(data["last_name"][parse_str(locator_type)], locator_type)
        _clean_textbox_data(last_name)
        last_name.send_keys(self.last_name)
        dob = self.browser.get_web_element(data["date_of_birth"][parse_str(locator_type)], locator_type)
        _clean_textbox_data(dob)
        dob.send_keys(self.date_of_birth)
        # click the dropdown listbox
        self.browser.get_web_element(data["gender"][parse_str(locator_type)], locator_type).click()
        # click the option from the dropdown listbox
        self.browser.get_web_element(data["gender"][self.gender.lower()], locator_type="xpath").click()

    def _fill_out_vision(self, data: dict, locator_type: str) -> None:
        log = getLogger(f"{self.test_name}._fill_out_vision")
        log.info(f"Param data: {data}")
        phone = self.browser.get_web_element(data["phone"][parse_str(locator_type)], locator_type)
        _clean_textbox_data(phone)
        phone.send_keys(self.phone_number)
        email = self.browser.get_web_element(data["email"][parse_str(locator_type)], locator_type)
        _clean_textbox_data(email)
        email.send_keys(self.email)
        first_name = self.browser.get_web_element(data["first_name"][parse_str(locator_type)], locator_type)
        _clean_textbox_data(first_name)
        first_name.send_keys(self.first_name)
        last_name = self.browser.get_web_element(data["last_name"][parse_str(locator_type)], locator_type)
        _clean_textbox_data(last_name)
        last_name.send_keys(self.last_name)
        dob = self.browser.get_web_element(data["date_of_birth"][parse_str(locator_type)], locator_type)
        _clean_textbox_data(dob)
        dob.send_keys(self.date_of_birth)
        # click the dropdown listbox
        self.browser.get_web_element(data["gender"][parse_str(locator_type)], locator_type).click()
        # click the option from the dropdown listbox
        self.browser.get_web_element(data["gender"][self.gender.lower()], locator_type="xpath").click()

    def _fill_out_supplemental(self, data: dict, locator_type: str) -> None:
        log = getLogger(f"{self.test_name}._fill_out_supplemental")
        log.info(f"Param data: {data}")
        phone = self.browser.get_web_element(data["phone"][parse_str(locator_type)], locator_type)
        _clean_textbox_data(phone)
        phone.send_keys(self.phone_number)
        email = self.browser.get_web_element(data["email"][parse_str(locator_type)], locator_type)
        _clean_textbox_data(email)
        email.send_keys(self.email)
        first_name = self.browser.get_web_element(data["first_name"][parse_str(locator_type)], locator_type)
        _clean_textbox_data(first_name)
        first_name.send_keys(self.first_name)
        last_name = self.browser.get_web_element(data["last_name"][parse_str(locator_type)], locator_type)
        _clean_textbox_data(last_name)
        last_name.send_keys(self.last_name)
        dob = self.browser.get_web_element(data["date_of_birth"][parse_str(locator_type)], locator_type)
        _clean_textbox_data(dob)
        dob.send_keys(self.date_of_birth)
        # click the dropdown listbox
        self.browser.get_web_element(data["gender"][parse_str(locator_type)], locator_type).click()
        # click the option from the dropdown listbox
        self.browser.get_web_element(data["gender"][self.gender.lower()], locator_type="xpath").click()


def _clean_textbox_data(web_element: WebElement) -> None:
    # ensure there's no remaining data in the textbox from previous test
    web_element.send_keys(f"{Keys.CONTROL}A{Keys.DELETE}")
