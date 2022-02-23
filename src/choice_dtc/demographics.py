from selenium import webdriver

from src.choice_dtc.data import (
    ApplicantInformation,
    DependentInformation,
    SpouseInformation,
)
from src.common.utils import clear_input_fields, get_config, is_legal_age


class ShortTermMedicalDemographics(ApplicantInformation):
    """
    Demographics for Short Term Health Insurance
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


class SupplementaryDemographics(ApplicantInformation):
    """
    Demographics for Dental, Vision and Supplemental Insurance
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
    Demographics for Medicare Insurance
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
    Demographics for ACA Health Insurance
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


class SpouseDemographics(SpouseInformation):
    """
    Demographics for Spouse
    """

    def fill_out_form(self, driver: webdriver):
        data = get_config("choice_dtc.yaml")["demographics"]

        driver.find_element_by_xpath("//div[@aria-label='Spouse ']//input[@id='firstName']").send_keys(self.first_name)
        driver.find_element_by_xpath("//div[@aria-label='Spouse ']//input[@id='lastName']").send_keys(self.last_name)
        driver.find_element_by_xpath("//div[@aria-label='Spouse ']//input[contains(@id, 'dateOfBirth')]").send_keys(
            self.birth_date
        )
        # gender selection
        driver.find_element_by_xpath("//div[@aria-label='Spouse ']//div[@id='gender']").click()
        driver.find_element_by_xpath(data["gender"][self.gender.lower()]).click()

        if is_legal_age(self.birth_date):
            driver.find_element_by_xpath(
                f"""{"//div[@aria-label='Spouse ']"}{data["tobacco_radio_button"][self.tobacco.lower()]}"""
            ).click()


class DependentDemographics(DependentInformation):
    """
    Demographics for Dependent
    """

    def fill_out_form(self, driver: webdriver):
        data = get_config("choice_dtc.yaml")["demographics"]

        driver.find_element_by_xpath("//div[@aria-label='Dependent ']//input[@id='firstName']").send_keys(
            self.first_name
        )
        driver.find_element_by_xpath("//div[@aria-label='Dependent ']//input[@id='lastName']").send_keys(self.last_name)
        driver.find_element_by_xpath("//div[@aria-label='Dependent ']//input[contains(@id, 'dateOfBirth')]").send_keys(
            self.birth_date
        )
        # gender selection
        driver.find_element_by_xpath("//div[@aria-label='Dependent ']//div[@id='gender']").click()
        driver.find_element_by_xpath(data["gender"][self.gender.lower()]).click()


def fill_out_details(driver: webdriver, lob_type: str, **kwargs) -> None:
    """ Fill out details for the primary applicant. """

    lob_demographics = {
        "short term": ShortTermMedicalDemographics,
        "medicare": MedicareDemographics,
        "aca": ACAHealthDemographics,
        "vision": SupplementaryDemographics,
        "dental": SupplementaryDemographics,
        "supplemental": SupplementaryDemographics,
    }
    applicant_demographics = None
    for key, value in lob_demographics.items():
        if key in lob_type.lower():
            # instantiate LOB demographics class
            applicant_demographics = value()
    # raise Value Error if LOB type is not valid
    if applicant_demographics is None:
        raise ValueError(f"LOB type '{lob_type}' format is invalid. Valid values are: {list(lob_demographics.keys())}")

    for key, value in kwargs.items():
        setattr(applicant_demographics, key, value)
    applicant_demographics.fill_out_form(driver)


def fill_out_spouse_details(driver: webdriver, **kwargs) -> None:
    spouse_demographics = SpouseDemographics()
    for key, value in kwargs.items():
        setattr(spouse_demographics, key, value)
    spouse_demographics.fill_out_form(driver)


def fill_out_dependent_details(driver: webdriver, **kwargs) -> None:
    dependent_demographics = DependentDemographics()
    for key, value in kwargs.items():
        setattr(dependent_demographics, key, value)
    dependent_demographics.fill_out_form(driver)
