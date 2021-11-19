import os
import src.lib.base as base

from src.lib.prep import Prep as prep
from src.lib.prep import Auxiliary
from src.lib.fmanager import FileFolderManager

f = FileFolderManager()
page = Auxiliary()


class _BAA(prep):
    def __init__(self):
        prep.__init__(self)

    def to_baa(self):
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

        # Create test case file using self.tcname value with .csv extension
        csv_file = os.path.join(os.path.join(f.workingdir, base.ts_data['tsname']), base.ts_data['tcname'] + ".csv")
        try:
            self.file_ = open(csv_file, 'w')
        except (PermissionError, FileNotFoundError):
            return ['of', 'the', 'Jedi!']

        """PAGE FLOW SECTION"""
        self.intro_section()
        self.welcome_brokers_section()
        self.welcome_e_store_section()
        self.broker_census_section()
        self.plan_compare_section()
        self.prospect_information_section()
        self.applicant_info_section()
        self.question_section()
        self.summary_section()
        self.payment_section(base.ts_data['data'])
        self.baa_finish_section()
        # self.app_verification_section()
        self.file_.close()
        return self.p.actline

    def intro_section(self):
        self.p.act(self.file_, self.testname, base.ts_data['tcname'], '')
        self.p.act(self.file_, self.description, base.ts_data['desc'], '')
        self.p.act(self.file_, self.type, base.ts_data['type'], '')
        self.p.act(self.file_, self.url, base.ts_data['uri'], '<uho_title_baa>')

    def welcome_brokers_section(self):
        self.p.act(self.file_, self.enter, base.ts_data['brokerid'], '<uho_broker_id_fld>')
        self.p.act(self.file_, self.enter, base.ts_data['brokerpwd'], '<uho_broker_password_fld>')
        self.p.act(self.file_, self.click, 'Sign In', '<uho_broker_sign_in_bttn>')

    def welcome_e_store_section(self):
        self.p.act(self.file_, self.click, 'Get an Instant Quote', '<uho_get_instant_quote_bttn>')

    def broker_census_section(self):
        self.p.act(self.file_, self.enter, base.ts_data['zipcode'], self.elmnt_zipcode)
        self.p.act(self.file_, self.pause, '5', 'seconds')
        """for zipcode with county input"""
        if page.has_county_selection(base.ts_data['zipcode']):
            self.p.act(self.file_, self.select, 'County: ' + base.ts_data['county'], self.elmnt_county)
        for i, applicant in enumerate(base.ts_data['applicants']):
            if applicant == 'nan':
                continue
            self.p.act(self.file_, self.select, 'Applicant: ' + applicant,
                       self.elmnt_uho_app_gendr_lst + str(i+1) + self.gt)
            self.p.act(self.file_, self.enter, str(base.ts_data['applicantsdob'][i]),
                       self.elmnt_uho_app_dob_fld + str(i+1) + self.gt, '', 0)
            if str(base.ts_data['applicantstobacco'][i]) == 'nan':
                self.p.act(self.file_, self.select, 'Tobacco: No', self.elmnt_uho_app_tobacco_lst + str(i+1) + self.gt)
            else:
                self.p.act(self.file_, self.select, 'Tobacco: ' + str(base.ts_data['applicantstobacco'][i]),
                           self.elmnt_uho_app_tobacco_lst + str(i + 1) + self.gt)
        # self.p.act(self.file_, self.click, 'zipcode field', self.elmnt_zipcode)
        for plan in base.ts_data['plans']:
            if self.plan_stm in plan:
                plan = str(plan).replace(self.plan_stm, 'Short Term Medical')
            elif self.plan_hpg in plan:
                if 'Plan' in plan:
                    plan = str(plan).replace(' - Plan', '')
                elif 'Choice Value' in plan:
                    plan = self.plan_hpg + ' Simplified A'
                elif 'Choice Plus' in plan:
                    plan = self.plan_hpg + ' Simplified B'
                elif 'Select Value' in plan:
                    plan = self.plan_hpg + ' Simplified C'
                elif 'Select Plus' in plan:
                    plan = self.plan_hpg + ' Simplified D'
                elif 'Premier Plus' in plan:
                    plan = self.plan_hpg + ' Simplified E'
            elif self.plan_vision in plan:
                plan = str(plan).replace(' -', '')
            elif self.plan_dental_plus in plan:
                plan = str(plan).replace('+', '')
            elif self.plan_supplemental in plan:
                if 'Fixed Indemnity Policy - $500' in plan:
                    plan = 'Hospital SafeGuard Premier Plan A'
                elif 'Fixed Indemnity Policy - $1' in plan:
                    plan = 'Hospital SafeGuard Premier Plan B'
                elif 'Confinement Indemnity Policy - $1' in plan:
                    plan = 'Hospital SafeGuard Plan A'
                elif 'Confinement Indemnity Policy - $2' in plan:
                    plan = 'Hospital SafeGuard Plan B'
            elif self.plan_disability in plan:
                continue
            self.p.act(self.file_, self.click, plan, 'input[value*=\'' + plan + '\']')
        self.p.act(self.file_, self.click, 'View Plans', self.elmnt_uho_view_plans_bttn)

    def plan_compare_section(self):
        self.p.act(self.file_, self.verify, 'Displayed:Plan Compare page', 'form#frmPlanCompare')
        tab = ' tab'
        hospital = 'Hospital & Doctor'
        ancillary = 'Vision and More'
        ancillary2 = 'More Coverage'
        for i, plan in enumerate(base.ts_data['plans']):
            if self.plan_stm in plan:
                plan = str(plan).replace(self.plan_stm, 'Short Term Medical')
                self.p.act(self.file_, self.click, self.plan_stm + tab, self.elmnt_uho_stm_tab)
                # 12/15 release: added if 'STM Copay Select A' in plan:
                if 'Short Term Medical Copay Select A' in plan:
                    self.p.act(self.file_, self.click, 'Page 3', 'a[data-gtm-id*=Pagination3]')
                self.p.act(self.file_, self.click, plan + ' Add to Cart', self.elmnt_uho_add_to_cart)
            elif self.plan_ihc in plan:
                self.p.act(self.file_, self.click, hospital + tab, self.elmnt_uho_hospital_tab)
                self.p.act(self.file_, self.click, plan + ' Add to Cart', self.elmnt_uho_add_to_cart)
            elif self.plan_hpg in plan:
                self.p.act(self.file_, self.click, hospital + tab, self.elmnt_uho_hospital_tab)
                self.p.act(self.file_, self.click, plan + ' Add to Cart', self.elmnt_uho_add_to_cart)
            elif self.plan_dental in plan:
                self.p.act(self.file_, self.click, self.plan_dental + tab, self.elmnt_uho_dental_tab)
                self.p.act(self.file_, self.click, plan + ' Add to Cart', self.elmnt_uho_add_to_cart)
            elif self.plan_apg in plan or self.plan_aeg in plan:
                self.p.act(self.file_, self.click, self.plan_apg + tab, self.elmnt_uho_accident_pro)
                self.p.act(self.file_, self.click, plan + ' Add to Cart', self.elmnt_uho_add_to_cart)
            elif self.plan_asg in plan:
                self.p.act(self.file_, self.click, self.plan_asg + tab, self.elmnt_uho_accident_tab)
                self.p.act(self.file_, self.click, plan + ' Add to Cart', self.elmnt_uho_add_to_cart)
            elif self.plan_critical in plan:
                self.p.act(self.file_, self.click, self.plan_critical + tab, self.elmnt_uho_crit_illness_tab)
                self.p.act(self.file_, self.click, plan + ' Add to Cart', self.elmnt_uho_add_to_cart)
            else:
                ancillary_tab = page.has_ancillary_tab(base.ts_data['state'], base.ts_data['type'])
                if ancillary_tab == 'visionandmore' and len(base.ts_data['plans']) > 1:
                # if page.has_ancillary_tab(base.ts_data['zipcode'], base.ts_data['type'], plan) and len(
                #         base.ts_data['plans']) > 1:
                    self.p.act(self.file_, self.click, ancillary + tab, self.elmnt_uho_ancillary_tab, m='m-')
                    # MOBILE SPECIFIC STEP
                    self.p.act(self.file_, self.click, ancillary + tab, '<uho_plan_menu_vision_and_more>', m='m')
                    uho_plan_menu_more_vision = '<uho_plan_menu_more_vision>'
                    uho_plan_menu_more_supplemental = '<uho_plan_menu_more_supplemental>'
                    uho_plan_menu_more_term_life = '<uho_plan_menu_more_term_life>'
                    uho_plan_menu_more_discount_card = '<uho_plan_menu_more_discount_card>'
                elif ancillary_tab == 'morecoverage' and len(base.ts_data['plans']) > 1:
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
                if self.plan_vision in plan:
                    self.p.act(self.file_, self.click, 'Vision tab', self.elmnt_uho_vision_tab, m='m-')
                    # MOBILE SPECIFIC STEP
                    self.p.act(self.file_, self.click, 'Vision tab', uho_plan_menu_more_vision, m='m')
                    self.p.act(self.file_, self.click, plan + ' Add to Cart', self.elmnt_uho_add_to_cart)
                elif self.plan_hsg in plan:
                    self.p.act(self.file_, self.click, self.plan_hsg + tab, self.elmnt_uho_supplemental_tab, m='m-')
                    # MOBILE SPECIFIC STEP
                    self.p.act(self.file_, self.click, self.plan_hsg + tab, uho_plan_menu_more_supplemental, m='m')
                    self.p.act(self.file_, self.click, plan + ' Add to Cart', self.elmnt_uho_add_to_cart)
                elif self.plan_tl in plan:
                    self.p.act(self.file_, self.click, self.plan_tl + tab, self.elmnt_uho_term_life_tab, m='m-')
                    # MOBILE SPECIFIC STEP
                    self.p.act(self.file_, self.click, self.plan_tl + tab, uho_plan_menu_more_term_life, m='m')
                    self.p.act(self.file_, self.click, plan + ' Add to Cart', self.elmnt_uho_add_to_cart)
                elif self.plan_discount in plan:
                    self.p.act(self.file_, self.click, self.plan_discount + tab, self.elmnt_uho_discount_tab, m='m-')
                    # MOBILE SPECIFIC STEP
                    self.p.act(self.file_, self.click, self.plan_discount + tab, uho_plan_menu_more_discount_card, m='m')
                    self.p.act(self.file_, self.click, plan + ' Add to Cart button', self.elmnt_uho_add_to_cart)
                elif self.plan_disability in plan:
                    continue
                    # plan = str(plan).replace(self.plan_disability, 'Disability Income')
                    # self.p.act(self.file_, self.click, self.plan_disability + tab, self.elmnt_uho_disability_tab)
                    # self.p.act(self.file_, self.click, plan + ' Add to Cart', self.elmnt_uho_add_to_cart)
        self.p.act(self.file_, self.click, 'Start Broker Assisted App', '<uho_start_baa_bttn>')
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

    def prospect_information_section(self):
        self.p.act(self.file_, self.verify, 'Expected:Prospect Information', '<uho_prospect_information_lbl>')
        self.p.act(self.file_, self.enter, base.ts_data['primaryfname'], '<uho_firstname_fld>')
        self.p.act(self.file_, self.enter, base.ts_data['primarylname'], '<uho_lastname_fld>')
        self.p.act(self.file_, self.enter, self.applicantgmailadd, '<uho_primary_email_address_fld>')
        self.p.act(self.file_, self.enter, self.applicantphonenum, '<uho_prospect_phone_fld>')
        self.p.act(self.file_, self.enter, self.applicantaddress, '<uho_address_line1_fld>')
        self.p.act(self.file_, self.enter, base.ts_data['county'], '<uho_city_fld>')
        self.p.act(self.file_, self.select, 'State:' + base.states[base.ts_data['state']], '<uho_state_lst>')
        self.p.act(self.file_, self.enter, base.ts_data['zipcode'], '<uho_pi_zip_code_fld>')
        self.p.act(self.file_, self.click, 'Save and Continue', '<uho_save_and_continue_bttn>')

    def applicant_info_section(self):
        self.p.act(self.file_, self.verify, 'Displayed: Applicant information page',
                   self.elmnt_uho_app_info_header_page, '', 0)
        for i, applicant in enumerate(base.ts_data['applicants']):
            if applicant in ['nan', None, ' ']:
                continue
            self.p.act(self.file_, self.enter, self.applicantfname[i],
                       self.elmnt_uho_app_fname_fld + str(i+1) + self.gt, '', 0)
            self.p.act(self.file_, self.enter, self.applicantlname,
                       self.elmnt_uho_app_lname_fld + str(i+1) + self.gt, '', 0)
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
            # if self.plan_critical in plan or self.plan_asg in plan or self.plan_hsg in plan or self.plan_tl in plan:
            #     self.p.act(self.file_, self.enter, self.applicantbeneficiary, self.elmnt_uho_beneficiary_fname_fld, '', 0)
            #     self.p.act(self.file_, self.enter, self.applicantlname, self.elmnt_uho_beneficiary_lname_fld, '', 0)
            #     self.p.act(self.file_, self.enter, self.applicantrelationship, self.elmnt_uho_beneficiary_relationship_fld,
            #                '', 0)
            #     self.p.act(self.file_, self.enter, self.applicantbeneficiaryage, self.elmnt_uho_beneficiary_age_fld, '', 0)
            # elif self.plan_disability in plan:
            #     continue
                # self.p.act(self.file_, self.enter, self.applicantoccupation, self.elmnt_uho_emp_occupation_fld, '', 0)
                # self.p.act(self.file_, self.enter, 'UHG', self.elmnt_uho_emp_employer_name_fld, '', 0)
                # self.p.act(self.file_, self.enter, 'Developer', self.elmnt_uho_emp_duties_fld, '', 0)
                # self.p.act(self.file_, self.select, 'Year:1-5 years',
                #            self.elmnt_uho_emp_occupation_length_fld, '', 0)
                # self.p.act(self.file_, self.enter, self.applicantaddress, self.elmnt_uho_emp_employer_address_fld, '', 0)
                # self.p.act(self.file_, self.enter, self.applicantcity, self.elmnt_uho_emp_employer_city_fld, '', 0)
                # self.p.act(self.file_, self.select, 'State:' + base.ts_data['state'], self.elmnt_uho_emp_employer_state_fld,
                #            '', 0)
                # self.p.act(self.file_, self.enter, base.ts_data['zipcode'], self.elmnt_uho_emp_employer_zipcode_fld, '', 0)
                # self.p.act(self.file_, self.click, 'Non-Business Owner',
                #            self.elmnt_uho_emp_nonbusiness_owner_fld, '', 0)
                # self.p.act(self.file_, self.enter, '5000', self.elmnt_uho_emp_nonbusiness_monthly_fld, '', 0)
                # self.p.act(self.file_, self.click, 'No', self.elmnt_uho_emp_nonbusiness_no_bttn,
                #            '', 0)
                # self.p.act(self.file_, self.enter, '50000', self.elmnt_uho_emp_nonbusiness_annual_fld, '', 0)
        # self.p.act(self.file_, self.click, 'Continue', self.elmnt_uho_continue_bttn)
        self.p.act(self.file_, self.click, 'Continue', self.elmnt_uho_continue_bttn)
        self.p.act(self.file_, self.verify, 'Displayed: Resident Physical Address error',
                   '<uho_address_mismatch_error>')
        self.p.act(self.file_, self.verify, '\" Displayed: \"\"Suggested Address:\"\"\"', '<uho_suggested_address_lbl>')
        self.p.act(self.file_, self.click, 'Use This Address button', '<uho_use_this_address>')
        self.p.act(self.file_, self.click, 'Continue', self.elmnt_uho_continue_bttn)
        # if page.has_registration_pop_up(base.ts_data['zipcode']):
        #     self.p.uho_registration_dialog(self.file_)

    def question_section(self):
        plan_list, plan_index = self.sort_question_page(base.ts_data['plans'])
        for i, plan in enumerate(plan_list):
            """for zipcode with or without question page"""
            question = str(base.ts_data['plandict'][plan][self.plan + str(plan_index[plan])
                                                          + self.planappquestions]).lower().strip()
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
                    # self.p.act(self.file_, self.select, 'Questions: all no', self.elmnt_uho_question_all_no_bttn)
                    self.p.act(self.file_, self.select, 'Questions: all no', 'a[role=radio][id*=\'_No\']')
                    self.p.act(self.file_, 'Pause', '3', 'Seconds')
                    if question == '1 yes':
                        # for 12/15/2017 release ###
                        if self.plan_dental in plan:
                            self.p.act(self.file_, self.click, 'Question: 1 YES',
                                       self.elmnt_uho_question_one_yes_bttn)
                        else:
                            self.p.act(self.file_, self.click, 'Question: 1 YES',
                                       self.elmnt_uho_question_one__yes_bttn)
                        if base.ts_data['applicantsnum'] > 1 and self.plan_dental not in plan:
                            self.p.act(self.file_, self.click, 'Applicant: Primary',
                                       self.elmnt_uho_question_primary_response_bttn)
                        if self.plan_asg in plan:
                            self.p.act(self.file_, self.enter, 'Carrier', self.elmnt_uho_question_carrier_fld)
                            if base.ts_data['zipcode'] in ['72718', '31050']:
                                self.p.act(self.file_, self.enter, 'Coverage', self.elmnt_uho_question_policy_fld)
                            else:
                                self.p.act(self.file_, self.enter, 'Coverage', self.elmnt_uho_question_coverage_fld)
                        elif self.plan_hsg in plan:
                            self.p.act(self.file_, self.enter, 'Carrier', self.elmnt_uho_question_carrier_fld)
                            self.p.act(self.file_, self.enter, '1357913579', self.elmnt_uho_question_policy_fld)
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
                # self.p.act(self.file_, self.click, 'Continue', self.elmnt_uho_continue_bttn)
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
                self.p.act(self.file_, self.click, str(plan) + ' Edit Button', form + str(i + 1) + edit)
                self.p.act(self.file_, self.enter, coverage_startdate, input_ + str(i) + coverage_sdate)
                self.p.act(self.file_, self.enter, coverage_startdate, input_ + str(i) + coverage_sdate)
                self.p.act(self.file_, self.click, str(plan) + ' Save Changes Button', form + str(i + 1) + save)
        ##### self.p.act(self.file_, 'compare', 'base premium rate', '.mc-review-subheader-container:nth-child(3) .col-xs-3')
        self.p.act(self.file_, self.click, 'Continue', self.elmnt_uho_continue_bttn)

    def payment_section(self, data):
        self.p.act(self.file_, self.verify, 'Displayed: Payment Type header', self.elmnt_uho_payment_type_header_page, 
                   '', 0)
        for i, plan in enumerate(base.ts_data['plans']):
            payment_type = base.ts_data['plandict'][plan][self.plan + str(i+1) + self.planpaymenttype]
            if 'EFT' in payment_type:
                self.p.act(self.file_, self.click, payment_type, self.elmnt_uho_payment_eft_bttn, '', 0)
                # self.p.act(self.file_, self.click, 'Continue', self.elmnt_uho_continue_bttn)
                self.p.act(self.file_, self.click, 'Continue', self.elmnt_uho_continue_bttn)
                self.p.act(self.file_, self.click, 'Checking', self.elmnt_uho_payment_checking_bttn, '', 0)
                # if len(data[self.eftroutingnumber]) < 9:
                #     data[self.eftroutingnumber] = '0' + data[self.eftroutingnumber]
                # self.p.act(self.file_, self.enter, data[self.eftroutingnumber], '#routingNumber', '', 0)
                # self.p.act(self.file_, self.enter, data[self.eftaccountnumber], '#bankAccountNumber', '', 0)
                self.p.act(self.file_, self.enter, self.eftroutingnum, self.elmnt_uho_payment_eft_routing_fld, '', 0)
                self.p.act(self.file_, self.enter, self.eftaccountnum, self.elmnt_uho_payment_eft_account_fld, '', 0)
            # elif payment_type == 'Credit Card':
            else:
                # print('do nothing john snow!')
                self.p.act(self.file_, self.click, payment_type, self.elmnt_uho_payment_cc_bttn, '', 0)
                # self.p.act(self.file_, self.click, 'Continue', self.elmnt_uho_continue_bttn)
                # self.p.act(self.file_, self.enter, str(data[self.creditcardnumber]).replace(' ', ''),
                #            self.elmnt_uho_payment_cc_number_fld, '', 0)
                # self.p.act(self.file_, self.enter, data[self.creditcardzip], self.elmnt_uho_payment_cc_zipcode_fld, '', 0)
                # self.p.act(self.file_, self.select, self.creditcardexpmonth, self.elmnt_uho_payment_cc_expiry_month_lst, '', 0)
                # self.p.act(self.file_, self.select, self.creditcardexpyear, self.elmnt_uho_payment_cc_expiry_year_lst, '', 0)
                # self.p.act(self.file_, self.select, self.creditcardexpday, self.elmnt_uho_payment_cc_expiry_day_lst, '', 0)
            self.p.act(self.file_, self.click, 'Continue', self.elmnt_uho_continue_bttn)
            break

    def baa_finish_section(self):
        self.p.act(self.file_, self.verify, 'Displayed: Broker Assisted Application Finish page',
                   'h1[data-code*=BrokerFinish]', '', 0)
        self.p.act(self.file_, self.click, 'Continue', 'button[type=submit][data-ng-click*=saveProspect]')
        self.p.act(self.file_, self.verify, 'Displayed: Your application has been successfully sent',
                   '.mc-alert-success-header [data-code*=SendProspectConfirmation]')
        self.p.act(self.file_, self.pause, '5', 'seconds')

    def app_verification_section(self):
        # self.p.act(self.file_, self.verify, 'Displayed: Application Verification', '.row.contentRow h3',
        #            '', 0)
        self.p.act(self.file_, self.enter, self.applicantlname, 'input#LastName')
        self.p.act(self.file_, self.enter, str(base.ts_data['applicantsdob'][0]), 'input#BirthDatePicker')
        self.p.act(self.file_, self.click, 'Continue', 'input#idContinue')

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
                plan_index[plan] = i + 1
            keys = list(plan_dict.keys())
            keys.sort()
            for i, key in enumerate(keys):
                plan_list.insert(i, plan_dict[key])
                plans.remove(plan_dict[key])
                break
            for i, plan in enumerate(plans):
                plan_list.insert(i + 1, plan)
            base.ts_data['plans'] = plan_list
        else:
            plan_list = plans
            plan_index[plans[0]] = 1
        return plan_list, plan_index
