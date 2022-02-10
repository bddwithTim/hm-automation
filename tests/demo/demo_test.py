import logging
import src.lib.log as logger
import pytest

from src.choice_dtc.choice_dtc_actions import ChoiceDTCActions
from src.utils.utils import get_config, read_xls, parse_str


@pytest.mark.regression
@pytest.mark.parametrize(
    "test_id, app_type, zip_code, prod_type, phone, email, first_name, last_name,"
    " dob, gender, tobacco, parent, plan",
    read_xls("demo_lob.xlsx"),
)
def test_demo_lob(
    test_id,
    app_type,
    zip_code,
    prod_type,
    phone,
    email,
    first_name,
    last_name,
    dob,
    gender,
    tobacco,
    parent,
    plan,
    driver,
    request,
):
    name = request.node.name
    logger.setup_logger(name, f"{name}.log")
    log = logging.getLogger(name)
    log.info("Test Case Logging Start")

    data = get_config("choice_dtc.yaml")
    acts = ChoiceDTCActions(request.node.name, driver)

    acts.get_url(app_type, data["choice_dtc_sites"][app_type]["url"])
    acts.lob_default_state(driver)  # ensures no LOBs are selected from previous tests
    acts.enter(zip_code, "#zipCode")
    acts.click(f"{prod_type} LOB", data["choice_dtc_lob"][parse_str(prod_type)]["css_value"])
    acts.click("Let's Go!", "[id*='submit-button-title']")

    acts.verify_page_loaded("Tell Us About Yourself", page_title="Contact Information", timeout=10)
    acts.input_demographics(
        prod_type,
        phone=phone,
        email=email,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        date_of_birth=dob,
        tobacco=tobacco,
        parent=parent,
        locator_type="css selector",
    )
    acts.click("See Quotes button", "//p[text() = 'See Quotes']", locator_type="xpath")
    acts.verify_page_loaded("Quotes page", page_title="Quotes", timeout=60)
    acts.verify_modal_displayed(prod_type, timeout=500)
    acts.close_modal(prod_type)


@pytest.mark.smoke
@pytest.mark.parametrize("test_id, app_type, zip_code, prod_type, plan, action", read_xls("demo_plan.xlsx"))
def test_demo_selecting_specific_plan(test_id, app_type, zip_code, prod_type, plan, action, driver, request):
    name = request.node.name
    logger.setup_logger(name, f"{name}.log")
    log = logging.getLogger(name)
    log.info("Test Case Logging Start")

    data = get_config("choice_dtc.yaml")
    acts = ChoiceDTCActions(request.node.name, driver)

    acts.get_url(app_type, data["choice_dtc_sites"][app_type]["url"])
    acts.lob_default_state(driver)  # ensures no LOBs are selected from previous tests
    acts.enter(zip_code, "#zipCode")
    acts.click(f"{prod_type} LOB", data["choice_dtc_lob"][parse_str(prod_type)]["css_value"])
    acts.click("Let's Go!", "[id*='submit-button-title']")

    acts.verify_page_loaded("Tell Us About Yourself", page_title="Contact Information", timeout=10)

    acts.click("See Quotes button", "//p[text() = 'See Quotes']", locator_type="xpath")
    acts.verify_page_loaded("Quotes page", page_title="Quotes", timeout=60)
    acts.verify_modal_displayed(prod_type, timeout=500)
    acts.close_modal(prod_type)
    acts.select_plan(plan_name=plan, action=action)


@pytest.mark.ui
def test_demo_ui(driver, request):
    name = request.node.name
    logger.setup_logger(name, f"{name}.log")
    log = logging.getLogger(name)
    log.info("Test Case Logging Start")

    data = get_config("choice_dtc.yaml")
    test = get_config("config.yaml")
    acts = ChoiceDTCActions(request.node.name, driver)

    acts.get_url("HealthMarket's shop site", data["choice_dtc_sites"][test["environment"]]["url"])
    # HealthMarket's shop site default logo in the header
    acts.verify_image(
        file_name="desktop_hm_header_logo.png",
        image_element="//img[@class= 'desktop-app-logo']",
        locator_type="xpath",
        timeout=15,
    )
    # HealthMarket's shop site default logo in the footer
    acts.verify_image(
        file_name="desktop_hm_footer_logo.png",
        image_element="//img[contains(@id, 'footer-logo')]",
        locator_type="xpath",
        timeout=15,
    )
