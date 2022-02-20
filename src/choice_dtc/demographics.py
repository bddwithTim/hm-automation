from selenium import webdriver

from src.choice_dtc.data import ApplicantInformation
from src.utils.utils import clear_input_fields, get_config, is_legal_age


class ShortTermMedicalDemographics(ApplicantInformation):
    """
    Demographics for Short Term Health Insurance applicant
    """

    def fill_out_form(self, driver: webdriver):
        data = get_config("choice_dtc.yaml")["demographics"]
        # clear remaining data in the text fields from previous test runs
        clear_input_fields(driver)

        driver.find_element_by_xpath(data["date_of_birth"]).send_keys(self.birth_date)
        # gender selection
        driver.find_element_by_xpath(data["gender"]["dropdown"]).click()
        driver.find_element_by_xpath(data["gender"][self.gender.lower()]).click()

        driver.find_element_by_xpath(data["parent_radio_button"][self.parent.lower()]).click()
        driver.find_element_by_xpath(data["email"]).send_keys(self.email)

        if is_legal_age(self.birth_date):
            driver.find_element_by_xpath(data["tobacco_radio_button"][self.tobacco.lower()]).click()


class SupplementalDemographics(ApplicantInformation):
    """
    Demographics for Supplemental Insurance applicant
    """

    def fill_out_form(self, driver: webdriver):
        data = get_config("choice_dtc.yaml")["demographics"]
        # clear remaining data in the text fields from previous test runs
        clear_input_fields(driver)

        driver.find_element_by_xpath(data["phone"]).send_keys(self.phone)
        driver.find_element_by_xpath(data["email"]).send_keys(self.email)
        driver.find_element_by_xpath(data["first_name"]).send_keys(self.first_name)
        driver.find_element_by_xpath(data["last_name"]).send_keys(self.last_name)
        driver.find_element_by_xpath(data["date_of_birth"]).send_keys(self.birth_date)
        # gender selection
        driver.find_element_by_xpath(data["gender"]["dropdown"]).click()
        driver.find_element_by_xpath(data["gender"][self.gender.lower()]).click()


class VisionDemographics(ApplicantInformation):
    """
    Demographics for Vision Insurance applicant
    """

    def fill_out_form(self, driver: webdriver):
        data = get_config("choice_dtc.yaml")["demographics"]
        # clear remaining data in the text fields from previous test runs
        clear_input_fields(driver)

        driver.find_element_by_xpath(data["phone"]).send_keys(self.phone)
        driver.find_element_by_xpath(data["email"]).send_keys(self.email)
        driver.find_element_by_xpath(data["first_name"]).send_keys(self.first_name)
        driver.find_element_by_xpath(data["last_name"]).send_keys(self.last_name)
        driver.find_element_by_xpath(data["date_of_birth"]).send_keys(self.birth_date)
        # gender selection
        driver.find_element_by_xpath(data["gender"]["dropdown"]).click()
        driver.find_element_by_xpath(data["gender"][self.gender.lower()]).click()


class MedicareDemographics(ApplicantInformation):
    """
    Demographics for Medicare Insurance applicant
    """

    def fill_out_form(self, driver: webdriver):
        data = get_config("choice_dtc.yaml")["demographics"]
        # clear remaining data in the text fields from previous test runs
        clear_input_fields(driver)

        driver.find_element_by_xpath(data["phone"]).send_keys(self.phone)
        driver.find_element_by_xpath(data["email"]).send_keys(self.email)
        driver.find_element_by_xpath(data["first_name"]).send_keys(self.first_name)
        driver.find_element_by_xpath(data["last_name"]).send_keys(self.last_name)
        driver.find_element_by_xpath(data["date_of_birth"]).send_keys(self.birth_date)


class ACAHealthDemographics(ApplicantInformation):
    """
    Demographics for ACA Health Insurance applicant
    """

    def fill_out_form(self, driver: webdriver):
        data = get_config("choice_dtc.yaml")["demographics"]
        # clear remaining data in the text fields from previous test runs
        clear_input_fields(driver)

        driver.find_element_by_xpath(data["phone"]).send_keys(self.phone)
        driver.find_element_by_xpath(data["email"]).send_keys(self.email)
        driver.find_element_by_xpath(data["first_name"]).send_keys(self.first_name)
        driver.find_element_by_xpath(data["last_name"]).send_keys(self.last_name)
        driver.find_element_by_xpath(data["date_of_birth"]).send_keys(self.birth_date)
        # gender selection
        driver.find_element_by_xpath(data["gender"]["dropdown"]).click()
        driver.find_element_by_xpath(data["gender"][self.gender.lower()]).click()

        driver.find_element_by_xpath(data["parent_radio_button"][self.parent.lower()]).click()

        if is_legal_age(self.birth_date):
            driver.find_element_by_xpath(data["tobacco_radio_button"][self.tobacco.lower()]).click()

        driver.find_element_by_xpath(data["annual_income"]).send_keys(self.annual_income)
        driver.find_element_by_xpath(data["household_members"]).send_keys(self.household_members)


class DentalDemographics(ApplicantInformation):
    """
    Demographics for Dental Insurance applicant
    """

    def fill_out_form(self, driver: webdriver):
        data = get_config("choice_dtc.yaml")["demographics"]
        # clear remaining data in the text fields from previous test runs
        clear_input_fields(driver)

        driver.find_element_by_xpath(data["phone"]).send_keys(self.phone)
        driver.find_element_by_xpath(data["email"]).send_keys(self.email)
        driver.find_element_by_xpath(data["first_name"]).send_keys(self.first_name)
        driver.find_element_by_xpath(data["last_name"]).send_keys(self.last_name)
        driver.find_element_by_xpath(data["date_of_birth"]).send_keys(self.birth_date)
        # gender selection
        driver.find_element_by_xpath(data["gender"]["dropdown"]).click()
        driver.find_element_by_xpath(data["gender"][self.gender.lower()]).click()
