import src.lib.base as base
from datetime import datetime
from src.lib.prep import Prep as prep
from src.lib.fmanager import FileFolderManager
from src.templates._dtc import _DTC
from src.templates._baa import _BAA
from src.templates._osign import _OSign
from src.templates._shopping_cart_quote import _ShoppingCartQuote
from src.templates._customized_quote import _CustomizedQuote
from src.templates._product_availability import _ProductAvailability
f = FileFolderManager()
_d = _DTC()
_baa = _BAA()
_osign = _OSign()
_cq = _CustomizedQuote()
_scq = _ShoppingCartQuote()
_prod_avail = _ProductAvailability()


class Procreate(prep):
    def __init__(self):
        prep.__init__(self)

    def prod_availability(self, xsldata, tsname):
        """This method reads the contents of the xsl file and save it in a datadict dictionary."""
        tsname = self.testsuitename(tsname)
        datadict = dict()
        tclist = []
        for key in xsldata:
            data = xsldata[key]
            keys = list(data.keys())
            keys.sort()
            planlist = []
            broke = False
            for ke in keys:
                # if 'nan' == ke:
                #     if 'x' == data[ke]:
                #         broke = True
                #         break
                if 'st' == ke:
                    st = str(data[ke]).strip()
                    if st in ['MA', 'ND', 'NH', 'NJ', 'NY', 'SC', 'VT', 'WA']:
                        broke = True
                        break
                    base.pa_data['state'] = st
                elif 'information' in ke:
                    zipcode = str(data[ke]).strip()
                    while len(zipcode) < 5:
                        zipcode = '0' + zipcode
                    base.pa_data['zipcode'] = zipcode
                # elif 'aca off exch' in ke:
                #     if 'nan' not in ke:
                #         planlist.append(ke)
                elif 'short term' == ke:
                    if 'nan' not in str(data[ke]).strip():
                        planlist.append(ke)
                elif 'dental' == ke:
                    if 'nan' not in str(data[ke]).strip():
                        planlist.append(ke)
                elif 'dental 50+' in ke:
                    if 'nan' not in str(data[ke]).strip():
                        planlist.append(ke)
                elif 'critical' in ke:
                    if 'nan' not in str(data[ke]).strip():
                        planlist.append(ke)
                elif 'accident' == ke:
                    if 'nan' not in str(data[ke]).strip():
                        planlist.append(ke)
                elif 'accident premier' == ke:
                    if 'nan' not in str(data[ke]).strip():
                        planlist.append(ke)
                elif 'accident pro' == ke:
                    if 'nan' not in str(data[ke]).strip():
                        planlist.append(ke)
                elif 'term life' == ke:
                    if 'nan' not in str(data[ke]).strip():
                        planlist.append(ke)
                elif 'discount card' == ke:
                    if 'nan' not in str(data[ke]).strip():
                        planlist.append(ke)
                elif 'supp indemnity' == ke:
                    if 'nan' not in str(data[ke]).strip():
                        planlist.append(ke)
                elif 'fixed indemnity' == ke:
                    if 'nan' not in str(data[ke]).strip():
                        planlist.append(ke)
                elif 'core access' == ke:
                    if 'nan' not in str(data[ke]).strip():
                        planlist.append(ke)
                elif 'vision' == ke:
                    if 'nan' not in str(data[ke]).strip():
                        planlist.append(ke)
            if not broke:
                base.pa_data['tsname'] = tsname
                base.pa_data['tcname'] = str(key + 2) + '_' + st + ' state'
                base.pa_data['desc'] = 'Tests ' + tsname + ' for ' + st + ' state'
                base.pa_data['uri'] = 'https://model.uhone.com/Quote/QuoteCensus'
                base.pa_data['type'] = f.convert
                base.pa_data['planlist'] = planlist
                tclist.append(_prod_avail.to_pa())
        datadict[tsname] = tclist
        return datadict

    def tp(self, xsldata, tsname):
        """This method reads the contents of the xsl file and save it in a datadict dictionary."""
        tsname = self.testsuitename(tsname)
        datadict = dict()
        tclist = []
        for key in xsldata:
            plancount = 1
            depcount = 1
            dobcount = 1
            tobaccocount = 1
            applicantsnum = 1
            data = xsldata[key]
            keys = list(data.keys())
            keys.sort()
            ref = dict()
            plans = list()
            plandict = dict()
            plandicts = dict()
            self.line = list()
            self.applicantheightft = ['5', '5']
            self.applicantheightin = ['8', '7']
            self.applicantweightlbs = ['170', '160']
            tcname = '%s_%s_%s_%s' % (data[self.testcasenumber],
                                      str(data[self.plansintestcase]).replace('\n', '').replace(' ', '_'),
                                      data[self.state], data[self.testcasetype].replace(' ', '_'))
            desc = 'This tests the %s in %s state.' % (str(data[self.plansintestcase]).replace('\n', '').replace(' ', '_'),
                                                       data[self.state])
            typ = str(data[self.testcasetype]).lower()
            brokerid = str(data[self.brokerid]).strip()
            brokerpwd = str(data[self.brokerpwd]).strip()
            applicants = [data[self.primarygender], data[self.spousegender]]
            primarydob = self.convert_date(data[self.primarydob])
            spousedob = str(data[self.spousedob]).lower()
            if spousedob not in ['nan', 'nat']:
                spousedob = self.convert_date(spousedob)
                applicantsnum += 1
            applicantsdob = [primarydob, spousedob]
            applicantstobacco = [data[self.primarytobacco], data[self.spousetobacco]]
            for ke in keys:
                if self.state in ke:
                    st = str(data[ke]).strip()
                elif self.zipcounty in ke:
                    zipcounty = str(data[ke]).split()
                    zipcode = str(zipcounty[1])
                    while len(zipcode) < 5:
                        zipcode = '0' + zipcode
                    county = str(zipcounty[2]).upper()
                    if len(zipcounty) == 4:
                        county = str(county + ' ' + str(zipcounty[3])).upper().replace('(', '').replace(')', '')
                    elif len(zipcounty) == 5:
                        county = str(county + ' ' + zipcounty[3] + ' ' + str(zipcounty[4])).upper().replace('(',
                                                                                                            '').replace(
                            ')', '')
                elif str(depcount) + self.dependentgender in ke:
                    applicants.append(data[ke])
                    depcount += 1
                elif str(dobcount) + self.dependentdob in ke:
                    dob = str(data[ke]).lower()
                    if dob not in ['nan', 'nat']:
                        dob = self.convert_date(dob, 'update_ht_wt')
                        applicantsnum += 1
                    applicantsdob.append(dob)
                    dobcount += 1
                elif str(tobaccocount) + self.dependenttobacco in ke:
                    applicantstobacco.append(data[ke])
                    tobaccocount += 1
                elif self.plan + str(plancount) == ke:
                    if data[ke] not in ['nan', None, ' ']:
                        plans.append(data[ke])
                        for k in keys:
                            if str(plancount) + self.plancoveragestartdate in k:
                                plandict[k] = data[k]
                            elif str(plancount) + self.plancoverageenddate in k:
                                plandict[k] = data[k]
                            elif str(plancount) + self.planmaxduration in k:
                                plandict[k] = data[k]
                            elif str(plancount) + self.plandeductiblecoinsurance in k:
                                plandict[k] = data[k]
                            elif str(plancount) + self.plandeductibletype in k:
                                plandict[k] = data[k]
                            elif str(plancount) + self.planotheroptions in k:
                                plandict[k] = data[k]
                            elif str(plancount) + self.planappquestions in k:
                                plandict[k] = data[k]
                            elif str(plancount) + self.planpaymenttype in k:
                                plandict[k] = data[k]
                            elif str(plancount) + self.plannotes in k:
                                plandict[k] = data[k]
                            elif str(plancount) + self.planappnumber in k:
                                plandict[k] = data[k]
                            elif str(plancount) + self.planbrochurenumber in k:
                                plandict[k] = data[k]
                        plancount += 1
                        plandicts[data[ke]] = plandict
            applicantsage = self.get_age(applicantsdob)
            """storing test suite data to base library"""
            base.ts_data['data'] = data
            base.ts_data['tsname'] = tsname
            base.ts_data['tcname'] = tcname
            base.ts_data['desc'] = desc
            base.ts_data['zipcode'] = zipcode
            base.ts_data['county'] = county
            base.ts_data['state'] = st
            base.ts_data['applicants'] = applicants
            base.ts_data['applicantsnum'] = applicantsnum
            base.ts_data['applicantsdob'] = applicantsdob
            base.ts_data['applicantsage'] = applicantsage
            base.ts_data['applicantstobacco'] = applicantstobacco
            base.ts_data['plans'] = plans
            base.ts_data['plandict'] = plandicts
            base.ts_data['type'] = typ
            base.ts_data['applicantheightft'] = self.applicantheightft
            base.ts_data['applicantheightin'] = self.applicantheightin
            base.ts_data['applicantweightlbs'] = self.applicantweightlbs
            base.ts_data['primaryfname'] = st + ' ' + county
            base.ts_data['primarylname'] = typ
            base.ts_data['brokerid'] = brokerid
            base.ts_data['brokerpwd'] = brokerpwd
            if typ == 'dtc':
                # continue
                base.ts_data['uri'] = 'https://model.uhone.com/shop/#/census'
                tclist.append(_d.to_dtc())
            elif typ == 'customized quote':
                continue
                base.ts_data['uri'] = 'https://model.uhone.com/broker'
                tclist.append(_cq.to_cq())
            elif typ == 'baa':
                continue
                base.ts_data['uri'] = 'https://model.uhone.com/broker'
                tclist.append(_baa.to_baa())
            elif typ == 'osign':
                continue
                base.ts_data['uri'] = 'https://model.uhone.com/Broker/PostLogin/BrokerHelpLogin.aspx?SingleSignOnGuid=0107adb4-3022-4e04-89f7-d7dfade719a1'
                tclist.append(_osign.to_osign())
            elif typ == 'shopping cart quote':
                continue
                base.ts_data['uri'] = 'https://model.uhone.com/broker'
                tclist.append(_scq.to_scq())
        datadict[tsname] = tclist
        return datadict

    def uho_expand_coverage_dialog(self, file_):
        self.file_ = file_
        self.act(self.file_, self.verify, 'Displayed: Successfully Added to Cart!', '<expand_coverage_dlg>', 'm-', 0)
        self.act(self.file_, self.click, 'Go to Cart', '<go_to_cart_bttn>', 'm-')

    def uho_consecutive_stm_dialog(self, file_, consecutive_plan=False):
        self.file_ = file_
        self.act(self.file_, self.verify, 'Displayed: Consecutive Short Term Dialog', 'h3.modal-title', 'm-', 0)
        if consecutive_plan:
            # self.act(self.file_, self.click, 'Yes', '#consecutiveCoverageResponse[data-gtm-id*=Yes]', 'm-')
            self.act(self.file_, self.click, 'Continue', '.modal-dialog button[type=submit]', 'm-')
        else:
            self.act(self.file_, self.click, 'No', '#consecutiveCoverageResponse[data-gtm-id*=No]', 'm-')
            self.act(self.file_, self.click, 'Continue', '.modal-dialog button[type=submit]', 'm-')

    def uho_registration_dialog(self, file_):
        self.file_ = file_
        self.act(self.file_, self.verify, 'Displayed: Registration dialog', '<uho_before_you_continue_dlg_ar>', '', 0)
        self.act(self.file_, self.click, 'Continue Without Registering', '<uho_continue_without_registering_bttn_ar>')

    def act(self, file_, act, data=None, exp_element='', m='', wait=1):
        self.file_ = file_
        if act in [self.testname, self.description, self.type, self.url]:
            self.actline = [act, data, exp_element, m]
        else:
            self.actline = [act, data, exp_element, m]
            if wait:
                self.actline = [self.wait, 'Uho Loading...', self.elmnt_uho_loading_img, m]

    def convert_date(self, date, var=None):
        date = str(date).split()
        date = date[0].split('-')
        current_year = datetime.now().year
        current_month = datetime.now().month
        current_day = datetime.now().day
        if var == 'update_ht_wt':
            age = current_year - int(date[0])
            if age > 17:
                self.applicantheightft.append('5')
                self.applicantheightin.append('6')
                self.applicantweightlbs.append('150')
            elif 12 < age < 18:
                self.applicantheightft.append('5')
                self.applicantheightin.append('3')
                self.applicantweightlbs.append('115')
            elif 6 < age < 13:
                self.applicantheightft.append('4')
                self.applicantheightin.append('4')
                self.applicantweightlbs.append('65')
            else:
                self.applicantheightft.append('3')
                self.applicantheightin.append('0')
                self.applicantweightlbs.append('35')
                if age == 0:
                    date[0] = str(current_year - 1)
        elif var == 'coverage_date':
            if int(date[0]) <= current_year:
                date[0] = str(current_year)
                if int(date[1]) < current_month:
                    date[1] = self.check_index(str(current_month))
                    if int(date[2]) < current_day:
                        date[2] = self.check_index(str(current_day))
        date = date[1] + '/' + date[2] + '/' + date[0]
        return date

    def get_age(self, dobs):
        age_list = list()
        for dob in dobs:
            if dob in ['nan', 'nat']:
                age_list.append(dob)
                continue
            date = str(dob).split('/')
            current_year = datetime.now().year
            current_month = datetime.now().month
            current_day = datetime.now().day
            age = current_year - int(date[2])
            if age == 65:
                if int(date[0]) == current_month:
                    if int(date[1]) > current_day:
                        age -= 1
                elif int(date[0]) > current_month:
                    age -= 1
            age_list.append(age)
        return age_list

    def trim_line(self, line, sep=', '):
        line = str(line)[1:-1]
        line = line.split(sep)
        lyn = list()
        for i, l in enumerate(line):
            l = str(l)[1:-1]
            lyn.append(l)
        line = lyn[0] + sep + lyn[1] + sep + lyn[2] + sep + lyn[3]
        return line

    def check_index(self, num, exp=2):
        num_len = len(num)
        if num_len < exp:
            num = '0' + str(num)
        return str(num)

    def get_attrib_from_notes(self, plans, plandict, get='?'):
        attrib = list()
        notes = list()
        primary = 1
        spouse = 1
        dependent = 1
        ssn = 'ssn'
        ssn_req = 'ssn required:'
        ssn_not = 'but not required'
        fact = 'fact'
        for i, plan in enumerate(plans):
            if plan in ['nan', ' ', None]:
                continue
            notes.append(plandict[plan][self.plan + str(i + 1) + self.plannotes])
        for note in notes:
            if get == ssn:
                if ssn_req in str(note).lower() and ssn_not not in str(note).lower():
                    note = str(note).strip().split('\n')
                    for nt in note:
                        if get in str(nt).lower():
                            nt = str(nt).lower().replace(ssn_req, '').strip()
                            if 'primary' in nt and primary:
                                attrib.append(0)
                                primary = 0
                            if 'spouse' in nt and spouse:
                                attrib.append(1)
                                spouse = 0
                            if 'dependent' in nt and dependent:
                                attrib.append(2)
                                attrib.append(3)
                                dependent = 0
            elif get == fact:
                if fact in str(note).lower():
                    attrib.append(1)
        return attrib

    def testsuitename(self, tsname):
        """Sets the test suite name and it's folder"""
        if str(tsname).endswith(('.xls', '.xlsx')):
            tsname = str(tsname).replace('.xlsx', '')
            tsname = str(tsname).replace('.xls', '')
        tsname = str(tsname).replace('.', '_').replace(' ', '_')
        # Create test suite folder with name dependent on tsname value
        if f.pathexists(f.workingdir, tsname):
            f.clrdir(f.workingdir, tsname)
        f.mkdir(f.workingdir, tsname)
        return tsname

    @property
    def actline(self):
        return self.line

    @actline.setter
    def actline(self, line):
        self.line.append(line)
        self.file_.write(self.trim_line(line) + '\n')
