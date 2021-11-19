import os
import src.lib.base as base
from src.lib.prep import Prep as prep
from src.lib.prep import Auxiliary
from src.lib.fmanager import FileFolderManager
f = FileFolderManager()
page = Auxiliary()


class _DTC(prep):
    def __init__(self):
        prep.__init__(self)

    # def to_dtc(self, ref):
    def to_dtc(self):
        from src.lib.procreate import Procreate
        self.p = Procreate()
        """Setting dict variables"""
        self.marital_field = dict()
        self.email_field = dict()
        self.phone_field = dict()
        self.ht_wt_field = dict()
        self.occupation_field = dict()
        self.license_field = dict()
        self.relationship_field = dict()

        # Create test case file using base.ts_data['tcname'] value with .csv extension
        csv_file = os.path.join(os.path.join(f.workingdir, base.ts_data['tsname']), base.ts_data['tcname'] + ".csv")
        try:
            self.file_ = open(csv_file, 'w')
        except (PermissionError, FileNotFoundError):
            return ['of', 'the', 'Jedi!']

        """PAGE FLOW SECTION"""
        self.intro_section()
        self.find_the_plan_section()
        self.plan_section()
        self.shopping_cart_section()
        self.applicant_info_section()
        self.question_section()
        self.summary_section()
        self.payment_section(base.ts_data['data'])
        self.review_submit_section()
        self.thank_you_section()
        self.file_.close()
        return self.p.actline

    def intro_section(self):
        self.p.act(self.file_, self.testname, base.ts_data['tcname'], '')
        self.p.act(self.file_, self.description, base.ts_data['desc'], '')
        self.p.act(self.file_, self.type, base.ts_data['type'], '')
        self.p.act(self.file_, self.url, base.ts_data['uri'], '<uho_census_title>')
        self.p.act(self.file_, self.enter, base.ts_data['zipcode'], self.elmnt_zipcode)
        # self.p.act(self.file_, self.pause, '5', 'seconds')
        """for zipcode with county input"""
        if page.has_county_selection(base.ts_data['zipcode']):
            self.p.act(self.file_, self.select, 'County: ' + base.ts_data['county'], self.elmnt_county)

    def find_the_plan_section(self):
        for i, applicant in enumerate(base.ts_data['applicants']):
            if applicant == 'nan':
                continue

            # DO MOBILE SPECIFIC STEPS (EXPAND SPOUSE/CHILD TO DISPLAY FIELDS
            # if i == 1:
            #     self.p.act(self.file_, self.click, 'Expand Spouse',
            #                '<uho_spouse_expand>', m='m')
            # elif i == 2:
            #     self.p.act(self.file_, self.click, 'Expand Child 1',
            #                '<uho_child1_expand>', m='m')
            # elif i == 3:
            #     self.p.act(self.file_, self.click, 'Expand Child 2',
            #                '<uho_child2_expand>', m='m')

            # SPECIFIC STEPS (EXPAND SPOUSE/CHILD TO DISPLAY FIELDS
            if i == 1:
                self.p.act(self.file_, self.click, 'Expand Spouse',
                           '<uho_spouse_expand>', )
            elif i == 2:
                self.p.act(self.file_, self.click, 'Expand Child 1',
                           '<uho_child1_expand>', )
            elif i == 3:
                self.p.act(self.file_, self.click, 'Expand Child 2',
                           '<uho_child1_expand>', )

            # self.p.act(self.file_, self.select, 'Applicant: ' + applicant,
            #            self.elmnt_uho_app_gendr_lst + str(i + 1) + self.gt)
            self.p.act(self.file_, self.click, 'Applicant: ' + applicant,
                       self.elmnt_uho_app_gendr_lst + str(i + 1) + self.gt)
            self.p.act(self.file_, self.enter, str(base.ts_data['applicantsdob'][i]),
                       self.elmnt_uho_app_dob_fld + str(i + 1) + self.gt, '', 0)
            if str(base.ts_data['applicantstobacco'][i]) == 'nan':
                self.p.act(self.file_, self.select, 'Tobacco: No', self.elmnt_uho_app_tobacco_lst + str(i+1) + self.gt)
            else:
                self.p.act(self.file_, self.select, 'Tobacco: ' + str(base.ts_data['applicantstobacco'][i]),
                           self.elmnt_uho_app_tobacco_lst + str(i + 1) + self.gt)
        self.p.act(self.file_, self.click, 'View Plans', self.elmnt_uho_view_plans_bttn)
        for age in base.ts_data['applicantsage']:
            if age in ['nan', 'nat']:
                continue
            if age > 64:
                self.p.act(self.file_, self.verify, 'Displayed: Discover more plan options!',
                           self.elmnt_uho_modal_65_dlg, '', 0)
                self.p.act(self.file_, self.click, 'Continue button', self.elmnt_uho_modal_65_continue_bttn)
                break

    def plan_section(self):
        tab = ' tab'
        hospital = 'Hospital & Doctor'
        ancillary = 'Vision and More'
        ancillary2 = 'More Coverage'
        for i, plan in enumerate(base.ts_data['plans']):
            self.p.act(self.file_, self.click, 'Expand Plan Selection',
                       '<uho_plan_menu_dropdown>', m='m')
            if self.plan_stm in plan:
                plan = str(plan).replace(self.plan_stm, 'Short Term Medical')
                # self.p.act(self.file_, self.click, self.plan_stm + tab, self.elmnt_uho_stm_tab, m='m-')
                self.p.act(self.file_, self.choose, 'Plan Type| Short Term | Short Term',
                           '[data-ng-repeat-start=\'applicationType in applicationTypes\'] | a[role=button] | a[role=button]',
                           m='m-')
                # MOBILE SPECIFIC STEP
                self.p.act(self.file_, self.click, self.plan_stm + tab, '<uho_plan_menu_stm>', m='m')
                # 12/15 release: added if 'STM Copay Select A' in plan:
                # if 'Short Term Medical Copay Select A' in plan:
                #     self.p.act(self.file_, self.click, 'Page 3', 'a[data-gtm-id*=Pagination3]')
                # self.p.act(self.file_, self.choose, 'Plan | ' + plan + ' | Add to Cart',
                #            self.elmnt_uho_plan_lst + self.pipe + self.elmnt_uho_plan_name_lbl + self.pipe +
                #            self.elmnt_uho_add_to_cart)
                self.p.act(self.file_, self.choose, 'Plan | ' + plan + ' | Add to Cart',
                           '[data-ng-repeat*=\'pagedPlans\']:not([style*=\'none\'])' + self.pipe + self.elmnt_uho_plan_name_lbl + self.pipe +
                           self.elmnt_uho_add_to_cart)
            elif self.plan_ihc in plan:
                # self.p.act(self.file_, self.click, hospital + tab, self.elmnt_uho_hospital_tab, m='m-')
                self.p.act(self.file_, self.choose, 'Plan Type| Hospital & Doctor | Hospital & Doctor',
                           '[data-ng-repeat-start=\'applicationType in applicationTypes\'] | a[role=button] | a[role=button]',
                           m='m-')
                # MOBILE SPECIFIC STEP
                self.p.act(self.file_, self.click, hospital + tab, '<uho_plan_menu_hospital>', m='m')
                self.p.act(self.file_, self.choose, 'Plan | ' + plan + ' | Add to Cart',
                           '[data-ng-repeat*=\'pagedPlans\']:not([style*=\'none\'])' + self.pipe + self.elmnt_uho_plan_name_lbl + self.pipe +
                           self.elmnt_uho_add_to_cart)
            elif self.plan_hpg in plan:
                # self.p.act(self.file_, self.click, hospital + tab, self.elmnt_uho_hospital_tab, m='m-')
                self.p.act(self.file_, self.choose, 'Plan Type| Hospital & Doctor | Hospital & Doctor',
                           '[data-ng-repeat-start=\'applicationType in applicationTypes\'] | a[role=button] | a[role=button]',
                           m='m-')
                # MOBILE SPECIFIC STEP
                self.p.act(self.file_, self.click, hospital + tab, '<uho_plan_menu_hospital>', m='m')
                self.p.act(self.file_, self.choose, 'Plan | ' + plan + ' | Add to Cart',
                           '[data-ng-repeat*=\'pagedPlans\']:not([style*=\'none\'])' + self.pipe + self.elmnt_uho_plan_name_lbl + self.pipe +
                           self.elmnt_uho_add_to_cart)
            elif self.plan_dental in plan \
                    or plan in ['Essential', 'Primary', 'Essential Preferred', 'Primary Plus', 'Primary Preferred',
                                     'Premier Choice', 'Premier Elite', 'Premier Plus', 'Premier Max',
                                     'Primary Preferred Plus']:
                # self.p.act(self.file_, self.click, self.plan_dental + tab, self.elmnt_uho_dental_tab, m='m-')
                self.p.act(self.file_, self.choose, 'Plan Type| Dental | Dental',
                           '[data-ng-repeat-start=\'applicationType in applicationTypes\'] | a[role=button] | a[role=button]',
                           m='m-')
                # MOBILE SPECIFIC STEP
                self.p.act(self.file_, self.click, self.plan_dental + tab, '<uho_plan_menu_dental>', m='m')
                self.p.act(self.file_, self.choose, 'Plan | ' + plan + ' | Add to Cart',
                           self.elmnt_uho_plan_lst + self.pipe + self.elmnt_uho_plan_name_lbl + self.pipe +
                           self.elmnt_uho_add_to_cart)
            elif self.plan_apg in plan or self.plan_aeg in plan:
                # self.p.act(self.file_, self.click, self.plan_apg + tab, self.elmnt_uho_accident_pro, m='m-')
                self.p.act(self.file_, self.choose, 'Plan Type| Accident ProGuard | Accident ProGuard',
                           '[data-ng-repeat-start=\'applicationType in applicationTypes\'] | a[role=button] | a[role=button]',
                           m='m-')
                # MOBILE SPECIFIC STEP
                self.p.act(self.file_, self.click, self.plan_apg + tab, '<uho_plan_menu_accident_pro>', m='m')
                self.p.act(self.file_, self.choose, 'Plan | ' + plan + ' | Add to Cart',
                           self.elmnt_uho_plan_lst + self.pipe + self.elmnt_uho_plan_name_lbl + self.pipe +
                           self.elmnt_uho_add_to_cart)
            elif self.plan_asg in plan:
                # self.p.act(self.file_, self.click, self.plan_asg + tab, self.elmnt_uho_accident_tab, m='m-')
                self.p.act(self.file_, self.choose, 'Plan Type| Accident | Accident',
                           '[data-ng-repeat-start=\'applicationType in applicationTypes\'] | a[role=button] | a[role=button]',
                           m='m-')
                # MOBILE SPECIFIC STEP
                self.p.act(self.file_, self.click, self.plan_asg + tab, '<uho_plan_menu_accident>', m='m')
                self.p.act(self.file_, self.choose, 'Plan | ' + plan + ' | Add to Cart',
                           self.elmnt_uho_plan_lst + self.pipe + self.elmnt_uho_plan_name_lbl + self.pipe +
                           self.elmnt_uho_add_to_cart)
            elif self.plan_critical in plan:
                # self.p.act(self.file_, self.click, self.plan_critical + tab, self.elmnt_uho_crit_illness_tab, m='m-')
                self.p.act(self.file_, self.choose, 'Plan Type| Critical Illness | Critical Illness',
                           '[data-ng-repeat-start=\'applicationType in applicationTypes\'] | a[role=button] | a[role=button]',
                           m='m-')
                # MOBILE SPECIFIC STEP
                self.p.act(self.file_, self.click, self.plan_critical + tab, '<uho_plan_menu_critical_illness>', m='m')
                self.p.act(self.file_, self.choose, 'Plan | ' + plan + ' | Add to Cart',
                           self.elmnt_uho_plan_lst + self.pipe + self.elmnt_uho_plan_name_lbl + self.pipe +
                           self.elmnt_uho_add_to_cart)
            else:
                ancillary_tab = page.has_ancillary_tab(base.ts_data['state'], base.ts_data['type'])
                if ancillary_tab == 'visionandmore':
                # if page.has_ancillary_tab(base.ts_data['zipcode'], base.ts_data['type'], plan):
                #     self.p.act(self.file_, self.click, ancillary + tab, self.elmnt_uho_ancillary_tab, m='m-')
                    self.p.act(self.file_, self.click, ancillary + tab, 'li.btn-group.dropdown #simple-btn-keyboard-nav', m='m-')
                    # MOBILE SPECIFIC STEP
                    self.p.act(self.file_, self.click, ancillary + tab, '<uho_plan_menu_vision_and_more>', m='m')
                    uho_plan_menu_more_vision = '<uho_plan_menu_more_vision>'
                    uho_plan_menu_more_supplemental = '<uho_plan_menu_more_supplemental>'
                    uho_plan_menu_more_term_life = '<uho_plan_menu_more_term_life>'
                    uho_plan_menu_more_discount_card = '<uho_plan_menu_more_discount_card>'
                elif ancillary_tab == 'morecoverage':
                    # self.p.act(self.file_, self.click, ancillary2 + tab, self.elmnt_uho_ancillary_tab2, m='m-')
                    self.p.act(self.file_, self.click, ancillary + tab, 'li.btn-group.dropdown #simple-btn-keyboard-nav', m='m-')
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
                if self.plan_vision in plan:
                    # self.p.act(self.file_, self.click, 'Vision tab', self.elmnt_uho_vision_tab, m='m-')
                    self.p.act(self.file_, self.choose, 'Plan Type| Vision | Vision',
                               '[data-ng-repeat=\'groupedApplicationType in groupedApplicationTypes\'] | a[role=button] | a[role=button]',
                               m='m-')
                    # MOBILE SPECIFIC STEP
                    self.p.act(self.file_, self.click, 'Vision tab', uho_plan_menu_more_vision, m='m')
                    self.p.act(self.file_, self.choose, 'Plan | ' + plan + ' | Add to Cart',
                               self.elmnt_uho_plan_lst + self.pipe + self.elmnt_uho_plan_name_lbl + self.pipe +
                               self.elmnt_uho_add_to_cart)
                elif self.plan_hsg in plan:
                    # self.p.act(self.file_, self.click, self.plan_hsg + tab, self.elmnt_uho_supplemental_tab, m='m-')
                    self.p.act(self.file_, self.choose, 'Plan Type| Hospital SafeGuard | Hospital SafeGuard',
                               '[data-ng-repeat=\'groupedApplicationType in groupedApplicationTypes\'] | a[role=button] | a[role=button]',
                               m='m-')
                    # MOBILE SPECIFIC STEP
                    self.p.act(self.file_, self.click, self.plan_hsg + tab, uho_plan_menu_more_supplemental, m='m')
                    self.p.act(self.file_, self.choose, 'Plan | ' + plan + ' | Add to Cart',
                               self.elmnt_uho_plan_lst + self.pipe + self.elmnt_uho_plan_name_lbl + self.pipe +
                               self.elmnt_uho_add_to_cart)
                elif self.plan_tl in plan:
                    # self.p.act(self.file_, self.click, self.plan_tl + tab, self.elmnt_uho_term_life_tab, m='m-')
                    self.p.act(self.file_, self.choose, 'Plan Type| Term Life | Term Life',
                               '[data-ng-repeat=\'groupedApplicationType in groupedApplicationTypes\'] | a[role=button] | a[role=button]',
                               m='m-')
                    # MOBILE SPECIFIC STEP
                    self.p.act(self.file_, self.click, self.plan_tl + tab, uho_plan_menu_more_term_life, m='m')
                    self.p.act(self.file_, self.choose, 'Plan | ' + plan + ' | Add to Cart',
                               self.elmnt_uho_plan_lst + self.pipe + self.elmnt_uho_plan_name_lbl + self.pipe +
                               self.elmnt_uho_add_to_cart)
                elif self.plan_discount in plan:
                    # self.p.act(self.file_, self.click, self.plan_discount + tab, self.elmnt_uho_discount_tab, m='m-')
                    self.p.act(self.file_, self.choose, 'Plan Type| Discount Card | Discount Card',
                               '[data-ng-repeat=\'groupedApplicationType in groupedApplicationTypes\'] | a[role=button] | a[role=button]',
                               m='m-')
                    # MOBILE SPECIFIC STEP
                    self.p.act(self.file_, self.click, self.plan_discount + tab, uho_plan_menu_more_discount_card, m='m')
                    self.p.act(self.file_, self.click, 'Add to Cart button', self.elmnt_uho_add_to_cart)
                elif self.plan_disability in plan:
                    plan = str(plan).replace(self.plan_disability, 'Disability Income')
                    self.p.act(self.file_, self.click, self.plan_disability + tab, self.elmnt_uho_disability_tab)
                    self.p.act(self.file_, self.choose, 'Plan | ' + plan + ' | Add to Cart',
                               self.elmnt_uho_plan_lst + self.pipe + self.elmnt_uho_plan_name_lbl + self.pipe +
                               self.elmnt_uho_add_to_cart)
            if page.has_expand_coverage_pop_up(base.ts_data['zipcode'], plan, i):  # and self.plan_discount not in plan:
                self.p.uho_expand_coverage_dialog(self.file_)

    def shopping_cart_section(self):
        self.p.act(self.file_, self.verify, 'Displayed: Shopping Cart page', self.elmnt_uho_shopping_cart_page, '', 0)
        # self.p.act(self.file_, 'get', 'rate', '.cartPlanCost')
        # self.p.act(self.file_, 'get', 'rate', '.customEstimatedPremiumForAllPlans')
        self.p.act(self.file_, self.click, 'Apply button', self.elmnt_uho_apply_bttn)
        if page.has_consecutive_stm_pop_up(base.ts_data['state'], base.ts_data['plans']):
            for i, plan in enumerate(base.ts_data['plans']):
                if self.plan_stm in plan:
                    other_options = base.ts_data['plandict'][plan][self.plan + str(i + 1) + ' ' +
                                                                   str(self.planotheroptions).lower().strip()]
                    if 'add consecutive' in other_options:
                        consecutive_plan = True
                    else:
                        consecutive_plan = False
                    break
            self.p.uho_consecutive_stm_dialog(self.file_, consecutive_plan)

    def applicant_info_section(self):
        self.p.act(self.file_, self.verify, 'Displayed: Applicant information page',
                   self.elmnt_uho_app_info_header_page, '', 0)
        for i, applicant in enumerate(base.ts_data['applicants']):
            if applicant in ['nan', None, ' ']:
                continue
            self.p.act(self.file_, self.enter, self.applicantfname[i],
                       self.elmnt_uho_app_fname_fld + str(i + 1) + self.gt, '', 0)
            self.p.act(self.file_, self.enter, self.applicantlname, self.elmnt_uho_app_lname_fld + str(i + 1) + self.gt,
                       '', 0)
            self.marital_field[i] = 0
            self.email_field[i] = 0
            self.phone_field[i] = 0
            self.ht_wt_field[i] = 0
            self.occupation_field[i] = 0
            self.relationship_field[i] = 0
            self.license_field[i] = 0
            for plan in base.ts_data['plans']:
                if page.has_marital_status_field(base.ts_data['zipcode'], plan, i) and not self.marital_field[i]:
                    status = 'single'
                    if base.ts_data['applicants'][1] not in ['nan', None, ' ']:
                        status = 'married'
                    self.p.act(self.file_, self.click, status, self.elmnt_uho_app_marital_fld + status + self.gt, '', 0)
                    self.marital_field[i] = 1
                if page.has_height_weight_field(base.ts_data['zipcode'], plan, i) and not self.ht_wt_field[i]:
                    self.p.act(self.file_, self.enter, base.ts_data['applicantheightft'][i],
                               self.elmnt_uho_app_height_ft_fld + str(i+1) + self.gt, '', 0)
                    self.p.act(self.file_, self.enter, base.ts_data['applicantheightin'][i],
                               self.elmnt_uho_app_height_in_fld + str(i+1) + self.gt, '', 0)
                    self.p.act(self.file_, self.enter, base.ts_data['applicantweightlbs'][i],
                               self.elmnt_uho_app_weight_lb_fld + str(i+1) + self.gt, '', 0)
                    self.ht_wt_field[i] = 1
                if page.has_driver_license(base.ts_data['zipcode'], plan, i) and not self.license_field[i]:
                    self.p.act(self.file_, self.enter, 'F25592150094',
                               self.elmnt_uho_app_driver_lcnse_fld + str(i + 1) + self.gt, '', 0)
                    self.p.act(self.file_, self.select, 'State: ' + base.ts_data['state'], 
                               self.elmnt_uho_app_driver_state_fld)
                    self.license_field[i] = 1
                if page.has_email_field(base.ts_data['zipcode'], plan, i) and not self.email_field[i]:
                    self.p.act(self.file_, self.enter, self.applicantemailadd,
                               self.elmnt_uho_app_email_fld + str(i + 1) + self.gt, '', 0)
                    self.email_field[i] = 1
                if page.has_phone_field(base.ts_data['zipcode'], plan, i) and not self.phone_field[i]:
                    self.p.act(self.file_, self.enter, self.applicantphonenum,
                               self.elmnt_uho_app_phone_fld + str(i + 1) + self.gt, '', 0)
                    self.phone_field[i] = 1
                if page.has_occupation_field(base.ts_data['zipcode'], plan, i) and not self.occupation_field[i]:
                    self.p.act(self.file_, self.enter, self.applicantoccupation,
                               self.elmnt_uho_app_occupation_fld + str(i+1) + self.gt, '', 0)
                    self.occupation_field[i] = 1
                if page.has_relationship_field(base.ts_data['zipcode'], plan, i) and not self.relationship_field[i]:
                    self.p.act(self.file_, self.enter, self.applicantrelationship,
                               self.elmnt_uho_app_relationship_fld + str(i + 1) + self.gt, '', 0)
                    self.relationship_field[i] = 1
            ssn = self.p.get_attrib_from_notes(base.ts_data['plans'], base.ts_data['plandict'], 'ssn')
            if i in ssn:
                self.p.act(self.file_, self.enter, self.ssn, self.elmnt_uho_app_ssn_fld + str(i + 1) + self.gt, '', 0)
        self.p.act(self.file_, self.enter, self.applicantaddress, self.elmnt_uho_app_contact_info_add_fld, '', 0)
        self.p.act(self.file_, self.enter, self.applicantcity, self.elmnt_uho_app_contact_info_city_fld, '', 0)

        for plan in base.ts_data['plans']:
            if page.has_beneficiary_fields(plan):
                self.p.act(self.file_, self.enter, self.applicantbeneficiary, self.elmnt_uho_beneficiary_fname_fld,
                           '', 0)
                self.p.act(self.file_, self.enter, self.applicantlname, self.elmnt_uho_beneficiary_lname_fld, '', 0)
                self.p.act(self.file_, self.enter, self.applicantrelationship,
                           self.elmnt_uho_beneficiary_relationship_fld,
                           '', 0)
                self.p.act(self.file_, self.enter, self.applicantbeneficiaryage, self.elmnt_uho_beneficiary_age_fld,
                           '', 0)
                break
        # for plan in base.ts_data['plans']:
        #     if self.plan_critical in plan:
        #         self.p.act(self.file_, self.enter, self.applicantbeneficiary, self.elmnt_uho_beneficiary_fname_fld, '', 0)
        #         self.p.act(self.file_, self.enter, self.applicantlname, self.elmnt_uho_beneficiary_lname_fld, '', 0)
        #         self.p.act(self.file_, self.enter, self.applicantrelationship,
        #                    self.elmnt_uho_beneficiary_relationship_fld, '', 0)
        #         self.p.act(self.file_, self.enter, self.applicantbeneficiaryage, self.elmnt_uho_beneficiary_age_fld, '', 0)
        #     elif self.plan_disability in plan:
        #         self.p.act(self.file_, self.enter, self.applicantoccupation, self.elmnt_uho_emp_occupation_fld, '', 0)
        #         self.p.act(self.file_, self.enter, 'UHG', self.elmnt_uho_emp_employer_name_fld, '', 0)
        #         self.p.act(self.file_, self.enter, 'Developer', self.elmnt_uho_emp_duties_fld, '', 0)
        #         self.p.act(self.file_, self.select, 'Year:1-5 years', self.elmnt_uho_emp_occupation_length_fld, '', 0)
        #         self.p.act(self.file_, self.enter, self.applicantaddress, self.elmnt_uho_emp_employer_address_fld, '', 0)
        #         self.p.act(self.file_, self.enter, self.applicantcity, self.elmnt_uho_emp_employer_city_fld, '', 0)
        #         self.p.act(self.file_, self.select, 'State:' + base.ts_data['state'], self.elmnt_uho_emp_employer_state_fld, '', 0)
        #         self.p.act(self.file_, self.enter, base.ts_data['zipcode'], self.elmnt_uho_emp_employer_zipcode_fld, '', 0)
        #         self.p.act(self.file_, self.click, 'Non-Business Owner',
        #                    self.elmnt_uho_emp_nonbusiness_owner_fld, '', 0)
        #         self.p.act(self.file_, self.enter, '5000', self.elmnt_uho_emp_nonbusiness_monthly_fld, '', 0)
        #         self.p.act(self.file_, self.click, 'No', self.elmnt_uho_emp_nonbusiness_no_bttn, '', 0)
        #         self.p.act(self.file_, self.enter, '50000', self.elmnt_uho_emp_nonbusiness_annual_fld, '', 0)
        self.p.act(self.file_, self.click, 'Continue', self.elmnt_uho_continue_bttn)
        self.p.act(self.file_, self.verify,'Displayed: Resident Physical Address error', '<uho_address_mismatch_error>')
        self.p.act(self.file_, self.verify, '\" Displayed: \"\"Suggested Address:\"\"\"', '<uho_suggested_address_lbl>')
        self.p.act(self.file_, self.click, 'Use This Address button', '<uho_use_this_address>')
        # self.p.act(self.file_, self.click, 'Continue', self.elmnt_uho_continue_bttn)
        if page.has_registration_pop_up(base.ts_data['zipcode']):
            self.p.uho_registration_dialog(self.file_)

    def question_section(self):
        plan_list, plan_index = self.sort_question_page(base.ts_data['plans'])
        for i, plan in enumerate(plan_list):
            """for zipcode with or without question page"""
            question = str(base.ts_data['plandict'][plan][self.plan + str(plan_index[plan]) + 
                                                          self.planappquestions]).lower().strip()
            if page.has_question_page(base.ts_data['state'], plan):
                self.p.act(self.file_, self.verify, 'Displayed: ' + plan + ' Question page ',
                           self.elmnt_uho_question_header_page, '', 0)
                if question == 'don\'t answer':
                    print('don\'t answer the questions...')
                elif question == 'nan':
                    # continue
                    self.p.act(self.file_, self.select, 'Questions: all no', self.elmnt_uho_question_all_no_bttn)
                    self.p.act(self.file_, 'Pause', '1', 'Second')
                else:  # FI, STM, ACC,
                    self.p.act(self.file_, self.select, 'Questions: all no', self.elmnt_uho_question_all_no_bttn)
                    self.p.act(self.file_, 'Pause', '1', 'Seconds')
                    if question == '1 yes':
                        # ## for 12/15/2017 release ###
                        if self.plan_dental in plan:
                            self.p.act(self.file_, self.click, 'Question: 1 YES',
                                       self.elmnt_uho_question_one_yes_bttn)
                        else:
                            self.p.act(self.file_, self.click, 'Question: 1 YES',
                                       self.elmnt_uho_question_one__yes_bttn)
                        if base.ts_data['applicantsnum'] > 1 and self.plan_dental not in plan:
                            self.p.act(self.file_, self.click, 'Applicant: Primary', 
                                       self.elmnt_uho_question_primary_response_bttn)
                        if self.plan_asg in plan or self.plan_hsg in plan:
                            self.p.act(self.file_, self.enter, 'Carrier', self.elmnt_uho_question_carrier_fld)
                            if base.ts_data['zipcode'] in ['72718', '31050']:
                                self.p.act(self.file_, self.enter, 'Coverage', self.elmnt_uho_question_policy_fld)
                            else:
                                self.p.act(self.file_, self.enter, 'Coverage', self.elmnt_uho_question_coverage_fld)
                    elif question == 'tobacco yes':
                        self.p.act(self.file_, self.click, 'Question: Tobacco Yes',
                                   self.elmnt_uho_question_one__yes_bttn)
                        for x, tobacco in enumerate(base.ts_data['applicantstobacco']):
                            if tobacco == 'nan':
                                continue
                            if base.ts_data['applicantsnum'] > 1:
                                if x == 0:
                                    self.p.act(self.file_, self.click, 'Applicant: Primary', 
                                               self.elmnt_uho_question_primary_response_bttn)
                                elif x == 1:
                                    self.p.act(self.file_, self.click, 'Applicant: Spouse', 
                                               self.elmnt_uho_question_spouse_response_bttn)
                                elif x == 2:
                                    self.p.act(self.file_, self.click, 'Applicant: Dependent 1', 
                                               self.elmnt_uho_question_dependent_one_response_bttn)
                                elif x == 3:
                                    self.p.act(self.file_, self.click, 'Applicant: Dependent 2', 
                                               self.elmnt_uho_question_dependent_two_response_bttn)
                    elif question == 'replacement yes':
                        self.p.act(self.file_, self.click, 'Question: Replacement Yes',
                                   self.elmnt_uho_question_replacement_yes_bttn)
                        if base.ts_data['applicantsnum'] > 1:
                            self.p.act(self.file_, self.click, 'Applicant: Primary', 
                                       self.elmnt_uho_question_primary_response_bttn)
                self.p.act(self.file_, self.click, 'Continue', self.elmnt_uho_continue_bttn)

    def summary_section(self):
        plan_list, plan_index = self.sort_question_page(base.ts_data['plans'])
        self.p.act(self.file_, self.verify, 'Displayed: Payment Summary page/header',
                   self.elmnt_uho_payment_summary_header_page, '', 0)
        form = 'form div:nth-child('
        edit = ') div div div button[data-ng-click*=editPlan]'
        save = ') div div div  button[data-ng-click*=savePlanChanges]'
        input_ = 'input#plans_'
        coverage_sdate = '_coverageStartDate'
        for i, plan in enumerate(plan_list):
            coverage_startdate = self.p.convert_date(
                str(base.ts_data['plandict'][plan][self.plan + str(plan_index[plan])
                                                   + self.plancoveragestartdate]).strip(), 'coverage_date')
            if coverage_startdate not in ['nan', 'nat']:
                self.p.act(self.file_, self.click, str(plan) + ' Edit Button', form + str(i + 2) + edit)
                self.p.act(self.file_, self.enter, coverage_startdate, input_ + str(i) + coverage_sdate)
                self.p.act(self.file_, self.enter, coverage_startdate, input_ + str(i) + coverage_sdate)
                self.p.act(self.file_, self.click, str(plan) + ' Save Changes Button', form + str(i + 2) + save)
        ##### self.p.act(self.file_, 'compare', 'base premium rate', '.mc-review-subheader-container:nth-child(3) .col-xs-3')
        self.p.act(self.file_, self.click, 'Continue', self.elmnt_uho_continue_bttn)

    def payment_section(self, data):
        self.p.act(self.file_, self.verify, 'Displayed: Payment Type header', self.elmnt_uho_payment_type_header_page, 
                   '', 0)
        for i, plan in enumerate(base.ts_data['plans']):
            payment_type = base.ts_data['plandict'][plan][self.plan + str(i+1) + self.planpaymenttype]
            if 'EFT' in payment_type:
                self.p.act(self.file_, self.click, payment_type, self.elmnt_uho_payment_eft_bttn, '', 0)
                self.p.act(self.file_, self.click, 'Continue', self.elmnt_uho_continue_bttn)
                self.p.act(self.file_, self.click, 'Checking', self.elmnt_uho_payment_checking_bttn, '', 0)
                # if len(data[self.eftroutingnumber]) < 9:
                #     data[self.eftroutingnumber] = '0' + data[self.eftroutingnumber]
                # self.p.act(self.file_, self.enter, data[self.eftroutingnumber], '#routingNumber', '', 0)
                # self.p.act(self.file_, self.enter, data[self.eftaccountnumber], '#bankAccountNumber', '', 0)
                self.p.act(self.file_, self.enter, self.eftroutingnum, self.elmnt_uho_payment_eft_routing_fld, '', 0)
                self.p.act(self.file_, self.enter, self.eftaccountnum, self.elmnt_uho_payment_eft_account_fld, '', 0)
                self.p.act(self.file_, self.select, "Desired Day for Monthly Withdrawal: 15",
                           "<uho_eft_desired_monthly_withd_lst>", '', 0)
            # elif payment_type == 'Credit Card':
            else:
                self.p.act(self.file_, self.click, payment_type, self.elmnt_uho_payment_cc_bttn, '', 0)
                self.p.act(self.file_, self.click, 'Continue', self.elmnt_uho_continue_bttn)
                # self.p.act(self.file_, self.enter, str(data[self.creditcardnumber]).replace(' ', ''),
                #            self.elmnt_uho_payment_cc_number_fld, '', 0)
                # self.p.act(self.file_, self.enter, data[self.creditcardzip], self.elmnt_uho_payment_cc_zipcode_fld, '',
                #            0)
                # self.p.act(self.file_, self.select, self.creditcardexpmonth, self.elmnt_uho_payment_cc_expiry_month_lst,
                #            '', 0)
                # self.p.act(self.file_, self.select, self.creditcardexpyear, self.elmnt_uho_payment_cc_expiry_year_lst,
                #            '', 0)
                # self.p.act(self.file_, self.select, self.creditcardexpday, self.elmnt_uho_payment_cc_expiry_day_lst, '',
                #            0)
                self.p.act(self.file_, self.verify, 'Displayed: Secure Payment Info',
                           '<uho_payment_type_header>', '', 0)
                self.p.act(self.file_, self.pause, '5', 'seconds')
                self.p.act(self.file_, self.switch, 'to trust commerce i frame',
                           'iframe#trust-commerce-iframe', '')
                self.p.act(self.file_, self.enter, 'VISA', 'input#CreditCard_name')
                self.p.act(self.file_, self.enter, str(data[self.creditcardnumber]).replace(' ', ''),
                           'input#CreditCard_cardNumber', '', 0)
                self.p.act(self.file_, self.enter, '1219', 'input#CreditCard_expDate', '', 0)
                self.p.act(self.file_, self.enter, data[self.creditcardzip], 'input#billingzipcode', '', 0)
                self.p.act(self.file_, self.click, 'Save button', 'input#cardPay')
                self.p.act(self.file_, self.pause, '3', 'seconds')
                self.p.act(self.file_, self.verify, 'Displayed: Credit Card successfully validated.',
                       'h4[data-code*="Payment.CreditCard.Message"]', '', 0)
            # else:
            #     """TBD"""
            #     print 'tbd'
            self.p.act(self.file_, self.click, 'Continue', self.elmnt_uho_continue_bttn)
            self.p.act(self.file_, self.wait, 'Uho Loading...', self.elmnt_uho_loading_img)
            break

    def review_submit_section(self):
        self.p.act(self.file_, self.verify, 'Displayed: Review and Submit page',
                   self.elmnt_uho_review_submit_header_page, '', 1)
        # for plan in base.ts_data['plans']:
        #     if self.plan_hpg in plan:
        #         self.p.act(self.file_, self.click, self.plan_hpg + ' checkbox', '<uho_esignature_def_chckbox>', '', 0)
        #     elif self.plan_stm in plan:
        #         self.p.act(self.file_, self.click, self.plan_stm + ' checkbox', '<uho_esignature_def_chckbox>')
        #         fact = self.p.get_attrib_from_notes(base.ts_data['plans'], base.ts_data['plandict'], 'fact')
        #         if fact:
        #             self.p.act(self.file_, self.click, 'FACT checkbox', '<uho_esignature_fact_chckbox>', '', 0)
        #     elif self.plan_dental in plan:
        #         self.p.act(self.file_, self.click, self.plan_dental + ' checkbox', '<uho_esignature_denta_chckbox>', '', 0)
        #     elif self.plan_vision in plan:
        #         self.p.act(self.file_, self.click, self.plan_vision + ' checkbox', '<uho_esignature_vision_chkbox>', '', 0)
        #     elif self.plan_critical in plan:
        #         self.p.act(self.file_, self.click, self.plan_critical + ' checkbox', '<uho_esignature_critical_chckbox>', '', 0)
        #     elif self.plan_asg in plan:
        #         self.p.act(self.file_, self.click, self.plan_asg + ' checkbox', '<uho_esignature_accident_chckbox>', '', 0)
        #     elif self.plan_tl in plan:
        #         self.p.act(self.file_, self.click, self.plan_tl + ' checkbox', '<uho_esignature_term_life_chckbox>', '', 0)
        #     elif self.plan_hsg in plan:
        #         self.p.act(self.file_, self.click, self.plan_hsg + ' checkbox',
        #                    '<uho_esignature_supplemental_indemnity_chckbox>', '', 0)
        #     elif self.plan_ihc in plan:
        #         self.p.act(self.file_, self.click, self.plan_ihc + ' checkbox', '<uho_esignature_hospital_chckbox>', '', 0)
        i = 0
        for plan in base.ts_data['plans']:
            if self.plan_hpg in plan:
                self.p.act(self.file_, self.click, self.plan_hpg + ' checkbox',
                           self.elmnt_uho_e_signature + str(i) + self.gt, '', 1)
                i += 1
            elif self.plan_stm in plan:
                self.p.act(self.file_, self.click, self.plan_stm + ' checkbox',
                           self.elmnt_uho_e_signature + str(i) + self.gt)
                fact = self.p.get_attrib_from_notes(base.ts_data['plans'], base.ts_data['plandict'], 'fact')
                if fact:
                    self.p.act(self.file_, self.click, 'FACT checkbox', self.elmnt_uho_e_signature_fact, '', 1)
                i += 1
            elif self.plan_dental in plan \
                    or plan in ['Essential', 'Primary', 'Essential Preferred', 'Primary Plus', 'Primary Preferred',
                                'Premier Choice', 'Premier Elite', 'Premier Plus', 'Premier Max',
                                'Primary Preferred Plus']:
                self.p.act(self.file_, self.click, self.plan_dental + ' checkbox',
                           self.elmnt_uho_e_signature + str(i) + self.gt, '', 1)
                i += 1
            elif self.plan_vision in plan:
                self.p.act(self.file_, self.click, self.plan_vision + ' checkbox',
                           self.elmnt_uho_e_signature + str(i) + self.gt, '', 1)
                i += 1
            elif self.plan_critical in plan:
                self.p.act(self.file_, self.click, self.plan_critical + ' checkbox',
                           self.elmnt_uho_e_signature + str(i) + self.gt, '', 1)
                i += 1
            elif self.plan_asg in plan:
                self.p.act(self.file_, self.click, self.plan_asg + ' checkbox',
                           self.elmnt_uho_e_signature + str(i) + self.gt, '', 1)
                i += 1
            elif self.plan_tl in plan:
                self.p.act(self.file_, self.click, self.plan_tl + ' checkbox',
                           self.elmnt_uho_e_signature + str(i) + self.gt, '', 1)
                i += 1
            elif self.plan_hsg in plan:
                self.p.act(self.file_, self.click, self.plan_hsg + ' checkbox',
                           self.elmnt_uho_e_signature + str(i) + self.gt, '', 1)
                i += 1
            elif self.plan_ihc in plan:
                self.p.act(self.file_, self.click, self.plan_ihc + ' checkbox',
                           self.elmnt_uho_e_signature + str(i) + self.gt, '', 1)
                i += 1
        for i, applicant in enumerate(base.ts_data['applicants']):
            if i > 1:
                break
            elif applicant not in ['nan', None, ' ']:
                for plan in base.ts_data['plans']:
                    if page.has_signature_checkbox(base.ts_data['zipcode'], plan, i):
                        self.p.act(self.file_, self.click, 'Applicant Signature ' + str(i + 1),
                                   self.elmnt_uho_app_e_signature_bttn + str(i + 1) + self.gt, '', 1)
                        break
        self.p.act(self.file_, self.click, 'submit your application', self.elmnt_uho_continue_bttn, '', 1)

    def thank_you_section(self):
        self.p.act(self.file_, self.wait, 'Uho Loading...', self.elmnt_uho_loading_img)
        self.p.act(self.file_, self.wait, 'Uho Loading...', self.elmnt_uho_loading_img)
        self.p.act(self.file_, self.verify, 'Displayed: Thank you page', self.elmnt_uho_thank_you_page, 'm-', 0)

    def sort_question_page(self, plans):
        plan_list = list()
        plan_dict = dict()
        plan_index = dict()
        if len(plans) > 1:
            for i, plan in enumerate(plans):
                if self.plan_hpg in plan or self.plan_ihc in plan:
                    plan_dict[0] = plan
                elif self.plan_stm in plan:
                    plan_dict[1] = plan
                elif self.plan_dental in plan or self.plan_dental_plus in plan:
                    plan_dict[2] = plan
                elif self.plan_critical in plan:
                    plan_dict[3] = plan
                elif self.plan_asg in plan:
                    plan_dict[4] = plan
                elif self.plan_vision in plan:
                    plan_dict[5] = plan
                elif self.plan_hsg in plan:
                    plan_dict[6] = plan
                elif self.plan_tl in plan:
                    plan_dict[7] = plan
                elif self.plan_disability in plan:
                    plan_dict[8] = plan
                plan_index[plan] = i+1
            keys = list(plan_dict.keys())
            keys.sort()
            for i, key in enumerate(keys):
                plan_list.insert(i, plan_dict[key])
                plans.remove(plan_dict[key])
                break
            for i, plan in enumerate(plans):
                plan_list.insert(i+1, plan)
            base.ts_data['plans'] = plan_list
        else:
            plan_list = plans
            plan_index[plans[0]] = 1
        return plan_list, plan_index
