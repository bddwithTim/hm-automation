# -*- coding: utf-8 -*-

import os
import re
import time
import platform

import src.lib.base as base
from src.lib.generateXml import TestDict
from src.lib.generateHtml import HTMLClass
from src.lib.fmanager import FileFolderManager

f = FileFolderManager()
xml = TestDict()
html = HTMLClass()


class Report(object):

    @staticmethod
    def capture_screen(driver, location=None, filename=None):
        if not location:
            location = os.path.join(f.workingdir, f.screenshotfolder)
        if not filename:
            filename = "default_error.png"
        driver.save_screenshot(os.path.join(location, filename))

    # def gen_htmlreport(self, base, etime):
    def gen_htmlreport(self):
        """This method generates an html report based from the xml files generated."""
        html.create_html(f.cwd, f.workingdir, f.reportfolder)

    def setup_report(self):
        # Clears or creates report folder if it doesn't exist
        if f.pathexists(f.workingdir, f.reportfolder):
            f.clrfiles(os.path.join(f.workingdir, f.reportfolder))
        else:
            f.mkdir(f.workingdir, f.reportfolder)
        # Creates or clears logs folder if it doesn't exist
        if not f.pathexists(f.workingdir, f.logfolder):
            f.mkdir(f.workingdir, f.logfolder)
        else:
            f.clrfiles(os.path.join(f.workingdir, f.logfolder))
        # Creates or clears screenshot folder if it doesn't exist
        if not f.pathexists(f.workingdir, f.screenshotfolder):
            f.mkdir(f.workingdir, f.screenshotfolder)
        else:
            f.clrfiles(os.path.join(f.workingdir, f.screenshotfolder))
        self.stime = time.time()
