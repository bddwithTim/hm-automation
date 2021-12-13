import logging

import src.lib.log as logger
import pytest

from src.choice_dtc.choice_dtc_action_series import ChoiceDTCActionSeries
from src.utils.util import get_config, read_xls, title_case


@pytest.mark.fips
@pytest.mark.parametrize("zip_code, fips, state, county, county_selection, prod_name",
                         read_xls('stm_popular_plans.xlsx'))
def test_demo(zip_code, fips, state, county, county_selection, prod_name, driver, request):
    name = request.node.name
    logger.setup_logger(name, f'{name}.log')
    log = logging.getLogger(name)
    log.info('Test Case Logging Start')

    data = get_config('choice_dtc.yaml')
    acts = ChoiceDTCActionSeries(request.node.name, driver)

    acts.get_url("dtc-model", data["choice_dtc_sites"]["dtc-model"]["url"])
    acts.lob_default_state(driver)  # ensures no LOBs are selected from previous tests
    acts.enter(zip_code, "#zipCode")
    acts.select_county(county, title_case(county_selection))
    acts.click("STM", data["choice_dtc_lob"]["short_term_health_insurance"]["css_value"])
    acts.click("Let's Go!", "[id*='submit-button-title']")

    acts.verify_page_loaded("Tell Us About Yourself", page_title='Contact Information', timeout=10)
    acts.input_demographics(insurance_type='Short Term', date_of_birth='03/03/1980',
                            gender='Female', email='', parent='No', tobacco='No')
    acts.click("See Quotes button", "//p[text() = 'See Quotes']", locator_type='xpath')
    acts.wait_plans_to_load()
    acts.get_most_popular_plans(prod_name, file_name=f'{state}_{county}_{zip_code}_{prod_name}')
