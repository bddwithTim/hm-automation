import os
import src.lib.base as base
from src.lib.prep import Prep as prep
from src.lib.prep import Auxiliary
from src.lib.fmanager import FileFolderManager
f = FileFolderManager()
page = Auxiliary()


class _ProductAvailability(prep):
    def __init__(self):
        prep.__init__(self)

    # def to_dtc(self, ref):
    def to_pa(self):
        from src.lib.procreate import Procreate
        self.p = Procreate()

        # Create test case file using base.ts_data['tcname'] value with .csv extension
        csv_file = os.path.join(os.path.join(f.workingdir, base.pa_data['tsname']), base.pa_data['tcname'] + ".csv")
        try:
            self.file_ = open(csv_file, 'w')
        except (PermissionError, FileNotFoundError):
            return ['of', 'the', 'Jedi!']

        """PAGE FLOW SECTION"""
        self.intro_section()
        self.find_the_plan_section()
        self.plan_section()
        self.file_.close()
        return self.p.actline

    def intro_section(self):
        self.p.act(self.file_, self.testname, base.pa_data['tcname'], '')
        self.p.act(self.file_, self.description, base.pa_data['desc'], '')
        self.p.act(self.file_, self.type, base.pa_data['type'], '')
        self.p.act(self.file_, self.url, base.pa_data['uri'], 'UHOne')
        self.p.act(self.file_, self.enter, base.pa_data['zipcode'], self.elmnt_zipcode)
        self.p.act(self.file_, self.pause, '5', 'seconds')
        """for zipcode with county input"""
        if page.has_county_selection(base.pa_data['zipcode'], f.convert):
            self.p.act(self.file_, self.select, 'County: ' + base.counties[base.pa_data['zipcode']], self.elmnt_county)

    def find_the_plan_section(self):
        self.p.act(self.file_, self.select, 'Applicant: ' + self.applicantgender[0],
                   self.elmnt_uho_app_gendr_lst + '1' + self.gt)
        self.p.act(self.file_, self.enter, self.applicantdob[0], self.elmnt_uho_app_dob_fld + '1' + self.gt, '', 0)
        self.p.act(self.file_, self.select, 'Tobacco: No', self.elmnt_uho_app_tobacco_lst + '1' + self.gt)
        self.p.act(self.file_, self.click, 'View Plans', self.elmnt_uho_view_plans_bttn)
        self.p.act(self.file_, self.pause, '3', 'seconds')

    def plan_section(self):
        tab = ' tab'
        hospital = 'Hospital & Doctor'
        ancillary = 'Vision and More'
        ancillary2 = 'More Coverage'
        for i, plan in enumerate(base.pa_data['planlist']):
            self.p.act(self.file_, self.click, 'Expand Plan Selection',
                       '<uho_plan_menu_dropdown>', m='m')
            if 'short term' == plan:
                plan = str(plan).replace(self.plan_stm, 'Short Term Medical')
                self.p.act(self.file_, self.verify, 'Displayed: ' + self.plan_stm + tab, self.elmnt_uho_stm_tab, m='m-')
                self.p.act(self.file_, self.click, self.plan_stm + tab, self.elmnt_uho_stm_tab, m='m-')
                # MOBILE SPECIFIC STEP
                self.p.act(self.file_, self.verify, 'Displayed: ' + self.plan_stm + tab, '<uho_plan_menu_stm>', m='m')
                self.p.act(self.file_, self.click, self.plan_stm + tab, '<uho_plan_menu_stm>', m='m')
            elif 'fixed indemnity' == plan:
                self.p.act(self.file_, self.verify, 'Displayed: ' + hospital + tab, self.elmnt_uho_hospital_tab, m='m-')
                self.p.act(self.file_, self.click, hospital + tab, self.elmnt_uho_hospital_tab, m='m-')
                # MOBILE SPECIFIC STEP
                self.p.act(self.file_, self.verify, 'Displayed: ' + hospital + tab, '<uho_plan_menu_hospital>', m='m')
                self.p.act(self.file_, self.click, hospital + tab, '<uho_plan_menu_hospital>', m='m')
            elif 'core access' == plan:
                self.p.act(self.file_, self.verify, 'Displayed: ' + hospital + tab, self.elmnt_uho_hospital_tab, m='m-')
                self.p.act(self.file_, self.click, hospital + tab, self.elmnt_uho_hospital_tab, m='m-')
                # MOBILE SPECIFIC STEP
                self.p.act(self.file_, self.verify, 'Displayed: ' + hospital + tab, '<uho_plan_menu_hospital>', m='m')
                self.p.act(self.file_, self.click, hospital + tab, '<uho_plan_menu_hospital>', m='m')
            elif str(self.plan_dental).lower() == plan or str(self.plan_dental_plus).lower() == plan:
                self.p.act(self.file_, self.verify, 'Displayed: ' + self.plan_dental + tab, self.elmnt_uho_dental_tab, m='m-')
                self.p.act(self.file_, self.click, self.plan_dental + tab, self.elmnt_uho_dental_tab, m='m-')
                # MOBILE SPECIFIC STEP
                self.p.act(self.file_, self.verify, 'Displayed: ' + self.plan_dental + tab, '<uho_plan_menu_dental>', m='m')
                self.p.act(self.file_, self.click, self.plan_dental + tab, '<uho_plan_menu_dental>', m='m')
            elif str(self.plan_apg).lower() == plan:
                self.p.act(self.file_, self.verify, 'Displayed: ' + self.plan_apg + tab, self.elmnt_uho_accident_pro, m='m-')
                self.p.act(self.file_, self.click, self.plan_apg + tab, self.elmnt_uho_accident_pro, m='m-')
                # MOBILE SPECIFIC STEP
                self.p.act(self.file_, self.verify, 'Displayed: ' + self.plan_apg + tab, '<uho_plan_menu_accident_pro>', m='m')
                self.p.act(self.file_, self.click, self.plan_apg + tab, '<uho_plan_menu_accident_pro>', m='m')
            elif str(self.plan_asg).lower() == plan or 'accident premier' == plan:
                self.p.act(self.file_, self.verify, 'Displayed: ' + self.plan_asg + tab, self.elmnt_uho_accident_tab, m='m-')
                self.p.act(self.file_, self.click, self.plan_asg + tab, self.elmnt_uho_accident_tab, m='m-')
                # MOBILE SPECIFIC STEP
                self.p.act(self.file_, self.verify, 'Displayed: ' + self.plan_asg + tab, '<uho_plan_menu_accident>', m='m')
                self.p.act(self.file_, self.click, self.plan_asg + tab, '<uho_plan_menu_accident>', m='m')
            elif str(self.plan_critical).lower() in plan:
                self.p.act(self.file_, self.verify, 'Displayed: ' + self.plan_critical + tab, self.elmnt_uho_crit_illness_tab, m='m-')
                self.p.act(self.file_, self.click, self.plan_critical + tab, self.elmnt_uho_crit_illness_tab, m='m-')
                # MOBILE SPECIFIC STEP
                self.p.act(self.file_, self.verify, 'Displayed: ' + self.plan_critical + tab, '<uho_plan_menu_critical_illness>', m='m')
                self.p.act(self.file_, self.click, self.plan_critical + tab, '<uho_plan_menu_critical_illness>', m='m')
            else:
                # if page.has_ancillary_tab(base.pa_data['zipcode'], base.pa_data['type'], plan):
                #     if str(self.plan_vision).lower() in base.pa_data['planlist']:
                #         self.p.act(self.file_, self.click, ancillary + tab, self.elmnt_uho_ancillary_tab, m='m-')
                #         # MOBILE SPECIFIC STEP
                #         self.p.act(self.file_, self.click, ancillary + tab, '<uho_plan_menu_vision_and_more>', m='m')
                #     else:
                #         self.p.act(self.file_, self.click, ancillary2 + tab, self.elmnt_uho_ancillary_tab2, m='m-')
                #         # MOBILE SPECIFIC STEP
                #         self.p.act(self.file_, self.click, ancillary2 + tab, '<uho_plan_menu_more_coverage>', m='m')
                ancillary_tab = page.has_ancillary_tab(base.pa_data['state'], base.pa_data['type'])
                if ancillary_tab == 'visionandmore':
                    self.p.act(self.file_, self.click, ancillary + tab, self.elmnt_uho_ancillary_tab, m='m-')
                    # MOBILE SPECIFIC STEP
                    self.p.act(self.file_, self.click, ancillary + tab, '<uho_plan_menu_vision_and_more>', m='m')
                    uho_plan_menu_more_vision = '<uho_plan_menu_more_vision>'
                    uho_plan_menu_more_supplemental = '<uho_plan_menu_more_supplemental>'
                    uho_plan_menu_more_term_life = '<uho_plan_menu_more_term_life>'
                    uho_plan_menu_more_discount_card = '<uho_plan_menu_more_discount_card>'
                elif ancillary_tab == 'morecoverage':
                    self.p.act(self.file_, self.click, ancillary2 + tab, self.elmnt_uho_ancillary_tab2, m='m-')
                    # MOBILE SPECIFIC STEP
                    self.p.act(self.file_, self.click, ancillary2 + tab, '<uho_plan_menu_more_coverage>', m='m')
                    uho_plan_menu_more_vision = None
                    uho_plan_menu_more_supplemental = '<uho_plan_menu_more_supplemental>'
                    uho_plan_menu_more_term_life = '<uho_plan_menu_more_term_life>'
                    uho_plan_menu_more_discount_card = '<uho_plan_menu_more_discount_card>'
                else:
                    # MOBILE SPECIFIC STEP
                    uho_plan_menu_more_vision = '<uho_plan_menu_vision_and_more>'
                    uho_plan_menu_more_supplemental = '<uho_plan_menu_supplemental>'
                    uho_plan_menu_more_term_life = '<uho_plan_menu_term_life>'
                    uho_plan_menu_more_discount_card = '<uho_plan_menu_discount>'
                if str(self.plan_vision).lower() == plan:
                    self.p.act(self.file_, self.verify, 'Displayed: ' + 'Vision tab', self.elmnt_uho_vision_tab, m='m-')
                    self.p.act(self.file_, self.click, 'Vision tab', self.elmnt_uho_vision_tab, m='m-')
                    # MOBILE SPECIFIC STEP
                    self.p.act(self.file_, self.verify, 'Displayed: ' + 'Vision tab', uho_plan_menu_more_vision, m='m')
                    self.p.act(self.file_, self.click, 'Vision tab', uho_plan_menu_more_vision, m='m')
                elif 'supp indemnity' == plan:
                    self.p.act(self.file_, self.verify, 'Displayed: ' + self.plan_hsg + tab, self.elmnt_uho_supplemental_tab, m='m-')
                    self.p.act(self.file_, self.click, self.plan_hsg + tab, self.elmnt_uho_supplemental_tab, m='m-')
                    # MOBILE SPECIFIC STEP
                    self.p.act(self.file_, self.verify, 'Displayed: ' + self.plan_hsg + tab, uho_plan_menu_more_supplemental, m='m')
                    self.p.act(self.file_, self.click, self.plan_hsg + tab, uho_plan_menu_more_supplemental, m='m')
                elif str(self.plan_tl).lower() == plan:
                    self.p.act(self.file_, self.verify, 'Displayed: ' + self.plan_tl + tab, self.elmnt_uho_term_life_tab, m='m-')
                    self.p.act(self.file_, self.click, self.plan_tl + tab, self.elmnt_uho_term_life_tab, m='m-')
                    # MOBILE SPECIFIC STEP
                    self.p.act(self.file_, self.verify, 'Displayed: ' + self.plan_tl + tab, uho_plan_menu_more_term_life, m='m')
                    self.p.act(self.file_, self.click, self.plan_tl + tab, uho_plan_menu_more_term_life, m='m')
                elif str(self.plan_discount).lower() in plan:
                    # self.p.act(self.file_, self.click, self.plan_discount + tab, self.elmnt_uho_discount_tab, m='m-')
                    self.p.act(self.file_, self.verify, 'Displayed: ' + self.plan_discount + tab,
                               self.elmnt_uho_discount_tab, m='m-')
                    # MOBILE SPECIFIC STEP
                    # self.p.act(self.file_, self.click, self.plan_discount + tab, '<uho_plan_menu_more_discount_card>',
                    #            m='m')
                    self.p.act(self.file_, self.verify, 'Displayed: ' + self.plan_discount + tab,
                               uho_plan_menu_more_discount_card, m='m')
