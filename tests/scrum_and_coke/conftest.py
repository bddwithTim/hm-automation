import pytest
import atexit

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

import src.lib.base as base


@pytest.fixture(scope='function')
def driver():
    web_driver = None
    browser = base.config['browser']
    if browser == 'ie':
        caps = webdriver.DesiredCapabilities.INTERNETEXPLORER
        caps['ignoreProtectedModeSettings'] = True
        caps['ignoreZoomSetting'] = True
        web_driver = webdriver.Ie('.\src\drivers\IEDriverServer.exe', log_file=".\logs\ie.log", capabilities=caps)
    elif browser == 'chrome':
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        web_driver = webdriver.Chrome(executable_path="./src/drivers/chromedriver.exe",
                                      options=chrome_options)
    elif browser == 'firefox':
        web_driver = webdriver.Firefox(executable_path=".\src\drivers\geckodriver.exe", log_path='.\logs\gecko.log')
    elif browser == 'safari':
        web_driver = webdriver.Safari()
    elif browser == 'mobile':
        mobile_emulation = {'deviceName': base.config['device']}
        chrome_opts = webdriver.ChromeOptions()
        chrome_opts.add_experimental_option('mobileEmulation', mobile_emulation)
        web_driver = webdriver.Chrome(executable_path='.\src\drivers\chromedriver.exe', chrome_options=chrome_opts,
                                      service_log_path='.\logs\mobile.log')

    yield web_driver
    atexit.register(web_driver.quit)


def pytest_generate_tests(metafunc):
    pass

def pytest_terminal_summary(terminalreporter):
    pass