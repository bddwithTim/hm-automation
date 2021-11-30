import logging
import src.lib.log as logger
import pytest

from src.choice_dtc.choice_dtc_action_series import ChoiceDTCActionSeries
from src.utils.util import get_config, read_xls, parse_str


@pytest.mark.regression
@pytest.mark.parametrize("test_id, app_type, zip_code, prod_type, phone, email, first_name, last_name,"
                         " dob, gender, tobacco, parent, plan", read_xls('test_lob.xlsx'))
def test_demo(test_id, app_type, zip_code, prod_type, phone, email, first_name, last_name,
              dob, gender, tobacco, parent, plan, driver, request):
    name = request.node.name
    logger.setup_logger(name, f'{name}.log')
    log = logging.getLogger(name)
    log.info('Test Case Logging Start')

    data = get_config('choice_dtc.yaml')
    acts = ChoiceDTCActionSeries(request.node.name, driver)

    acts.get_url(app_type, data["choice_dtc_sites"][app_type]["url"])
    acts.lob_default_state(driver)  # ensures no LOBs are selected from previous tests
    acts.enter(zip_code, "#zipCode")
    acts.click(f"{prod_type} LOB",
               data["choice_dtc_lob"][parse_str(prod_type)]["css_value"])
    acts.click("Let's Go!", "[id*='submit-button-title']")

    acts.verify_page_loaded("Tell Us About Yourself", page_title='Contact Information', timeout=10)
    acts.input_demographics(prod_type, phone=phone, email=email, first_name=first_name, last_name=last_name,
                            gender=gender, date_of_birth=dob, tobacco=tobacco, parent=parent,
                            locator_type='css selector')
    acts.click("See Quotes button", "//p[text() = 'See Quotes']", locator_type='xpath')
    acts.verify_page_loaded("Quotes page", page_title='Quotes', timeout=60)
    acts.verify_modal_displayed(prod_type, timeout=60)
    acts.close_modal(prod_type)



@pytest.mark.smoke
@pytest.mark.parametrize("test_id, app_type, zip_code, prod_type, phone, email, first_name, last_name,"
                         " dob, gender, tobacco, parent, plan", read_xls('test_lob.xlsx'))
def test_selecting_a_specific_plan(test_id, app_type, zip_code, prod_type, phone, email, first_name, last_name,
              dob, gender, tobacco, parent, plan, driver, request):
    name = request.node.name
    logger.setup_logger(name, f'{name}.log')
    log = logging.getLogger(name)
    log.info('Test Case Logging Start')

    data = get_config('choice_dtc.yaml')
    acts = ChoiceDTCActionSeries(request.node.name, driver)

    acts.get_url(app_type, data["choice_dtc_sites"][app_type]["url"])
    acts.lob_default_state(driver)  # ensures no LOBs are selected from previous tests
    acts.enter(zip_code, "#zipCode")
    acts.click(f"{prod_type} LOB",
               data["choice_dtc_lob"][parse_str(prod_type)]["css_value"])
    acts.click("Let's Go!", "[id*='submit-button-title']")

    acts.verify_page_loaded("Tell Us About Yourself", page_title='Contact Information', timeout=10)

    acts.click("See Quotes button", "//p[text() = 'See Quotes']", locator_type='xpath')
    acts.verify_page_loaded("Quotes page", page_title='Quotes', timeout=60)
    acts.verify_modal_displayed(prod_type, timeout=60)
    acts.close_modal(prod_type)
    # acts.select_plan('WellCare Focus (HMO)', action='see plan details')
    # acts.select_plan('WellCare Focus (HMO)', action='compare')
    acts.select_plan('WellCare Focus (HMO)', action='add to cart')
    acts.verify_text(description="Add to cart modal", text="Great! You've added a  plan to your cart.")
    acts.click("Go to my cart button", "//p[text() = 'Go to My Cart']", locator_type='xpath')


@pytest.mark.ui
def test_capture_logo(driver, request):
    name = request.node.name
    logger.setup_logger(name, f'{name}.log')
    log = logging.getLogger(name)
    log.info('Test Case Logging Start')

    acts = ChoiceDTCActionSeries(request.node.name, driver)

    acts.get_url("Landing page",
                 "https://shop.model.healthmarkets.com/en?Token=d672d103-d73c-4110-baef-4196a7cf9625")
    acts.verify_image_displayed(description="Health Markets logo", web_element="//img[@class='desktop-app-logo']")