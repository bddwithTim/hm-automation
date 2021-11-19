# /Automation/lib
import os


class HTMLClass(object):

    def create_html(self, cwd, dir_, report_folder):
        """This method processes an xmlfile and convert it into an html file."""
        HTMLTemplateFile = "HTML.html.template"
        jsonfile = "reports.json"
        outputname = "reports.html"

        # Read HTML Template
        with open(os.path.join(cwd, HTMLTemplateFile), 'r') as f:
            HTMLData = f.read()

        # Read JSON File
        with open(os.path.join(os.path.join(dir_, report_folder), jsonfile), 'r') as f:
            jsondata = f.read()

        HTMLData = HTMLData.replace("@@data@@", jsondata)

        ofile = open(os.path.join(os.path.join(dir_, report_folder), outputname), 'w')
        ofile.write(HTMLData)
        ofile.close()

# if __name__ == "__main__":
#     print(os.getcwd())
#     dir_ = os.getcwd()
#     hreport = HTMLClass()
#     hreport.create_html(dir)
