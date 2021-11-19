# -*- coding: utf-8 -*-
import re
import os
import time
import uuid
from logging import getLogger
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, \
    StaleElementReferenceException, NoSuchElementException
# from PIL import Image

import src.lib.base as base
from src.lib.elements import Elements
from src.lib.checkEmail import CheckEmail
from src.lib.fmanager import FileFolderManager

f = FileFolderManager()


class Actions(Elements):
    """Action Class contains all the action methods to test the Application"""

    def __init__(self, test_name, driver):
        Elements.__init__(self)
        self.test_name = test_name
        self.test_type = None
        self.log = getLogger(test_name + ".Actions")
        self.driver = driver
        self.rest = WebDriverWait(self.driver, base.config['timeout'])
        self.plan = None
        self.plan_dom = None
        self.plan_page = 0
        self.plan_found = False
        self.capture_ = {}
        self.uid = None

    def __get_element(self, spec, log):
        """get element disctionary
        :param spec: to be searched in dictionary
        :param log: Logger object
        :return: string value
        """
        element = None
        if spec:
            element = Elements.get_data(self, spec)
            if not element:
                log.error('Element "%s" NOT found in dictionary' % spec)
                assert element, 'Element "%s" NOT found in dictionary' % spec

        return element

    def __get_webelement(self, css, log, persist_fail=True):
        """
        Retrieve WebELement Object
        :param css: CSS Selector
        :param log: Logger Object
        :return: WebElement Object
        """
        element = None
        try:
            if self.plan is not None:
                element = self.plan.find_element_by_css_selector(css)
            else:
                element = self.driver.find_element_by_css_selector(css)
        except Exception as e:
            error_message = 'Get WebElement "%s" Exception: %s' % (css, str(e).strip())
            log.error(error_message)
            if persist_fail:
                assert 0, error_message

        return element

    @staticmethod
    def __enabled(webelement, log):
        """
        Check if Element is enabled True/False
        :param webelement: WebElement Object
        :param log: Logger Object
        :return: Boolean
        """
        enabled = False
        if webelement is not None:
            try:
                enabled = webelement.is_enabled()
            except Exception as e:
                message = 'Element Enabled Exception: %s' % str(e).strip()
                log.warning(message)

        return enabled

    def __clickable(self, css, log):
        """
        Check if element is Clickable
        :param css: CSS Selector
        :param log: Logger Object
        :return: WebElement or None
        """
        element = None
        try:
            element = self.rest.until(ec.element_to_be_clickable((By.CSS_SELECTOR, css)))
        except TimeoutException as e:
            error_message = 'Element Clickable Wait Timeout: %s' % str(e).strip()
            log.warning(error_message)
        except Exception as e:
            error_message = 'Element Clickable Wait Exception: %s' % str(e).strip()
            log.warning(error_message)

        return element

    def __located(self, css, log):
        """
        Check if element is in the page
        :param css: CSS Selector
        :param log: Logger Object
        :return: WebElement or None
        """
        element = None
        try:
            if self.plan is not None:
                element = self.__get_webelement(css, log)
            else:
                element = self.rest.until(ec.presence_of_element_located((By.CSS_SELECTOR, css)))
        except TimeoutException as e:
            error_message = 'Element Locate Wait Timeout: %s' % str(e).strip()
            log.warning(error_message)
        except Exception as e:
            error_message = 'Element Locate Wait Exception: %s' % str(e).strip()
            log.warning(error_message)

        return element

    def __visible(self, css, log, invi=False):
        """
        Check if element is located and visible
        :param css: CSS Selector
        :param log: Logger Object
        :return: WebElement or None
        """
        element = None
        try:
            if self.plan is not None:
                _element = self.plan.find_element_by_css_selector(css)
                displayed = _element.is_displayed()
                if displayed:
                    element = _element
            else:
                element = self.rest.until(ec.visibility_of_element_located((By.CSS_SELECTOR, css)))
        except TimeoutException as e:
            if invi:
                return False
            error_message = 'Element Visible Wait Timeout: %s' % str(e).strip()
            log.warning(error_message)
        except Exception as e:
            if invi:
                return False
            error_message = 'Element Visible Wait Exception: %s' % str(e).strip()
            log.warning(error_message)

        return element

    def testname(self, step, data, spec):
        log = getLogger('%s.testname.%i' % (self.test_name, step))
        log.info('TestName: %s' % data)

    def description(self, step, data, spec):
        log = getLogger('%s.description.%i' % (self.test_name, step))
        log.info('Description: %s' % data)

    def type(self, step, data, spec):
        self.test_type = data

    def tags(self, step, data, spec):
        self.type(step, data, spec)

    def get_url(self, step, data, spec, clear_cookie=True):

        log = getLogger('%s.url.%i' % (self.test_name, step))
        log.info("Param data: " + data)
        log.info("Param spec: " + spec)
        spec = self.__get_element(spec, log)

        if clear_cookie and base.config['execution'] == 'local':
            self.driver.delete_all_cookies()
            self.driver.refresh()
        self.driver.get(data)
        print('finished')
        try:
            self.rest.until(lambda driver: self.driver.title.startswith(spec))

        except TimeoutException:
            error_message = 'Page Title expected: "%s" but actual: "%s"' % (spec, self.driver.title)
            self.log.error(error_message)
            assert 0, error_message


    def url(self, step, data, spec, clear_cookie=True):
        # https = 'https://'
        # uho = "uhone"
        # ghi = "gethealthinsurance"
        # mnt = "maintenance"
        # hm = "healthmarkets"
        # site = ""
        #
        # if f.env:
        #     if mnt in str(data):
        #         site = mnt
        #     elif uho in str(data):
        #         site = uho
        #     elif ghi in str(data):
        #         site = ghi
        #     else:
        #         site = data
        #
        #     regex = https + "(.*?)." + site
        #     matches = re.search(regex, str(data))
        #     if matches:
        #         env = matches.group(1)
        #         if env and f.env == "prod":
        #             data = str(data).replace(env + ".", "www.")  # added wwww. for prod
        #         else:
        #             temp = env
        #             temp_f = f.env
        #             data = str(data).replace(env, f.env)
        #     else:
        #         if f.env != "prod":
        #             data = str(data).replace(https, https + f.env + '.')

        log = getLogger('%s.url.%i' % (self.test_name, step))
        log.info("Param data: " + data)
        log.info("Param spec: " + spec)
        spec = self.__get_element(spec, log)

        if clear_cookie and base.config['execution'] == 'local':
            self.driver.delete_all_cookies()
            self.driver.refresh()

        if clear_cookie and base.config['release'] and f.env != 'prod' and site != mnt:
            time.sleep(1)
            self.release(step, base.config['release'], None)

        if 'tab:' in data[0:4]:
            data = data.replace('tab:', '').strip()

            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[len(self.driver.window_handles) - 1])
            self.driver.get(data)
        else:
            self.driver.get(data)

        try:
            self.rest.until(lambda driver: self.driver.title.startswith(spec))

        except TimeoutException:
            error_message = 'Page Title expected: "%s" but actual: "%s"' % (spec, self.driver.title)
            self.log.error(error_message)
            assert 0, error_message

    def wait(self, step, data, spec):
        log = getLogger('%s.wait.%i' % (self.test_name, step))
        log.info("Param data: " + data)
        log.info("Param spec: " + spec)
        self.pause(0, "1", "Second")

        element = self.__get_element(spec, log)
        web_element = self.__get_webelement(element, log, False)

        data = _multi_param(data)
        check = None
        if len(data) > 1:
            check = data[0].lower()

        try:
            if check is None:
                displayed = web_element.is_displayed()
                if displayed:
                    self.rest.until_not(ec.visibility_of(web_element))
            elif check == 'visibility_of':
                self.rest.until(ec.visibility_of(web_element))
        except TimeoutException as e:
            log.warning('Element Wait Timeout: %s' % str(e).strip())
        except StaleElementReferenceException as e:
            log.warning('Element Wait StaleElement: %s' % str(e).strip())
        except NoSuchElementException as e:
            log.warning('Element Wait NoSuchElement: %s' % str(e).strip())
        except Exception as e:
            log.warning('Element Wait Exception: %s' % str(e).strip())

    def click(self, step, data, spec):
        log = getLogger('%s.click.%i' % (self.test_name, step))
        log.info("Param data: " + data)
        log.info("Param spec: " + spec)

        element = self.__get_element(spec, log)
        if self.plan is not None:
            web_element = self.plan.find_element_by_css_selector(element)
        else:
            web_element = self.__clickable(element, log)
        if not web_element:
            error_message = 'WebElement Error, value: "%s" or "%s" element not found.' % (element, spec)
            log.error(error_message)
            assert 0, error_message

        self.scroll(step, 'Element: %s' % data, spec)

        try:
            web_element.click()
        except Exception as e:
            error_message = 'Click Exception: %s' % str(e).strip()
            log.error(error_message)
            assert 0, error_message

    def double_click(self, step, data, spec):
        log = getLogger('%s.double_click.%i' % (self.test_name, step))
        log.info("Param data: " + data)
        log.info("Param spec: " + spec)

        element = self.__get_element(spec, log)
        if self.plan is not None:
            web_element = self.plan.find_element_by_css_selector(element)
        else:
            web_element = self.__clickable(element, log)
        if not web_element:
            error_message = 'WebElement Error, value: "%s" or "%s" element not found.' % (element, spec)
            log.error(error_message)
            assert 0, error_message

        self.scroll(step, 'Element: %s' % data, spec)

        try:
            action_chains = ActionChains(self.driver)
            action_chains.move_to_element(web_element)
            action_chains.double_click(web_element).perform()
        except Exception as e:
            error_message = 'Double Click Exception: %s' % str(e).strip()
            log.error(error_message)
            assert 0, error_message

    def check(self, step, data, spec, test_type=None, broker=None):
        log = getLogger('%s.check.%i' % (self.test_name, step))
        log.info("Param data: " + data)
        log.info("Param spec: " + spec)
        if test_type is None:
            test_type = self.test_type

        error_message = 'Email/Element/Empty: Value'
        if ':' not in data:
            log.error(error_message)
            assert 0, error_message

        deta = _multi_param(data)
        web_element = self.__get_element(spec, log)
        way = deta[0].lower()
        if way == 'email':
            self.email(step, data, spec, test_type, broker)
        elif way == 'element':
            element_found = len(self.driver.find_elements_by_css_selector(web_element))
            if element_found == 1:
                return True
            else:
                return False
        elif way == 'empty':
            if self.driver.find_element_by_css_selector(web_element).get_property("value") == "":
                return True
            else:
                return False
        else:
            log.error(error_message)
            assert 0, error_message

    def find(self, step, data, spec):
        log = getLogger('%s.find.%i' % (self.test_name, step))
        log.info("Param data: " + data)
        log.info("Param spec: " + spec)

        error_message = 'Elements/Text: Value'
        if ':' not in data:
            log.error(error_message)
            assert 0, error_message

        data = _multi_param(data)
        web_element = self.__get_element(spec, log)
        way = data[0].lower()
        if way == 'elements':
            list_ = self.driver.find_elements_by_css_selector(web_element)
            return list_
        elif way == 'text':
            try:
                text = self.driver.find_element_by_css_selector(web_element).text
                if text == '':
                    text = web_element.get_attribute('value')
                return text
            except Exception as e:
                error_message = "Element not found. Exception: %s" % str(e).strip()
                log.error(error_message)
                assert 0, error_message
        else:
            log.error(error_message)
            assert 0, error_message

    def choose(self, step, data, spec):
        log = getLogger('%s.choose.%i' % (self.test_name, step))
        log.info("Param data: " + data)
        log.info("Param spec: " + spec)

        raw_data = data
        raw_spec = spec
        data = _multi_param(data, "|")
        spec = _multi_param(spec, "|")
        if len(data) != len(spec):
            error_message = 'Argument length did not match! data: %i spec: %i' % (len(data), len(spec))
            log.error(error_message)
            assert 0, error_message

        if "<ghi_plan>" in spec:
            # Get the number of GetHealthInsurance plans found
            element = self.__get_element("<ghi_plan_count>", log)
            plan_count = self.__located(element, log)
            if plan_count is None:
                error_message = "Plan Count on GHI error"
                log.error(error_message)
                assert 0, error_message
            plan_count = plan_count.text
            try:
                scroll_x = float(plan_count) / 10
            except ValueError as e:
                error_message = "ValueError: %s" % str(e).strip()
                log.warning(error_message)
            if scroll_x > 1:
                while scroll_x >= 1:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    scroll_x -= 1

        while self.check(step, "Element: See More Plans", ".mc-planList-see-more[aria-hidden=false]"):
            self.click(step, "See More Plans button link", "[data-ng-click*='paging']")
            self.wait(step, "Loading", "<uhone_loading>")

        plan_element = self.__get_element(spec[0], log)
        plan_web_element = self.driver.find_elements_by_css_selector(plan_element)
        if (plan_web_element is None) or (len(plan_web_element) < 1):
            error_message = "Unable to find any plans"
            log.error(error_message)
            assert 0, error_message

        if self.plan_page > 0:
            del plan_web_element[0:self.plan_page]

        self.plan_found = False
        for p, plan in enumerate(plan_web_element):
            index = p + 1 + self.plan_page
            self.plan = plan
            self.plan_dom = "%s:nth-child(%i)" % (plan_element, index)
            score = 0
            top_score = len(spec) - 2
            rng = list(range(1, top_score+1))
            for i in rng:
                exp_val = data[i].strip()
                element = self.__get_element(spec[i], log)
                web_element = self.__get_webelement(element, log)
                txt = None
                try:
                    txt = web_element.text
                    if txt == '':
                        txt = web_element.get_attribute('value')
                except Exception as e:
                    error_message = "Unable to process plan in plans object. Exception: %s" % str(e).strip()
                    log.error(error_message)
                    assert 0, error_message
                finally:
                    if txt is not None:
                        txt = str(txt).strip()
                        if exp_val == txt:  # or (exp_val in txt):
                            score += 1
                            self.log.debug("Plan Scored %d/%d from %s", score, top_score, spec[i])
                        else:
                            break
            if score == top_score:
                log.debug("Found the plan %d/%d", score, top_score)
                act = 'click'
                i = top_score + 1
                d = data[i]
                if ':' in data[i]:
                    s = _multi_param(data[i])
                    act = s[0].lower()
                    try:
                        d = "%s: %s" % (s[1], s[2])
                    except IndexError:
                        d = s[1]
                do = getattr(self, act)
                if act == "capture":
                    return do(step, d, spec[i])
                do(step, d, spec[i])
                self.plan_found = True
                self.plan = None
                break
            else:
                if top_score >= 2:
                    pagination_element = "[data-ng-click*='paging']"
                    expand = self.__clickable(pagination_element, log)
                    if expand is not None:
                        if index == len(plan_web_element) + self.plan_page:
                            self.plan = None
                            self.plan_page = index
                            self.click(step, 'See More Plans...', pagination_element)
                            self.wait(step, "Loading", "<uhone_loading>")
                            self.choose(step, raw_data, raw_spec)

        if not self.plan_found:
            error_message = 'Plan %s not found!' % data
            log.error(error_message)
            assert 0, error_message

    def email(self, step, data, spec, test_type=None, broker=None):
        log = getLogger('%s.email.%i' % (self.test_name, step))
        log.info("Param data: " + data)
        log.info("Param spec: " + spec)

        if ':' not in data:
            error_message = 'Expected Received: Email'
            log.error(error_message)
            assert 0, error_message
        data = _multi_param(data)
        email_file = self.test_name + ".html"
        check_email = CheckEmail()

        if data[0].lower() == 'email':
            exp_title = None
            search_duration = 90
            uid = None
            url = None
            while not exp_title:
                url, exp_title, uid = check_email.get_email(test_type, email_file, search_duration, data[1], broker)
            self.uid = uid

            if exp_title == 'search_limit_reached':
                log.error('Email not found after "%s" seconds', str(search_duration))
                assert 0, 'Email not found after "%s" seconds' % str(search_duration)
            if not url:
                log.error('Email for specific applicant "%s" not found!', str(data[1]))
                assert 0, 'Email for specific applicant "%s" not found!' % str(data[1])
            # Open email html file
            # self.url(step, url, exp_title, clear_cookie=False)
            self.url(step, url, spec, clear_cookie=False)
            # if base.config['execution'] == 'local':
            #     # Click link in the email content
            #     self.click(step, 'Link', 'body a')

    def enter(self, step, data, spec, mask=False):
        log = getLogger('%s.enter.%i' % (self.test_name, step))
        masked = data
        if mask:
            masked = data[-4:].rjust(len(data), "*")
        log.info("Param data: " + masked)
        log.info("Param spec: " + spec)

        data = _gen_rand(data)

        element = self.__get_element(spec, log)
        web_element = self.__get_webelement(element, log)
        enabled = self.__enabled(web_element, log)
        if enabled:
            try:
                scr = 'document.querySelector("%s").select();' % element
                self.driver.execute_script(scr)
            except Exception as e:
                message = 'Value Select Exception: %s' % str(e).strip()
                log.warning(message)

            try:
                web_element.clear()
                if len(data.strip()) > 0:
                    web_element.send_keys(data)
            except Exception as e:
                error_message = 'Input Data Exception: %s' % str(e).strip()
                log.error(error_message)
                assert 0, error_message

    def hover(self, step, data, spec):
        log = getLogger('%s.hover.%i' % (self.test_name, step))
        log.info("Param data: " + data)
        log.info("Param spec: " + spec)

        element = self.__get_element(spec, log)
        web_element = self.__get_webelement(element, log)
        action_chains = ActionChains(self.driver)
        action_chains.move_to_element(web_element)
        action_chains.perform()

    def key(self, step, data, spec):
        log = getLogger('%s.key.%i' % (self.test_name, step))
        log.info("Param data: " + data)
        log.info("Param spec: " + spec)

        try:
            key = getattr(Keys, str(data).upper())
        except AttributeError:
            error_message = 'Key "%s" Invalid ' % data
            log.error(error_message)
            assert 0, error_message

        self.enter(step, key, spec)
        # element = self.__get_element(spec, log)
        # web_element = self.__get_webelement(element, log)
        # if web_element:
        #     web_element.send_keys(key)
        # else:
        #     error_message = 'Error sending input key "%s"' % data
        #     log.error(error_message)
        #     assert 0, error_message

    def pause(self, step, data, spec):
        log = getLogger('%s.pause.%i' % (self.test_name, step))
        log.info("Param data: " + data)
        log.info("Param spec: " + spec)

        time.sleep(int(data))

    def scroll(self, step, data, spec):
        log = getLogger('%s.scroll.%i' % (self.test_name, step))
        log.info("Param data: " + data)
        log.info("Param spec: " + spec)

        if ':' not in data:
            error_message = 'Expected Page/Element: None/ElementName'
            log.error(error_message)
            assert 0, error_message

        fault = None
        data = _multi_param(data)
        if data[0].lower() == 'element':
            element = self.__get_element(spec, log)
            if self.plan is not None:
                element = "%s %s" % (self.plan_dom, element)
            web_element = self.__located(element, log)
            if web_element is None:
                error_message = "WebElementError: value is None and can't scroll to it"
                log.error(error_message)
                assert 0, error_message

            try:
                fault = "Scroll visibility checking"
                # http://jsfiddle.net/gcvL2ogj/15/
                scr = 'function isScrolledIntoView(elem){ ' \
                      'var docViewTop = window.scrollY; ' \
                      'var docViewBottom = docViewTop + window.innerHeight; ' \
                      'var elemTop = document.querySelector(elem).getBoundingClientRect().top + docViewTop - 100; ' \
                      'var elemBottom = elemTop + document.querySelector(elem).getBoundingClientRect().height + 100; ' \
                      'return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop)); } ' \
                      'return isScrolledIntoView("%s");' % str(element)
                located = self.driver.execute_script(scr)
                if not located:
                    fault = "Element scroll to center"
                    position = web_element.location
                    scr = 'function scroll_to_center(elem, pos){' \
                          'element = document.querySelector(elem);' \
                          'elementRect = element.getBoundingClientRect();' \
                          'absoluteElementTop = elementRect.top + window.pageYOffset;' \
                          'middle = absoluteElementTop - (window.innerHeight / 2);' \
                          'window.scrollTo(pos, middle);}' \
                          'scroll_to_center("%s", "%i");' % (str(element), position['x'])
                    self.driver.execute_script(scr)
            except Exception as e:
                error_message = 'Scroll Exception on > %s: %s' % (fault, str(e).strip())
                log.error(error_message)
                assert 0, error_message
        elif data[0].lower() == 'page':
            page_height = self.driver.execute_script('return document.body.scrollHeight')
            screen_height = self.driver.execute_script('return window.screen.height')
            scroll_height = screen_height - 200
            if screen_height < page_height:
                while screen_height < page_height:
                    time.sleep(1.5)
                    self.driver.execute_script('window.scrollTo(0, %i)' % screen_height)
                    screen_height += scroll_height
                    time.sleep(1.5)

    def select(self, step, data, spec):
        log = getLogger('%s.select.%i' % (self.test_name, step))
        log.info("Param data: " + data)
        log.info("Param spec: " + spec)

        if ':' not in data:
            error_message = 'Expected Field/Questions/Question: Dropdown Value/Yes/No'
            log.error(error_message)
            assert 0, error_message

        data = _multi_param(data)
        element = self.__get_element(spec, log)
        if 'select' in element:
            web_element = self.__get_webelement(element, log)
            enabled = self.__enabled(web_element, log)
            if enabled:
                try:
                    for opt in web_element.find_elements_by_tag_name('option'):
                        text_ = str(opt.text).lower()
                        data_ = data[1].lower()
                        if text_.strip() == data_.strip():
                            opt.click()
                            break
                except Exception as e:
                    error_message = 'Find Option Value Exception: %s' % str(e).strip()
                    log.error(error_message)
                    assert 0, error_message
            else:
                error_message = '"%s" is not enabled. Element: "%s"' % (data[0].lower(), element)
                log.error(error_message)
                assert 0, error_message
        elif 'questions' in data[0].lower():
            options = self.driver.find_elements_by_css_selector(element)
            if options:
                for i, option in enumerate(options):
                    element_id = False
                    element_enabled = None
                    try:
                        element_id = option.get_attribute('id')
                        element_enabled = self.rest.until(ec.visibility_of_element_located((By.ID, element_id))) \
                            if element_id != "" else None
                    except Exception as e:
                        error_message = 'Exception: %s' % str(e).strip()
                        log.warning(error_message)

                    if element_id and element_enabled:
                        btn = self.__clickable("#%s" % str(element_id), log)
                        if btn:
                            time.sleep(1)
                            self.scroll(step, 'Element:', '#%s' % str(element_id))
                            btn.click()
                        else:
                            assert 0, btn
                    else:   # Else the option does not have an ID then send Click directly on option instead
                        option.click()
            else:
                error_message = 'Unable to process "%s". Element: "%s"' % (data[0].lower(), element)
                log.error(error_message)
                assert 0, error_message

    def verify(self, step, data, spec):
        log = getLogger('%s.verify.%i' % (self.test_name, step))
        log.info("Param data: " + data)
        log.info("Param spec: " + spec)

        error_message = 'Displayed/Expected/Link/Text/Button/Input/Part_Number: Value'
        if ':' not in data:
            log.error(error_message)
            assert 0, error_message

        data = _multi_param(data)
        element = self.__get_element(spec, log)
        way = data[0].lower()
        if way == 'displayed':
            visible = self.__visible(element, log)
            if not visible:
                error_message = '"%s" is not visible. Element: "%s"' % (data[1].lower(), element)
                log.error(error_message)
                assert 0, error_message
        elif way == 'no':
            visible = self.__visible(element, log, invi=True)
            if visible:
                error_message = '"%s" is STILL VISIBLE. Element: "%s"' % (data[1].lower(), element)
                log.error(error_message)
                assert 0, error_message
        elif way in ['expected', 'link', 'text', 'button']:
            act_value = None
            if element in list(self.capture_.keys()):
                act_value = self.capture_[element]
                if data[1] == 'uid':
                    data[1] = self.uid
            else:
                web_element = self.__located(element, log)
                try:
                    act_value = web_element.text
                    if act_value == '':
                        act_value = web_element.get_attribute('value')
                    if "\"" in str(act_value):
                        act_value = str(act_value).replace("\"", "")
                except Exception as e:
                    log.warning(e)

            # if data[1] != str(act_value).strip():
            if (data[1]).lower() != str(act_value).strip().lower():
                error_message = 'Expected "%s" does not match with "%s"' % (data[1], str(act_value).strip())
                log.error(error_message)
                assert 0, error_message
        elif way == 'input':
            act_type = None
            web_element = self.__located(element, log)
            try:
                act_type = web_element.get_attribute('type')
            except Exception as e:
                log.warning(e)

            if data[1].lower() != str(act_type):
                error_message = 'Expected "%s" does not match with "%s"' % (data[1], str(act_type))
                log.error(error_message)
                assert 0, error_message
        elif way == 'part_number':
            web_element = self.__located(element, log)
            href = None
            exp_value = "%s:%s" % (data[1], data[2])
            try:
                href = web_element.get_attribute('href')
            except Exception as e:
                log.error(e)
                assert 0, e
            if exp_value != href:
                error_message = "HREF Mismatch: %s | | %s" % (exp_value, href)
                log.error(error_message)
                assert 0, error_message
        elif way == 'enabled':
            web_element = self.__visible(element, log)
            act_value = self.__enabled(web_element, log)
            exp_value = False
            if data[1].lower() == "true":
                exp_value = True
            if exp_value != act_value:
                error_message = 'Element "%s" Enabled expected "%s" but actually "%s"' % \
                                (element, data[1], act_value)
                log.error(error_message)
                assert 0, error_message
        elif way == 'selected':
            web_element = self.__located(element, log)
            exp_value = data[1].lower()
            if exp_value != 'true' and exp_value != 'false':
                exp_value = data[1]  # reassign it, transforming it to lower() earlier will make life miserable later on
                selected = Select(web_element)
                act_value = selected.first_selected_option.text
            else:
                exp = False
                if exp_value == 'true':
                    exp = True
                try:
                    act_value = web_element.is_selected()
                finally:
                    exp_value = exp

            if act_value != exp_value:
                error_message = 'Element "%s" Selected expected "%s" but actually "%s"' % \
                                (element, exp_value, act_value)
                log.error(error_message)
                assert 0, error_message
        elif way == 'title':
            try:
                self.rest.until(lambda driver: self.driver.title.startswith(data[1]))
            except TimeoutException:
                error_message = 'Page Title expected: "%s" but actual: "%s"' % (data[1], self.driver.title)
                self.log.error(error_message)
                assert 0, error_message
        else:
            log.error(error_message)
            assert 0, error_message

    def release(self, step, data, spec):
        log = getLogger('%s.release.%i' % (self.test_name, step))
        log.info("Param data: " + data)
        # log.info("Param spec: " + spec)

        if f.env == 'prod':
            return False

        date = data

        self.wait(step, "Loading", "<uhone_loading>")
        # Broker Portal still uses the old dom
        if '/broker' in str(self.driver.current_url).lower():
            date_link = self.__get_element("[id$=pnlMaximizeServerDateChooser]", log)
            date_fld = self.__get_element("[id$=txtServerDate]", log)
            date_btn = self.__get_element("<server_date_bttn>", log)

            c1 = self.__get_webelement(date_link, log)
            if date != '' and date not in c1.text:
                c1.click()
                c2 = self.__get_webelement(date_fld, log)
                c2.clear()
                c2.send_keys(date)
                c2.send_keys(Keys.TAB)
                time.sleep(0.5)
                self.wait(step, "Loading", "<uhone_loading>")
                c3 = self.__get_webelement(date_btn, log)
                c3.click()
                time.sleep(1)
                self.wait(step, "Loading", "<uhone_loading>")

        # UHOne/GHI uses the rewrite dom
        else:
            date_link = self.__get_element("<server_date_lnk>", log)
            date_fld = self.__get_element("<server_date_fld>", log)
            c1 = self.__get_webelement(date_link, log)
            sdate = str(c1.text).split("Server Date: ")

            if date != '' and date not in sdate[1]:
                c1.click()
                c2 = self.__get_webelement(date_fld, log)
                c2.clear()
                c2.send_keys(date)
                time.sleep(1)
                self.wait(step, "Loading", "<uhone_loading>")

    def capture(self, step, data, spec):
        log = getLogger('%s.capture.%i' % (self.test_name, step))
        log.info("Param data: " + data)
        log.info("Param spec: " + spec)
        capt = self.capture.__name__
        page, eliment = False, False
        if ("value" in data or "text" in data) and ":" in data:
            element = self.__get_element(spec, log)
            web_element = self.__get_webelement(element, log)
            try:
                val = web_element.text
                if val == '':
                    val = web_element.get_attribute('value')
            except Exception as e:
                error_message = "Unable to FIND plan in plans object. Exception: %s" % str(e).strip()
                log.error(error_message)
                assert 0, error_message
            return val
        elif str(step).isdigit() and ':' in data:
            data = _multi_param(data)
            name = str(data[1]).strip()
            if '/' in name:
                name = name.replace('/', '_')
            elif ' ' in name:
                name = name.replace(' ', '_')
            if data[0].lower() == 'element':
                eliment = True
            elif data[0].lower() == 'page':
                page = True
        elif not str(step).isdigit():
            akt = ['click', 'enter', 'choose', 'hover', 'key', 'scroll', 'select', 'verify']
            capt = 'auto_capture'
            strng = _multi_param(step, '_')
            act = str(strng[1]).lower().strip()
            if act not in akt:
                return
            if act == 'verify' and 'title' in str(data).lower():
                page = True
            eliment = True
            name = self.test_name + '_step_' + str(step)
        else:
            log = getLogger('%s.%s.%s' % (self.test_name, capt, step))
            error_message = 'Expected Page/Element: None/ElementName'
            log.error(error_message)
            assert 0, error_message
        log = getLogger('%s.%s.%s' % (self.test_name, capt, step))
        log.info("Param data: " + data)
        log.info("Param spec: " + spec)
        if page:
            self.driver.save_screenshot(os.path.join(f.workingdir, "%s\\%s.png" % (f.screenshotfolder, name)))
        # TODO: Update PIL incompatibilities in Python 3
        # elif eliment:
        #     element = self.__get_element(spec, log)
        #     # web_element = self.__located(element, log)
        #     try:
        #         ele = self.__get_webelement(element, log)
        #         # Get entire page screenshot
        #         location = ele.location
        #         size = ele.size
        #         path_ = os.path.join(f.workingdir, f.screenshotfolder)
        #         file_ = os.path.join(path_, name + '.png')
        #         self.drivers.save_screenshot(file_)  # saves screenshot of entire page
        #         im = Image.open(file_)  # uses PIL library to open image in memory
        #         left = location['x']
        #         top = location['y']
        #         right = location['x'] + size['width']
        #         bottom = location['y'] + size['height']
        #         im = im.crop((left, top, right, bottom))  # defines crop points
        #         im.save(file_)  # saves new cropped image
        #     except Exception as e:
        #         error_message = 'Capture Exception: %s' % str(e).strip()
        #         log.error(error_message)
        #         assert 0, error_message
        # #TO DO: implement policy capture
        # elif 'policy' in data[0].lower:
        #     policies = self.__get_element(spec, log)
        #     # policies = self.drivers.find_elements_by_css_selector(element)
        #     values = [policy.text for policy in policies]
        #     policy_nums = os.path.join(os.path.join(f.workingdir, f.logfolder),
        #                                str(data[1]).strip() + '.policy_num')
        #     file_ = open(policy_nums, "a")
        #     # file_.write(self.platform + ' - ' + self.drivers.desired_capabilities['browserName'] + ':\n')
        #     file_.write('browser name:\n')
        #     for value in values:
        #         file_.write('- ' + value + '\n')
        #     file_.close()
        else:
            element = self.__get_element(spec, log)
            self.capture_[str(data[0]).strip()] = element.text

    def switch(self, step, data, spec):
        log = getLogger('%s.switch.%i' % (self.test_name, step))
        log.info("Param data: " + data)
        log.info("Param spec: " + spec)

        error_message = 'Window/Frame: Page Title/Main/iFrame/Parent Frame'
        if ':' not in data:
            log.error(error_message)
            assert 0, error_message

        data = _multi_param(data)
        element = self.__get_element(spec, log)
        way = data[0].lower()
        window_title = data[1].lower()
        tab_index = int(spec)

        if way == 'window':
            if (tab_index <= len(self.driver.window_handles)):
                self.driver.switch_to.window(self.driver.window_handles[tab_index-1])
                if (window_title != self.driver.title.lower()):
                    error_message = 'Page Title expected: "%s" but actual: "%s"' % (window_title, self.driver.title.lower())
                    self.log.error(error_message)
                    assert 0, error_message
            else:
                error_message = 'Tab "%s" is not available.' % (spec)
                log.error(error_message)
                assert 0, error_message
        elif way == 'window' and window_title == 'main':
            self.driver.switch_to.window('main')
        # example: step | "Parent Page" | "Parent/parent/PARENT"
        elif way == 'frame' and spec in ['Parent', 'parent', 'PARENT']:
            self.driver.switch_to.parent_frame()
        elif way == 'frame' and window_title == 'iframe':
            element = self.__get_element(spec, log)
            self.driver.switch_to_frame(self.driver.find_element_by_css_selector(element))
        else:
            log.error(error_message)
            assert 0, error_message



def _gen_rand(char):
    """
    Replace $ with a random key
    :param char: string containing $
    :return: string with random key
    """
    out = char
    if '$' in char:
        uid = str(uuid.uuid4()).split('-')
        out = char.replace('$', uid[1])

    return out


def _multi_param(string=str, sep=':'):
    """
    Split up data
    :param string:
    :return: list
    """
    arr = []
    result = []
    if sep in string:
        if sep == ':':
            arr = string.split(sep, 1)
        else:
            arr = string.split(sep)

    for val in arr:
        result.append(val.strip())
    return result


