import os
import errno
import time
import requests
import aiohttp
import asyncio
import async_timeout
import json
import glob
from datetime import datetime
from tinydb import TinyDB, Query
from sauceclient import SauceClient
from multiprocessing.pool import ThreadPool

import src.lib.base as base
import src.lib.config as config
import src.lib.log as logger
from src.lib.fmanager import FileFolderManager

browsers = [
    {
        'platform': 'Windows 10',
        'browserName': 'chrome',
        'version': 'latest'
    }
]


def remote_setup(path):
    """
    Load browser list from specific JSON file
    :param path: Path to JSON file
    :return: Browser list/dict
    """
    cfg_file = 'browsers.json'
    if path is not None:
        path += '\%s' % cfg_file
    else:
        path = '.\%s' % cfg_file

    g = glob.glob(path)
    if len(g) >= 1:
        filename = g[len(g) - 1]
        with open(filename, 'r') as data_file:
            load = json.load(data_file)
    else:
        load = browsers

    return load


class SauceHelper(SauceClient):
    def __init__(self, user, key):
        SauceClient.__init__(self, user, key)
        self.meta = {}
        self._temp_meta = {}
        self.base_flag = False
        self.__test_name = None

    @staticmethod
    def __path_gen(name, folder, file=None):
        p = "%s\\imgdiff\\%s\\%s" % (os.getcwd(), name, folder)
        if file:
            p = "%s\\%s" % (p, file)

        return p

    def _create_dir(self, name):
        if name:
            baseline_dir = self.__path_gen(name, "baseline")
            current_dir = self.__path_gen(name, "current")
            try:
                os.makedirs(baseline_dir)
                os.makedirs(current_dir)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

    def get_report_nodes(self, report):
        if report is not None:
            with TinyDB(report) as db:
                tests = db.table("_tests").search(Query().node_id)
            if len(tests) > 0:
                for test in tests:
                    node = test['node_id']
                    if node and test['passed']:
                        self.meta.setdefault(node, {
                            "name": test['name'],
                            "screenshots": []
                        })
                        self._create_dir(test['name'])

    def get_screenshot_list(self, node):
        r = None
        status = None
        if node:
            print(node)
            # print(self.sauce_username)
            while status != "complete":
                r = self.jobs.get_job(node)
                status = r['status']
            r = self.jobs.get_job_assets(node)
            self.meta[node]['screenshots'].extend(r['screenshots'])

        return r

    def get_screenshot_items(self):
        for node in self.meta:
            self._temp_meta = self.meta[node]
            self._temp_meta['node'] = node
            urls = []
            for asset_id in self._temp_meta['screenshots']:
                urls.append(self.jobs.get_job_asset_url(node, asset_id))
            result_imgs = ThreadPool(10).imap_unordered(self._request_img, urls)
            for r in result_imgs:
                print(r)
            print("...")

    def _request_img(self, url):
        if url:
            file = url.split("/")[-1]
            folder = "current"
            if self.base_flag:
                folder = "baseline"
            path = self.__path_gen(self._temp_meta['name'], folder, file)
            r = requests.get(url, auth=(self.sauce_username, self.sauce_access_key), stream=True)
            if r.status_code == 200:
                with open(path, "wb") as f:
                    for chunk in r:
                        f.write(chunk)

            return "%s : %s" % (url, path)


class Server(object):
    def __init__(self):
        self.host = None
        self.header = {"Content-Type": "application/json"}
        self._report = {}
        self._tests = []
        self._test_runs = []
        self.default_config = {
            'browserName': None,
            'appiumVersion': None,
            'deviceName': None,
            'deviceOrientation': None,
            'platform': None,
            'platformVersion': None,
            'platformName': None,
            'version': None
        }

    @staticmethod
    def out():
        # print(str(base.report))
        f = open('C:\\blob.json', 'w+')
        f.write(str(base.report))
        f.close()

    def prep_report(self):
        pass

    def __send_suite_data(self, suite):
        req = requests.post("%s/api/Suites" % self.host,
                            json={
                                'SuiteName': suite
                            })

        if req.status_code == requests.codes.conflict:
            req = requests.patch("%s/api/Suites?suitename=%s" % (self.host, suite),
                                 json={
                                     'Date': datetime.now().isoformat()
                                 })

        print("send_suite_data(Suite) => %i" % req.status_code)

    def __send_suite_history(self, suite, duration):
        req = requests.post("%s/api/SuiteHistories" % self.host,
                            json={
                                'SuiteName': suite,
                                'Duration': int(float(duration)),
                                'Date': datetime.now().isoformat()
                            })
        print(req.status_code)
        return req.json()['ID']

    def __send_case_data(self, case, desc, tags):
        tag_array = tags.split("|")
        for tag in tag_array:
            tag = tag.strip()
            tag_req = requests.put("%s/api/Tags?key=%s" % (self.host, tag),
                                   json={
                                       'Key': tag
                                   })
        req = requests.post("%s/api/Cases" % self.host,
                            json={
                                'CaseName': case,
                                'Description': desc,
                                'Tags': tags
                            })

        if req.status_code == requests.codes.conflict:
            req = requests.patch("%s/api/Cases?name=%s" % (self.host, case),
                                 json={
                                     'Description': str(desc),
                                     'Tags': str(tags)
                                 })
        print("send_case_data(Case) => %i" % req.status_code)

    async def __send_test_data(self):
        async with aiohttp.ClientSession() as session:
            i = 0
            while len(self._tests) != i:
                print(json.dumps(self._tests[i]))
                async with session.post("%s/api/Tests" % self.host,
                                        headers=self.header,
                                        data=json.dumps(self._tests[i])) as req:
                    # req = await req.read()
                    print(req.status)
                i += 1

    async def __send_test_history(self):
        async with aiohttp.ClientSession() as session:
            i = 0
            while len(self._test_runs) != i:
                print(json.dumps(self._test_runs[i]))
                async with session.post("%s/api/TestHistories" % self.host,
                                        headers=self.header,
                                        data=json.dumps(self._test_runs[i])) as req:
                    # req = await req.read()
                    print(req.status)
                i += 1

    def send_report(self, path):
        try:
            with open(path) as p:
                self._report = json.load(p)
            # os.remove(path)cls

        except FileNotFoundError:
            raise FileNotFoundError

        self.host = 'http://%s/DSA' % base.config['server_address']

        # self._report = base.report
        if len(self._report) > 0:
            for suite in self._report:
                _suite = self._report[suite]
                self.__send_suite_data(suite)
                suite_id = self.__send_suite_history(suite, _suite['duration'])
                for case in _suite['tests']:
                    _case = _suite['tests'][case]
                    desc = _case['desc']
                    tags = _case['tags']
                    self.__send_case_data(case, desc, tags)
                    self._tests.append({
                        'SuiteName': suite,
                        'CaseName': case
                    })
                    for test in _case['cases']:
                        _test = _case['cases'][test]
                        duration = (_test['duration']).strip('s')
                        duration = int(float(duration))
                        status = "Passed" if _test['status'] == "1" else "Failed"
                        config = self.default_config.copy()
                        config.update(_test['config'])
                        config['SuiteHistoryID'] = suite_id
                        config['Suite'] = suite
                        config['Name'] = case
                        config['TestName'] = test
                        config['Status'] = status
                        config['Duration'] = duration
                        # config['Tester'] = base.config['username']
                        config['Tester'] = _suite['tester']
                        config['node'] = _test['node']
                        self._test_runs.append(config)
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.__send_test_data())
            loop.run_until_complete(self.__send_test_history())


# server = Server()

if __name__ == '__main__':
    # base.config['username'] = 'rcogonon'
    # base.report = 'C:\\Tests\\Smoke\\reports\\report.json'
    # server.send_report('C:\\Tests\\Smoke\\reports\\report.json')
    pass
