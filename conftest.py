from platform import system, release
import os
import time
import datetime
import pytest
import logging
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from tinydb.operations import add, set, increment
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.remote_connection import RemoteConnection

import src.lib.log as logger
import src.lib.base as base
import src.lib.config as configs
import src.lib.parser as parser
import src.lib.remote as remote
from src.lib.report import Report
from src.lib.fmanager import FileFolderManager

f = FileFolderManager()
g = Report()
# configs.setup_configs(option='log_level')
logger.setup_logger('Automation.conftest', 'Automation.log', rotate=True, stream=False)
log = logging.getLogger('Automation.conftest')
log.info('Automation log in conftest.py')


def pytest_addoption(parser):
    parser.addoption("--path", action="store", default=None, help="run all combinations")
    parser.addoption("--clearall", action="store_true", default=False, help="clears all repo folders")
    parser.addoption("--clearlogs", action="store_true", default=False, help="clears all logs")
    parser.addoption("--clearreports", action="store_true", default=False, help="clears all reports")
    parser.addoption("--clearscreenshots", action="store_true", default=False, help="clears all screenshots")
    parser.addoption("--screenshoton", action="store_true", default=False, help="triggers screenshot capture")
    parser.addoption("--env", action="store", default=None,
                     help="sets which environment/url to use either test,model,or prod")
    parser.addoption("--reportname", action="store", default=None,
                     help="sets/alters default report file name 'report.html'")
    parser.addoption("--convert", action="store", default=None,
                     help="specifies what spreadsheet to convert into test scripts, either 'tp' for test plan or \
                     'pa' for product availability")
    parser.addoption("--bdd", action="store_true", default=False, help="Run BDD Tests: True or False")
    parser.addoption("--func", action="store_true", default=False, help="Run Functional Tests: True or False")
    parser.addoption("--build_tag", action="store", default=None, help="Build Tag to run against. Ex. Model.0.0.1234")
    parser.addoption("--remote", action="store_true", default=False,
                     help="Run tests remotely. Remote configs should be readily prepared")
    parser.addoption("--baseline", action="store_false", default=False,
                     help="Capture baseline images for comparison. Flag only used for server.py")
    parser.addoption("--tunnel", action="store_true", default=False,
                     help="Run tests in proxy tunnel especially tests will be ran in test and dev environments.")
    parser.addoption("--bs", action="store_true", default=False,
                     help="Run tests in Browserstack testing platform. Default run in SauceLabs.")
    parser.addoption("--sso", action="store_true", default=False,
                     help="Run autoit script that needs SSO login in Remote execution.")


def pytest_configure(config):
    log.info("pytest_configure")
    # load up the settings
    f.workingdir = config.option.path
    configs.setup_configs(f.workingdir)
    f.clear_options(config.option)
    f.env = config.option.env
    f.reportname = config.option.reportname
    f.convert = config.option.convert
    f.sso = config.option.sso
    if not f.screenshoton:
        f.screenshoton = config.option.screenshoton

    #   set defaults for reporting
    if not config.option.collectonly:
        g.setup_report()
        build_tag = config.option.build_tag if base.config["build_tag"] == "" else base.config["build_tag"]
        with TinyDB(f.report_path(file_name="reports.json"), storage=CachingMiddleware(JSONStorage)) as db:
            db.upsert({
                "build": build_tag,
                "start_date": datetime.datetime.now().isoformat(' '),
                "duration": 0,
                "passed": 0,
                "failed": 0
            }, Query().build.exists())


def pytest_generate_tests(metafunc):
    if metafunc.config.option.remote or base.config['execution'] == 'remote':
        browser_list = remote.remote_setup(f.workingdir)  # load up remote browser configurations
    else:
        browser_list = [{'browserName': base.config['browser'], 'platform': "%s %s" % (system(), release())}]

    parse = parser.Parser(f.workingdir)
    print(parse)

    if 'drivers' in metafunc.fixturenames:
        if metafunc.config.option.bdd or metafunc.config.option.func:  # BDD and Functional Specific parametrization
            metafunc.parametrize("data", browser_list,
                                 ids=[browser['browserName'] for browser in browser_list],
                                 scope='function')
        else:
            test_cases = parse.get_datadict()
            tests = parser.proliferate(browser_list, test_cases, collect_only=metafunc.config.option.collectonly)
            metafunc.parametrize('data',
                                 tests,
                                 ids=[value['TestName'] for value in tests],
                                 scope='function')


@pytest.yield_fixture(scope='function')
def driver(request, data):
    """Driver Configuration"""
    # if the assignment below does not make sense to you please read up on object assignments.
    # The point is to make a copy and not mess with the original test spec.
    desired_caps = dict()
    test_name = request.node.name
    build_tag = request.config.option.build_tag if base.config["build_tag"] == "" else base.config["build_tag"]

    # Assign browser to data dict if in BDD or in Functional
    if request.config.option.bdd or request.config.option.func:
        data = {
            "browser": data
        }

    web_driver = None
    if request.config.option.remote or base.config['execution'] == 'remote':
        desired_caps.update(data['browser'])
        if request.config.option.bs:  # for BrowserStack
            username = os.getenv("BS_USERNAME")
            access_key = os.getenv("BS_ACCESS_KEY")
            selenium_endpoint = "https://%s:%s@hub-cloud.browserstack.com/wd/hub" % (username, access_key)
            desired_caps['os'] = "Windows"
            desired_caps['osVersion'] = "10"
            desired_caps['resolution'] = "1920x1080"
            # desired_caps['browserstack.idleTimeout'] = 300
            # desired_caps['browserstack.autoWait'] = 0
            if request.config.option.tunnel:
                from browserstack.local import Local
                # Creates an instance of Local
                bs_local = Local()
                # You can also set an environment variable - "BS_ACCESS_KEY".
                bs_local_args = {"key": access_key, "forcelocal": "true"}
                # Starts the Local instance with the required arguments
                bs_local.start(**bs_local_args)
                # Check if BrowserStack local instance is running
                print("BS Local is running? ")
                print(bs_local.isRunning())
                # # # Stop the Local instance in TEARDOWN
                desired_caps['browserstack.local'] = True
            if request.config.option.sso:
                desired_caps['unhandledPromptBehavior'] = "ignore"
        else:  # for SauceLabs
            username = base.config['username']
            access_key = base.config['access_key']
            # selenium_endpoint = "https://%s:%s@ondemand.saucelabs.com:443/wd/hub" % (username, access_key)
            selenium_endpoint = "http://%s:%s@ondemand.saucelabs.com/wd/hub" % (username, access_key)
            if request.config.option.tunnel:
                desired_caps['tunnelIdentifier'] = base.config['tunnel_id']
                desired_caps['parentTunnel'] = "optumtest"
            if request.config.option.sso:
                # Ensure there's sso.exe uploaded and saved in sauce storage prior using/running the test with sso
                desired_caps['prerun'] = {"executable": "sauce-storage:sso.exe",
                                          "args": ["--silent", "-a", "-q"], "background": True}
            desired_caps['acceptInsecureCerts'] = True
            desired_caps['screenResolution'] = "1920x1080"
            # desired_caps['recordLogs'] = False    # to on/off logs recording in SauceLabs
            # desired_caps['recordScreenshots'] = False # to on/off screenshots recording in SauceLabs
            # desired_caps['extendedDebugging'] = True    # to on/off extended debugging in SauceLabs
            # desired_caps['capturePerformance'] = True   # to on/off performance capturing in SauceLabs
            # desired_caps['public'] = "public restricted"  # to allow non-SauceLabs user to view recorded test
            # desired_caps['acceptSslCerts'] = False
            # desired_caps['idleTimeout'] = 200
        desired_caps['name'] = test_name
        if build_tag:
            desired_caps['build'] = build_tag
        # desired_caps['tags'] = str(data['Tags']).split("|")

        executor = RemoteConnection(selenium_endpoint, resolve_ip=False)
        web_driver = webdriver.Remote(
            command_executor=executor,
            desired_capabilities=desired_caps
        )
    else:
        browser = base.config['browser']
        if browser == 'ie':
            caps = webdriver.DesiredCapabilities.INTERNETEXPLORER
            caps['ignoreProtectedModeSettings'] = True
            caps['ignoreZoomSetting'] = True
            web_driver = webdriver.Ie('.\drivers\IEDriverServer.exe', log_file=".\logs\ie.log", capabilities=caps)
        elif browser == 'chrome':
            # chrome_opts = None
            chrome_opts = webdriver.ChromeOptions()
            chrome_opts.add_experimental_option('useAutomationExtension', False)
            # chrome_opts.add_argument('--disable-extensions')
            web_driver = webdriver.Chrome('.\drivers\chromedriver.exe', options=chrome_opts,
                                          service_log_path='.\logs\chrome.log')
            # web_driver = webdriver.Chrome(options=chrome_opts,
            #                               service_log_path='.\logs\chrome.log')
            # web_driver = webdriver.Chrome(options=chrome_opts, executable_path='.\drivers\chromedriver.exe',
            #                               service_log_path='.\logs\chrome.log')
        elif browser == 'firefox':
            web_driver = webdriver.Firefox(executable_path=".\drivers\geckodriver.exe", log_path='.\logs\gecko.log')
        elif browser == 'safari':
            web_driver = webdriver.Safari()
        elif browser == 'mobile':
            mobile_emulation = {'deviceName': base.config['device']}
            chrome_opts = webdriver.ChromeOptions()
            chrome_opts.add_experimental_option('mobileEmulation', mobile_emulation)
            web_driver = webdriver.Chrome(executable_path='.\drivers\chromedriver.exe', chrome_options=chrome_opts,
                                          service_log_path='.\logs\mobile.log')

    # This is specifically for SauceLabs plugin.
    # In case test fails after selenium session creation having this here will help track it down.
    # creates one file per test non ideal but xdist is awfulww
    if web_driver is not None:
        if not request.config.option.remote and base.config['execution'] == 'local':
            web_driver.maximize_window()
        # web_driver.implicitly_wait(base.config['timeout'] / 5)
    else:
        raise WebDriverException("Never created!")

    if request.config.option.func:
        suite = request.node._request.fspath.purebasename
        with TinyDB(f.report_path(file_name="reports.json"), storage=CachingMiddleware(JSONStorage)) as db:
            t_suites = db.table('_suites')
            q_suites = Query()
            if not t_suites.contains(q_suites.suite == suite):
                t_suites.insert({
                    "suite": suite,
                    "duration": 0,
                    "passed": 0,
                    "failed": 0
                })

            t_suites = db.table('_cases')
            q_suites = Query()
            t_suites.upsert({
                "suite": suite,
                "case": request.node.originalname
            }, (q_suites.suite == suite) & (q_suites.case == request.node.originalname))

    yield web_driver
    # Teardown starts here
    # report results
    log.info("Teardown/Report")
    node_id = None  # No session ID need for local runs
    e = None
    try:
        if request.config.option.remote or base.config['execution'] == 'remote':
            if request.config.option.bs:  # for BrowserStack
                if request.node.rep_call.failed:
                    web_driver.execute_script('browserstack_executor: {"action": "setSessionStatus", '
                                              '"arguments": {"status":"failed", "reason": "TEST FAILED!!!"}}')
                else:
                    web_driver.execute_script('browserstack_executor: {"action": "setSessionStatus", '
                                              '"arguments": {"status":"passed", "reason": "TEST PASSED!!!"}}')
                if request.config.option.tunnel:
                    # Stop the Local instance
                    bs_local.stop()
            else:  # for SauceLabs
                web_driver.execute_script("sauce:job-result=%s" % str(not request.node.rep_call.failed).lower())
            node_id = web_driver.session_id  # SauceLabs session ID

        if request.node.rep_call.failed and base.config['execution'] == 'local':
            g.capture_screen(web_driver, filename=str(test_name) + "_ERROR.png")
        else:
            if "thankyou" in web_driver.current_url or "Thank You" in web_driver.title:
                # g.capture_screen(web_driver, filename=str(test_name) + "_ThankYou.png")
                e = ""
                try:
                    policies = web_driver.find_elements_by_css_selector(".mc-thankyou-plan-details")
                    for policy in policies:
                        e = policy.text + "\n" + e
                finally:
                    with open(".\\reports\\%s_policyinfo.txt" % test_name, "w") as t:
                        t.write(e)
        web_driver.quit()
    except WebDriverException as exc:
        log.warning('Warning: The drivers failed to quit properly. Exception: %s', exc)

    setup_duration = round(request.node.rep_setup.duration)
    test_duration = round(request.node.rep_call.duration)
    error = request.node.rep_call.longrepr
    error = None if error is None else error.reprcrash.message
    if error is None:
        error = e
    if request.config.option.bdd or request.config.option.func:
        # Update reports for BDD runs
        if request.config.option.bdd:
            suite = request.node.rep_call.scenario['feature']['name']
            case = request.node.rep_call.scenario['name']
        # Update reports for Functional runs
        # TODO: Update reports for Functional runs
        else:
            # suite = request.node.name
            # case = request.node.name
            suite = request.node._request.fspath.purebasename
            case = request.node.originalname
        t_data = {
            "node_id": node_id,
            "case": case,
            "name": request.node.name,
            "passed": request.node.rep_call.passed,
            "setup_duration": setup_duration,
            "test_duration": test_duration,
            "error": error,
            "browser": data['browser']
        }
    else:
        # Update reports for CSV runs
        suite = data['SuiteName']
        t_data = {
            "node_id": node_id,
            "case": data['TestCase'],
            "name": data['TestName'],
            "passed": request.node.rep_call.passed,
            "setup_duration": setup_duration,
            "test_duration": test_duration,
            "error": error,
            "browser": data['browser']
        }
    with TinyDB(f.report_path(file_name="reports.json"), storage=CachingMiddleware(JSONStorage)) as db:
        t_suites = db.table("_suites")
        t_tests = db.table("_tests")
        q_suites = Query()
        q_tests = Query()
        t_tests.upsert(t_data, (q_tests.case == t_data["case"]) & (q_tests.name == t_data["name"]))
        if request.node.rep_call.passed:
            db.update(increment('passed'), doc_ids=[1])
            t_suites.update(increment('passed'), q_suites.suite == suite)
        else:
            db.update(increment('failed'), doc_ids=[1])
            t_suites.update(increment('failed'), q_suites.suite == suite)
        t_suites.update(add('duration', setup_duration + test_duration), q_suites.suite == suite)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    print("pytest_runtest_makereport()")
    # this sets the result as a test attribute for SauceLabs reporting.
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set an report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)
    # setattr(rep, "f", f)


def pytest_bdd_before_scenario(request, feature, scenario):
    suite = feature.name
    with TinyDB(f.report_path(file_name="reports.json"), storage=CachingMiddleware(JSONStorage)) as db:
        t_suites = db.table('_suites')
        q_suites = Query()
        if not t_suites.contains(q_suites.suite == suite):
            t_suites.insert({
                "suite": suite,
                "duration": 0,
                "passed": 0,
                "failed": 0
            })

        t_suites = db.table('_cases')
        q_suites = Query()
        t_suites.upsert({
            "suite": suite,
            "case": scenario.name
        }, (q_suites.suite == suite) & (q_suites.case == scenario.name))


def pytest_terminal_summary(terminalreporter, exitstatus):
    log.info("pytest_terminal_summary")
    if not terminalreporter.config.option.collectonly:
        end = datetime.datetime.now()
        with TinyDB(f.report_path(file_name="reports.json"), storage=CachingMiddleware(JSONStorage)) as db:
            start = db.get(Query())['start_date']
            start = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S.%f")
            db.update(set("duration", (end - start).seconds), doc_ids=[1])
        g.gen_htmlreport()
        f.backupfiles(f.workingdir, f.reportfolder, ['.txt', '.xml', '.html', '.json'])
        f.backupfiles(f.workingdir, f.logfolder, ['.log', '.policy_num'])
        f.backupfiles(f.workingdir, f.screenshotfolder, ['.png'])

        if base.ws['server'] is not None:
            server = base.ws['server']
            total_passed = []
            total_failed = []
            if 'passed' in terminalreporter.stats:
                total_passed = terminalreporter.stats['passed']
            if 'failed' in terminalreporter.stats:
                total_failed = terminalreporter.stats['failed']
            stats = "%i Passed and %i Failed" % (len(total_passed), len(total_failed))
            server.send_message_to_all(stats)
