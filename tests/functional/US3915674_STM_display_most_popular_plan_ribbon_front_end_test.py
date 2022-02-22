import logging

import pytest

import src.common.log as logger
from src.choice_dtc.choice_dtc_actions import ChoiceDTCActions
from src.common.utils import get_config, read_xls, rectify_zip_code, title_case


@pytest.mark.fips_stm
@pytest.mark.parametrize(
    "zip_code, fips, state, county, county_selection, prod_name, plan_id",
    read_xls("US3915674_stm_most_popular_plans.xlsx"),
)
def test_fips_stm(zip_code, fips, state, county, county_selection, prod_name, plan_id, driver, request):
    name = request.node.name
    logger.setup_logger(name, f"{name}.log")
    log = logging.getLogger(name)
    log.info("Test Case Logging Start")

    data = get_config("choice_dtc.yaml")
    test_environment = data["choice_dtc_sites"][get_config("config.yaml")["environment"]]["url"]
    acts = ChoiceDTCActions(request.node.name, driver)

    acts.get_url("HealthMarket's shop site", test_environment)  # eg., model/supp environment
    acts.lob_default_state(driver)  # ensures no LOBs are selected from previous tests
    acts.enter(rectify_zip_code(zip_code), "#zipCode")
    acts.select_county(county, title_case(county_selection))
    acts.click("STM", data["choice_dtc_lob"]["short_term_health_insurance"]["css_value"])
    acts.click("Let's Go!", "[id*='submit-button-title']")

    acts.verify_page_loaded("Tell Us About Yourself", page_title="Contact Information", timeout=20)
    acts.input_applicant_demographics(
        lob_type="Short Term", birth_date="03/03/1980", gender="Female", parent="No", tobacco="No"
    )
    acts.click("See Quotes button", "//p[text() = 'See Quotes']", locator_type="xpath")
    acts.wait_plans_to_load(timeout=500)
    acts.get_plan_with_popular_ribbon()
    acts.verify_plan_id(plan_id)
