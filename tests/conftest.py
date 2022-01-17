import os
import pytest
import atexit

from datetime import datetime
import src.lib.base as base
from src.choice_dtc.browser import get_driver


@pytest.fixture(scope='session')
def driver():
    browser = base.config['browser']
    web_driver = get_driver(browser, headless=False)
    yield web_driver
    atexit.register(lambda: web_driver.quit())


# set up a hook to be able to check if a test has failed
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"

    setattr(item, "rep_" + rep.when, rep)


def pytest_cmdline_preparse(args):
    # generates an html report using the pytest-html plugin
    args.extend(['--html', f'./reports/report_{datetime.today().strftime("%Y-%m-%d_%H-%M-%S")}.html'])


@pytest.fixture(scope="function", autouse=True)
def test_failed_check(request):
    yield
    # takes a screenshot for the failed test
    if request.node.rep_setup.passed and request.node.rep_call.failed:
        driver = request.node.funcargs['driver']
        _capture_screenshot(driver, request.node.name)


def _capture_screenshot(driver, node_name):
    file_name = f'{node_name}_{datetime.today().strftime("%Y-%m-%d_%H-%M-%S")}.png'
    failed_tests_dir = './screenshots/failed_tests'
    if not os.path.exists(failed_tests_dir):
        os.mkdir(failed_tests_dir)
    driver.save_screenshot(f'{failed_tests_dir}/{file_name}')
