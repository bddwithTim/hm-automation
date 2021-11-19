import pytest
import time

from src.templates.action_series import UHO_ActionSeries
from src.utils.util import get_config, read_xls


@pytest.mark.timoy_aca
@pytest.mark.parametrize("test_id, app_type, zip_code, prod_type, phone, email, fname, lname, age, sex, tobacco, "
                         "parent,plan", read_xls('test_aca_stm.xlsx'))
def test_get_url(test_id, app_type, zip_code, prod_type, phone, email, fname, lname, age, sex, tobacco, parent, plan,
                 driver, request):
    data = get_config('choice_dtc.yaml')
    acts = UHO_ActionSeries(request.node.name, driver)

    acts.url(0, data["choice_dtc_sites"][app_type]["url"], data["choice_dtc_sites"][app_type]["title"])
    acts.enter(0, zip_code, "#zipCode")
    acts.click(0, data["choice_dtc_lob"][prod_type.lower().replace(" ", "_")]["description"],
               data["choice_dtc_lob"][prod_type.lower().replace(" ", "_")]["css_value"])
    time.sleep(0.8)
    acts.click(0, "Let's Go!", "[id*='submit-button-title']")

    acts.verify(0, "Text: Tell Us About Yourself", "[id*='ApplicantInfoForm.TellUsAboutYourself']")
    time.sleep(5)


