import os
import re
import csv
import shutil
import datetime
import pandas as pd
import src.lib.base as base


class FileFolderManager(object):
    def __init__(self):
        self.cwd = self.currentdir()

    def currentdir(self):
        """This method gets current working directory."""
        return os.getcwd()

    def pathexists(self, dir, fname=''):
        """This method checks if path or folder exists and create if needed."""
        path = os.path.join(dir, fname)
        if os.path.exists(path):
            return True
        else:
            return False

    def mkdir(self, dir, fname=datetime.datetime.now().strftime("%Y-%m-%d_%H")):
        """This method creates new directory if folder doesn't exists."""
        if not self.pathexists(dir, fname):
            try:
                os.makedirs(os.path.join(dir, fname))
            except WindowsError as e:
                print('WindowsError = %s' % e)
                pass

    def backupfiles(self, dir_, fname, f_ext=[], nfname=datetime.datetime.now().strftime("%Y-%m-%d_%H")):
        """This method backups specific file type extensions.
        Default destination folder name is 'YYYY-MM-DD_HH' if destination folder name is not specified.
        """
        repo_dir = os.path.join(dir_, fname)
        bkp_path = os.path.join(repo_dir, nfname)
        if not os.path.exists(bkp_path):
            self.mkdir(bkp_path)
        filenames = os.listdir(repo_dir)
        for filename in filenames:
            if filename.endswith(tuple(f_ext)) and self.pathexists(repo_dir, filename):
                if os.path.isfile(os.path.join(repo_dir, filename)):
                    bkp_file = os.path.join(repo_dir, filename)
                    try:
                        if os.path.exists(os.path.join(bkp_path, filename)):
                            os.remove(os.path.join(bkp_path, filename))
                        shutil.copy2(bkp_file, bkp_path)
                    except OSError as e:
                        print(e)
                        continue
                    except IOError as e:
                        print(e)
                        continue

    def clrdir(self, dir, fname):
        """This method deletes directory and its specific contents."""
        if self.pathexists(dir, fname):
            shutil.rmtree(os.path.join(dir, fname), ignore_errors=True)

    def clrfiles(self, dir_):
        """This method clears specific files in a directory."""
        filenames = os.listdir(dir_)
        for filename in filenames:
            if os.path.isfile(os.path.join(dir_, filename)) and self.pathexists(dir_, filename):
                try:
                    os.remove(os.path.join(dir_, filename))
                except OSError as e:
                    print('WindowsError = %s' % e)
                    continue

    def readcsv(self, tests):
        """This method reads the contents of the csv files and save it in a datadict dictionary."""
        datadict = {}
        for test in tests:
            tsdict = []
            num = 1
            files_ = tests.get(test)
            for file in files_:
                list_ = []
                no_tc = True
                count = 1
                # checks if csv file is empty
                if os.path.getsize(file) > 0:
                    f = open(file, 'r')
                    n = int(sum(1 for r in csv.reader(f)))
                    f.close()
                    f = open(file, 'r')
                    try:
                        reader = csv.reader(f)
                        for row in reader:
                            row_len = len(row)
                            for x in range(0, row_len):
                                row[x] = row[x].strip()
                            if no_tc:
                                ro = str(row).lower()
                                if "testname" in ro:
                                    sp = re.split(',', ro)
                                    key = sp[1]
                                    if "'" in key:
                                        key = re.sub('[\']', '', key)
                                    key = key.strip()
                                    no_tc = False
                                if count == n:
                                    key = "testcase_noname_%s" % str(num)
                                    num = int(num)
                                    num += 1
                                count += 1
                            list_.append(row)
                        tsdict.append(list_)
                        # tsdict[key] = list_
                    finally:
                        f.close()
            datadict[test] = tsdict
        return datadict

    def readxsl(self):
        ts_dict = {}
        col_list = []
        xl = pd.read_excel(os.path.join(self.workingdir, self.xslFile))
        if self.convert == 'tp':
            df = pd.DataFrame(xl)
            for col in xl.columns:
                col_list.append(str(col).lower())
            # print len(xl.columns)
            for row in df.iterrows():
                print('index = ' + str(row[0]))
                count = 0
                tc_dict = {}
                for n in row[1]:
                    tc_dict[col_list[count]] = str(n).strip()  #.lower()
                    count += 1
                ts_dict[row[0] + 1] = tc_dict
        elif self.convert == 'pa':
            xl.columns = xl.iloc[1]
            xl = xl[2:]
            df = pd.DataFrame(xl)
            for col in xl.columns:
                col_list.append(str(col).lower())
            # print(col_list)
            num_states = 51
            state = 0
            for row in df.iterrows():
                count = 0
                tc_dict = {}
                if state == num_states:
                    break
                # print('index = ' + str(row[0]))
                for n in row[1]:
                    tc_dict[col_list[count]] = str(n).strip()  # .lower()
                    count += 1
                ts_dict[row[0] + 1] = tc_dict
                state += 1
            # for d in ts_dict:
            #     print(ts_dict[d])
        else:
            exit('unknown convert code!')
        return ts_dict

    def clear_options(self, args):
        if args.clearall:
            if self.pathexists(self.workingdir, self.logfolder):
                self.clrdir(self.workingdir, self.logfolder)
            if self.pathexists(self.workingdir, self.reportfolder):
                self.clrdir(self.workingdir, self.reportfolder)
            if self.pathexists(self.workingdir, self.screenshotfolder):
                self.clrdir(self.workingdir, self.screenshotfolder)
        else:
            if args.clearlogs and self.pathexists(self.workingdir, self.logfolder):
                self.clrdir(self.workingdir, self.logfolder)
            if args.clearreports and self.pathexists(self.workingdir, self.reportfolder):
                self.clrdir(self.workingdir, self.reportfolder)
            if args.clearscreenshots and self.pathexists(self.workingdir, self.screenshotfolder):
                self.clrdir(self.workingdir, self.screenshotfolder)

    def check_file_path(self, file_, folder, concat_fldr=None):
        """
        Check the file path
        :param file_:
        :param folder:
        :return exact file path:
        """
        if not concat_fldr:
            concat_fldr = "data\\functional"
            print(concat_fldr)
        cwd = os.path.abspath(".")
        path_ = os.path.join(cwd, concat_fldr)
        if os.path.isfile(file_) and not folder:
            return file_
        elif folder:
            path_ = os.path.join(path_, folder)
            file_ = os.path.join(path_, file_)
            if os.path.isfile(file_):
                return file_
            else:
                exit("%s doesn't exists" % file_)
        else:
            if self.pathexists(path_):
                for root, dirs, files in os.walk(path_):
                    break
                for dir_ in dirs:
                    path = os.path.join(path_, dir_)
                    file = os.path.join(path, file_)
                    if file_ in os.listdir(path):
                        if os.path.getsize(file) > 0:
                            return file
                        else:
                            exit("%s contains nothing" % file)
            else:
                exit("%s doesn't exists" % path_)

    @property
    def workingdir(self):
        """Getter: I'm the 'workingdir' property."""
        return base.dirs['wkd']

    @workingdir.setter
    def workingdir(self, custom_path):
        """Setter: I'm the 'workingdir' setter."""
        if custom_path:
            # base.dirs['wkd'] = custom_path
            if os.path.exists(custom_path):
                if os.path.isfile(custom_path) and str(custom_path).endswith(('.xls', '.xlsx')):
                    dir_, file_ = os.path.split(custom_path)
                    print(file_ + ' is a file!')
                    print(dir_)
                    custom_path = dir_
                    self.xslFile = file_
                elif os.path.isdir(custom_path):
                    print(custom_path + ' is a directory!')
                else:
                    print('file is not an EXCEL!')
                    quit()
                base.dirs['wkd'] = custom_path
            else:
                print("file / path doesn't exists!")
                quit()
        else:
            base.dirs['wkd'] = self.currentdir() # OR base.dirs['wkd'] = base.dirs['cwd']

    @property
    def reportfolder(self):
        """Getter: I'm the 'reportfolder' property."""
        return base.config['reportfolder']

    @property
    def logfolder(self):
        """Getter: I'm the 'logfolder' property."""
        return base.config['logfolder']

    @property
    def screenshotfolder(self):
        """Getter: I'm the 'screenshotfolder' property."""
        return base.config['screenshotfolder']

    @property
    def screenshoton(self):
        """Getter: screenshoton property."""
        return base.config['screenshot']

    @screenshoton.setter
    def screenshoton(self, sshot):
        """Setter: I'm the 'screenshoton' setter."""
        base.config['screenshot'] = sshot

    @property
    def env(self):
        """Getter: I'm the 'env' property."""
        return base.config['environment']

    @env.setter
    def env(self, env):
        """Setter: I'm the 'env' setter."""
        if not env:
            if not base.config['environment']:
                base.config['environment'] = None
            else:
                base.config['environment'] = str(base.config['environment']).lower().strip()
        else:
            if str(env).lower().strip() == 'test':
                base.config['environment'] = 'test'
            elif str(env).lower().strip() == 'dev':
                base.config['environment'] = 'dev'
            elif str(env).lower().strip() == 'model':
                base.config['environment'] = 'model'
            elif str(env).lower().strip() == 'stage':
                base.config['environment'] = 'stage'
            elif str(env).lower().strip() == 'production':
                base.config['environment'] = 'production'
            elif str(env).lower().strip() == 'prod':
                base.config['environment'] = 'prod'
            else:
                exit("Invalid value set for env argument!")

    @property
    def xslFile(self):
        return base.config['xsl']

    @xslFile.setter
    def xslFile(self, xsl):
        base.config['xsl'] = xsl

    @property
    def reportname(self):
        """Getter: I'm the 'reportname' property."""
        return base.config['reportname']

    @reportname.setter
    def reportname(self, outputname):
        """Setter: I'm the 'reportname' setter."""
        if outputname:
            base.config['reportname'] = str(outputname) + '.html'

    @property
    def convert(self):
        return base.config['convert']

    @convert.setter
    def convert(self, what):
        base.config['convert'] = what

    def report_path(self, workingdir=None, reportfolder=None, file_name=str):
        if not workingdir:
            workingdir = self.workingdir
        if not reportfolder:
            reportfolder = self.reportfolder
        report_path = None
        if workingdir is not None and reportfolder is not None:
            try:
                report_path = os.path.join(workingdir, reportfolder, file_name)
            except Exception as e:
                print(e)

        return report_path

    @property
    def sso(self):
        """Getter: I'm the 'sso' property."""
        return base.config['sso']

    @sso.setter
    def sso(self, sso):
        """Setter: I'm the 'sso' setter."""
        if sso:
            base.config['sso'] = True
        else:
            base.config['sso'] = False
