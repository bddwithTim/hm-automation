import os
import pytest

from datetime import datetime
from src.lib.browser import get_driver
from src.utils.util import get_config


@pytest.fixture(scope="session")
def driver():
    data = get_config("config.yaml")
    browser = data["browser"]["name"]
    web_driver = get_driver(browser, headless=False)
    yield web_driver
    web_driver.quit()


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
    data = get_config("config.yaml")
    # generates an html report using the pytest-html plugin
    args.extend(
        ["--html", f'{data["directory"]["reports"]}/report_{datetime.today().strftime("%Y-%m-%d_%H-%M-%S")}.html']
    )


@pytest.fixture(scope="function", autouse=True)
def test_failed_check(request):
    yield
    # takes a screenshot for the failed test
    if request.node.rep_setup.passed and request.node.rep_call.failed:
        driver = request.node.funcargs["driver"]
        _capture_screenshot(driver, request.node.name)


def _capture_screenshot(driver, node_name):
    # initialize the directory for the screenshots
    directory = get_config("config.yaml")["directory"]["screenshots"]
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_name = f'{node_name}_{datetime.today().strftime("%Y-%m-%d_%H-%M-%S")}.png'
    failed_tests_dir = f"{directory}/failed_tests"
    if not os.path.exists(failed_tests_dir):
        os.mkdir(failed_tests_dir)
    driver.save_screenshot(f"{failed_tests_dir}/{file_name}")
