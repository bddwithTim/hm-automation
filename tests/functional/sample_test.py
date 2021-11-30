import pytest

from src.choice_dtc.choice_dtc_action_series import ChoiceDTCActionSeries


@pytest.mark.smoke
def test_sample(driver, request):
    acts = ChoiceDTCActionSeries(request.node.name, driver)

    acts.get_url('contact-info', 'https://shop.model.healthmarkets.com/en/about-me/contact-info')
    acts.verify_text("Tell Us About Yourself", timeout=10)