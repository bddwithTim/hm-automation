import logging

import pytest

import src.common.log as logger
from src.choice_dtc.choice_dtc_actions import ChoiceDTCActions
from src.common.utils import get_config


@pytest.mark.release_regression
def test_stm_basic_flow(driver, request):
    name = request.node.name
    logger.setup_logger(name, f"{name}.log")
    log = logging.getLogger(name)
    log.info("Test Case Logging Start")

    data = get_config("choice_dtc.yaml")
    # Test environment assignment i.e. model, supp, prod
    test_environment = data["choice_dtc_sites"][get_config("config.yaml")["environment"]]["url"]
    acts = ChoiceDTCActions(request.node.name, driver)

    acts.get_url("HealthMarket's shop site", test_environment)
    acts.lob_default_state(driver)  # ensures no LOBs are selected from previous tests
    acts.enter("75201", "#zipCode")  # Dallas, Texas zip code
    acts.click("Select STM LOB", data["choice_dtc_lob"]["short_term_health_insurance"]["css_value"])
    acts.click("Let's Go!", "[id*='submit-button-title']")
    acts.verify_page_loaded("Tell Us About Yourself", page_title="Contact Information")
    # Short Term Health Insurance
    acts.input_applicant_demographics(
        lob_type="short term medical",
        birth_date="10/25/1980",
        gender="Female",
        parent="No",
        tobacco="No",
    )
    acts.click("See Quotes button", "//p[text() = 'See Quotes']", locator_type="xpath")
    acts.verify_page_loaded("Quotes page", page_title="Quotes", timeout=60)
    # Since STM has no modal, increase the timeout taking into account the time for the plans loading
    acts.select_plan("Short Term Medical Value", action="add to cart", timeout=300)
    acts.verify_text(
        description="Add To Cart modal text",
        text="Great! You've added a  plan to your cart.\nIt's time to review your cart and enroll/apply.",
    )
    acts.click("Add To Cart button", "//p[text()='Go to My Cart']", locator_type="xpath")
    acts.verify_page_loaded("Cart page", page_title="Health Quotes")
    acts.click("Proceed to Application button", "//span[text()='Proceed To Application']", locator_type="xpath")
    # Enrollment
    acts.enter("9999999999", "input[id^= 'phoneNumber']")
    acts.enter("Test", "input[id^= 'firstName']")
    acts.enter("Automation", "input[id^= 'lastName']")


@pytest.mark.release_regression
def test_stm_with_spouse(driver, request):
    name = request.node.name
    logger.setup_logger(name, f"{name}.log")
    log = logging.getLogger(name)
    log.info("Test Case Logging Start")

    data = get_config("choice_dtc.yaml")
    # Test environment assignment i.e. model, supp, prod
    test_environment = data["choice_dtc_sites"][get_config("config.yaml")["environment"]]["url"]
    acts = ChoiceDTCActions(request.node.name, driver)

    acts.get_url("HealthMarket's shop site", test_environment)
    acts.lob_default_state(driver)  # ensures no LOBs are selected from previous tests
    acts.enter("75201", "#zipCode")  # Dallas, Texas zip code
    acts.click("Select STM LOB", data["choice_dtc_lob"]["short_term_health_insurance"]["css_value"])
    acts.click("Let's Go!", "[id*='submit-button-title']")
    acts.verify_page_loaded("Tell Us About Yourself", page_title="Contact Information")
    # Short Term Health Insurance
    acts.input_applicant_demographics(
        lob_type="short term medical",
        birth_date="10/25/1980",
        gender="Male",
        parent="No",
        tobacco="No",
    )
    # Add Spouse
    acts.click("Add Spouse label", "//span[contains(text(),'Add Spouse')]", locator_type="xpath")
    acts.input_spouse_demographics(
        first_name="TestSpouse",
        last_name="Automation",
        birth_date="10/25/1982",
        gender="Female",
        tobacco="No",
    )
    acts.click("See Quotes button", "//p[text() = 'See Quotes']", locator_type="xpath")
    # Quotes loading
    acts.verify_page_loaded("Quotes page", page_title="Quotes", timeout=60)
    # Since STM has no modal, increase the timeout taking into account the time for the plans loading
    acts.select_plan("Short Term Medical Value", action="add to cart", timeout=300)
    acts.verify_text(
        description="Add To Cart modal text",
        text="Great! You've added a  plan to your cart.\nIt's time to review your cart and enroll/apply.",
    )
    acts.click("Add To Cart button", "//p[text()='Go to My Cart']", locator_type="xpath")
    acts.verify_page_loaded("Cart page", page_title="Health Quotes")
    acts.click("Proceed to Application button", "//span[text()='Proceed To Application']", locator_type="xpath")
    # Enrollment
    acts.enter("9999999999", "input[id^= 'phoneNumber']")
    acts.enter("TestPrimary", "input[id^= 'firstName']")
    acts.enter("Automation", "input[id^= 'lastName']")


@pytest.mark.release_regression
def test_stm_with_dependent(driver, request):
    name = request.node.name
    logger.setup_logger(name, f"{name}.log")
    log = logging.getLogger(name)
    log.info("Test Case Logging Start")

    data = get_config("choice_dtc.yaml")
    # Test environment assignment i.e. model, supp, prod
    test_environment = data["choice_dtc_sites"][get_config("config.yaml")["environment"]]["url"]
    acts = ChoiceDTCActions(request.node.name, driver)

    acts.get_url("HealthMarket's shop site", test_environment)
    acts.lob_default_state(driver)  # ensures no LOBs are selected from previous tests
    acts.enter("75201", "#zipCode")  # Dallas, Texas zip code
    acts.click("Select STM LOB", data["choice_dtc_lob"]["short_term_health_insurance"]["css_value"])
    acts.click("Let's Go!", "[id*='submit-button-title']")
    acts.verify_page_loaded("Tell Us About Yourself", page_title="Contact Information")
    # Short Term Health Insurance
    acts.input_applicant_demographics(
        lob_type="short term medical",
        birth_date="10/25/1980",
        gender="Male",
        parent="Yes",
        tobacco="No",
    )
    # Add Dependent
    acts.click("Add Dependent label", "//span[contains(text(),'Add Dependent')]", locator_type="xpath")
    acts.input_dependent_demographics(
        first_name="TestDependent",
        last_name="Automation",
        birth_date="10/25/2010",
        gender="Female",
        tobacco="No",
    )
    acts.click("See Quotes button", "//p[text() = 'See Quotes']", locator_type="xpath")
    # Quotes loading
    acts.verify_page_loaded("Quotes page", page_title="Quotes", timeout=60)
    # Since STM has no modal, increase the timeout taking into account the time for the plans loading
    acts.select_plan("Short Term Medical Value", action="add to cart", timeout=300)
    acts.verify_text(
        description="Add To Cart modal text",
        text="Great! You've added a  plan to your cart.\nIt's time to review your cart and enroll/apply.",
    )
    acts.click("Add To Cart button", "//p[text()='Go to My Cart']", locator_type="xpath")
    acts.verify_page_loaded("Cart page", page_title="Health Quotes")
    acts.click("Proceed to Application button", "//span[text()='Proceed To Application']", locator_type="xpath")
    # Enrollment
    acts.enter("9999999999", "input[id^= 'phoneNumber']")
    acts.enter("TestPrimary", "input[id^= 'firstName']")
    acts.enter("Automation", "input[id^= 'lastName']")


@pytest.mark.release_regression
def test_stm_with_spouse_and_dependent(driver, request):
    name = request.node.name
    logger.setup_logger(name, f"{name}.log")
    log = logging.getLogger(name)
    log.info("Test Case Logging Start")

    data = get_config("choice_dtc.yaml")
    # Test environment assignment i.e. model, supp, prod
    test_environment = data["choice_dtc_sites"][get_config("config.yaml")["environment"]]["url"]
    acts = ChoiceDTCActions(request.node.name, driver)

    acts.get_url("HealthMarket's shop site", test_environment)
    acts.lob_default_state(driver)  # ensures no LOBs are selected from previous tests
    acts.enter("75201", "#zipCode")  # Dallas, Texas zip code
    acts.click("Select STM LOB", data["choice_dtc_lob"]["short_term_health_insurance"]["css_value"])
    acts.click("Let's Go!", "[id*='submit-button-title']")
    acts.verify_page_loaded("Tell Us About Yourself", page_title="Contact Information")
    # Short Term Health Insurance
    acts.input_applicant_demographics(
        lob_type="short term medical",
        birth_date="10/25/1980",
        gender="Male",
        parent="Yes",
        tobacco="No",
    )
    # Add Spouse
    acts.click("Add Spouse label", "//span[contains(text(),'Add Spouse')]", locator_type="xpath")
    acts.input_spouse_demographics(
        first_name="TestSpouse",
        last_name="Automation",
        birth_date="10/25/1982",
        gender="Female",
        tobacco="No",
    )
    # Add Dependent
    acts.click("Add Dependent label", "//span[contains(text(),'Add Dependent')]", locator_type="xpath")
    acts.input_dependent_demographics(
        first_name="TestDependent",
        last_name="Automation",
        birth_date="10/25/2010",
        gender="Female",
        tobacco="No",
    )
    acts.click("See Quotes button", "//p[text() = 'See Quotes']", locator_type="xpath")
    # Quotes loading
    acts.verify_page_loaded("Quotes page", page_title="Quotes", timeout=60)
    # Since STM has no modal, increase the timeout taking into account the time for the plans loading
    acts.select_plan("Short Term Medical Value", action="add to cart", timeout=300)
    acts.verify_text(
        description="Add To Cart modal text",
        text="Great! You've added a  plan to your cart.\nIt's time to review your cart and enroll/apply.",
    )
    acts.click("Add To Cart button", "//p[text()='Go to My Cart']", locator_type="xpath")
    acts.verify_page_loaded("Cart page", page_title="Health Quotes")
    acts.click("Proceed to Application button", "//span[text()='Proceed To Application']", locator_type="xpath")
    # Enrollment
    acts.enter("9999999999", "input[id^= 'phoneNumber']")
    acts.enter("TestPrimary", "input[id^= 'firstName']")
    acts.enter("Automation", "input[id^= 'lastName']")
