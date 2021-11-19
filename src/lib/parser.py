# /automation/lib/
import os
import re
import csv
import configparser
import json
import traceback

import pandas as pd
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from tinydb.operations import add, set, increment

from src.lib.fmanager import FileFolderManager
from src.lib.procreate import Procreate
import src.lib.base as base

f = FileFolderManager()
procreate = Procreate()


def _iter_browser(browsers):
    for browser in browsers:
        yield browser


def format_test_name(test, browser):
    try:
        platform = browser['deviceName']
    except KeyError:
        platform = browser['platform']

    browser_name = browser['browserName']
    platform = platform.replace('.', '_').replace(' ', '_')
    browser_name = browser_name.replace('.', '_').replace(' ', '_')
    name = test.replace('.', '_').replace(' ', '_')
    test_name = "%s-%s-%s" % (name, browser_name, platform)

    return str(test_name)


def proliferate(browsers, test_data, collect_only=False):
    data = []
    db = None
    if not collect_only:
        db = TinyDB(f.report_path(file_name="reports.json"), storage=CachingMiddleware(JSONStorage))

    for browser in _iter_browser(browsers):
        for suite, tests in list(test_data.items()):
            if len(tests) <= 0:
                continue
            # base.report.setdefault(suite, {})
            # base.report[suite].setdefault("duration", 0)
            # base.report[suite].setdefault("passed", 0)
            # base.report[suite].setdefault("failed", 0)
            if db is not None:
                t_suites = db.table('_suites')
                q_suites = Query()
                t_suites.upsert({
                    "suite": suite,
                    "duration": 0,
                    "passed": 0,
                    "failed": 0
                }, q_suites.suite == suite)

            for test in tests:
                tc = (test[0][1]).replace(' ', '_')
                name = format_test_name(tc, browser)
                tags = ""

                if (test[2][0]).lower() == "tags" or (test[2][0]).lower() == "type":
                    tags = test[2][1]

                data.append({
                    "browser": browser,
                    "SuiteName": suite,
                    "TestCase": tc,
                    "TestName": name,
                    "Tags": tags,
                    "steps": test})

                if db is not None:
                    t_cases = db.table('_cases')
                    q_cases = Query()
                    t_cases.upsert({
                        "suite": suite,
                        "case": tc
                    }, (q_cases.suite == suite) & (q_cases.case == tc))

                    # t_runs = db.table("_tests")
                    # t_runs.upsert({
                    #     "case": tc,
                    #     "name": name,
                    #     "passed": None,
                    #     "duration": 0,
                    #     "browser": browser
                    # }, Query().name == name)

                    # base.report[suite]['tester'] = base.config['username']
                    # base.report[suite].setdefault("tests", {})
                    # base.report[suite]["tests"].setdefault(tc, {})

                    # base.report[suite]["tests"][tc]["desc"] = ""
                    # if (test[1][0]).lower() == "description":
                    #     base.report[suite]["tests"][tc]["desc"] = test[1][1]

                    # base.report[suite]["tests"][tc]["tags"] = tags
                    # base.report[suite]["tests"][tc].setdefault("cases", {})
                    # base.report[suite]["tests"][tc]["cases"].setdefault(name, {})
                    # base.report[suite]["tests"][tc]["cases"][name]["duration"] = 0
                    # base.report[suite]["tests"][tc]["cases"][name]["passed"] = None
                    # base.report[suite]["tests"][tc]["cases"][name]["config"] = browser
                    # base.report[suite]["tests"][tc]["steps"] = test
    if db is not None:
        db.close()
    return data


class Parser:

    def __init__(self, path=None):
        self.path = 'data'
        if path is not None:
            self.path = path

    def readconfig(self):
        """"This method searches the run.ini file in test suites directory and gets the testcases that will be ran."""
        ts_folder = self.path
        inifile = "run.ini"
        rtc = "run_testcases"
        tc = "testcases"
        rtc_all = False
        tc_is = ""
        tests_dir = {}
        tests = {}

        cwd = os.path.abspath(".")
        config = configparser.ConfigParser()
        path_ = os.path.join(cwd, ts_folder)
        if f.pathexists(path_):
            for root, dirs, files in os.walk(path_):
                break
            for dir in dirs:
                if " " in dir:
                    key_ts = str(dir)
                    key_ts = key_ts.replace(" ", "_")
                else:
                    key_ts = str(dir)
                path = os.path.join(path_, dir)
                file_ = os.path.join(path, inifile)
                if inifile in os.listdir(path):
                    if os.path.getsize(file_) > 0:
                        config.read(file_)
                        sections = config.sections()
                        for section in sections:
                            # Gets the run_testcases section, its option and its value
                            if rtc == section:
                                for option in config.options(section):
                                    if option == rtc:
                                        value = config.get(section, option).lower()
                                        if value == "all":
                                            tc_is = "all"
                                            rtc_all = True
                                            tests_dir[key_ts] = path
                                            break
                                        else:
                                            tc_is = "nall"
                                    else:
                                        tc_is = "nall"
                            # Gets the testcases section, its option and its value
                            elif tc == section and tc_is == "nall":
                                for option in config.options(section):
                                    if option == tc:
                                        value = config.get(section, option)
                                        values = re.split(',', value)
                                        tc_list = []
                                        for val in values:
                                            val = val.strip()
                                            val = val + ".csv"
                                            if f.pathexists(path, val):
                                                v = os.path.join(path, val)
                                                tc_list.append(v)
                                        tests[key_ts] = tc_list
                                        # Gets all the testcases if testcases option is empty or no testcases listed
                                        if len(tc_list) == 0:
                                            rtc_all = True
                                            tests_dir[key_ts] = path
                                        break
                                    else:
                                        print("no option for testcases = %s... run everything = %s" % (option, path))
                                        rtc_all = True
                                        tests_dir[key_ts] = path
                    else:
                        print("empty ini file in this path = %s... run everything" % path)
                        rtc_all = True
                        tests_dir[key_ts] = path
                else:
                    print("no ini file found in this path = %s... run everything" % path)
                    rtc_all = True
                    tests_dir[key_ts] = path
            if rtc_all:
                for tc in tests_dir:
                    p = tests_dir.get(tc)
                    tcs = []
                    for t in os.listdir(p):
                        t = str(t)
                        if t.endswith(".csv"):
                            tcs.append(os.path.join(p, t))
                    tests[tc] = tcs
            for test in tests:
                print(str(test) + " " + str(tests.get(test)))
        else:
            print("data folder does not exist")
            print(cwd)
            print(path_)
        return tests

    def get_datadict(self):
        """This method calls the readcsv or readxsl method."""
        if f.xslFile and f.convert is not None:
            xsldata = f.readxsl()
            if f.convert == 'tp':
                data = procreate.tp(xsldata, f.xslFile)
            elif f.convert == 'pa':
                data = procreate.prod_availability(xsldata, f.xslFile)
        else:
            tests = self.readconfig()
            data = f.readcsv(tests)
        # print(data)
        # exit()
        return data

    def json_(self, file_, folder=None, param=False):
        """
        Get JSON Data directly
        :param file_:
        :param folder:
        :param param:
        :return parsed json:
        """
        file_path = f.check_file_path(file_, folder)
        with open(file_path, 'r') as fp:
            obj = json.load(fp)
        if param:
            values = []
            for objct in obj:
                if len(objct) > 1:
                    values.append(tuple(objct.values()))
                else:
                    for key, value in objct.items():
                        values.append(value)
            return values
        else:
            return obj

    def csv_(self, file_, folder=None, param=False):
        """
        Get CSV data
        :param file_:
        :param folder:
        :param param:
        :return parsed csv:
        """
        file_path = f.check_file_path(file_, folder)
        with open(file_path, 'r') as csvFile:
            next(csvFile)
            contents = csv.reader(csvFile)
            values = []
            if param:
                for row in contents:
                    row = [item.strip() for item in row]
                    row = [item.replace("/", "-") for item in row]
                    row = [item.replace("\t", "") for item in row]
                    row = [item.replace(":", "") for item in row]
                    values.append(tuple(row))
            else:
                for row in contents:
                    values.append(tuple(row))
            return values


    def xls_(self, file_, folder=None, param=False):
        """
        Get excel data
        :param file_:
        :param folder:
        :param param:
        :return parsed excel:
        """
        fp = f.check_file_path(file_, folder)

        xl = pd.read_excel(fp)
        df = pd.DataFrame(xl)

        if param:
            values = []
            for row in df.iterrows():
                row = list(row)
                row[1] = [str(item).strip() for item in row[1]]
                row[1] = [str(item).replace("/", "-") for item in row[1]]
                row[1] = [str(item).replace("\t", "") for item in row[1]]
                row[1] = [str(item).replace(":", "") for item in row[1]]
                items = []
                for n in row[1]:
                    items.append(n)
                values.append(tuple(items))
            return values
        else:
            return df

    def for_testname_ids(self, file_, folder=None, data_format="xls"):
        """
        Assign test name ids
        :param file_:
        :param folder:
        :param data_format: excel, json, or csv
        :return parsed excel:
        """
        if data_format == "xls":
            values = self.xls_(file_, folder, True)
        elif data_format == "json":
            values = self.json_(file_, folder, True)
        elif data_format == "csv":
            values = self.csv_(file_, folder, True)
        else:
            exit("Invalid data format provided! It should be either xls, json, or csv")
        ids = []
        for index, value in enumerate(values):
            value = "".join(value)
            if len(value) > 200:
                value = value[0:50] + "..."
            data_ = str("{:03d}".format(index + 1)) + "-" + value
            ids.append(data_)
        return ids





# if __name__ ==
#     #print "main"'__main__':
#     obj = Parser()
#     obj.get_datadict()
