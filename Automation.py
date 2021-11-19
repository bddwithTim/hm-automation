import pytest
import logging
import time

import src.lib.base as base
import src.lib.log as logger
from src.lib.actions import Actions
from src.lib.report import Report
from src.lib.fmanager import FileFolderManager

g = Report()
f = FileFolderManager()


@pytest.mark.nonbdd
@pytest.mark.usefixtures('drivers', 'data')
class TestClass(object):

    # @classmethod
    # def setup_class(cls):
    #     g.setup_report()

    def test(self, driver, data):
        logger.setup_logger(data['TestName'], '%s.log' % data['TestName'])
        log = logging.getLogger(data['TestName'])
        log.info('test case logging')

        actions = Actions(data['TestName'], driver)
        execution = base.config['execution']

        for i, _test in enumerate(data['steps']):
            step = i + 1
            act = _test[0].lower()
            if '#' in act:
                continue
            _data = str(_test[1]).replace('"', '')
            spec = _test[2]
            mob = ''
            try:
                mob = _test[3]
            except IndexError:
                pass

            if act:
                actions.plan = None
                browser = str(data['browser']).lower()
                on_mobile = ('ios' in browser) or ('mobile' in browser) or ('android' in browser)
                flag = True
                if on_mobile and mob == 'm-':
                    flag = False
                    log.info('Step %i is SKIPPED in Mobile setup', step)
                elif not on_mobile and mob == 'm':
                    flag = False
                    log.info('Step %i will be SKIPPED since not in Mobile setup', step)

                if flag:
                    if f.screenshoton and execution == 'local':
                        do_act = getattr(actions, 'capture')
                        do_act(str(step) + '_' + act, _data, spec)
                    do_act = getattr(actions, act)
                    do_act(step, _data, spec)
                    time.sleep(1)

            if 'signature' in driver.current_url.lower() and 'prod' in base.config['environment']:
                log.info("Stopped at the ESign page.")
                break

            if base.config['debug_stop'] == step:
                pass

    # @classmethod
    # def teardown_class(cls):
    #     g.teardown_report()
