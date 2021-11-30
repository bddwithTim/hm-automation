import pytest
import atexit

import src.lib.base as base

from src.choice_dtc.browser import get_driver


@pytest.fixture(scope='session')
def driver():
    browser = base.config['browser']
    web_driver = get_driver(browser, headless=False)
    yield web_driver
    atexit.register(lambda: web_driver.quit())
