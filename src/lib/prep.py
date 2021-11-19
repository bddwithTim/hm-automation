class Prep(object):
    def __init__(self):
        """test plan spreadsheet column/header names"""
        # ##################################################
        # Test plan spreadsheet column/header names
        # ##################################################
        self.testcasenumber = 'test case\n#'  # fix
        self.plansintestcase = 'plans in this test case'  # fix
        self.state = 'state'  # fix
        self.zipcounty = 'zip/county'  # in
        self.testcasetype = 'test case type'  # fix
        self.brokerid = 'broker'  # fix
        self.brokerpwd = 'broker password'  # fix
        self.primarygender = 'primary gender'  # fix
        self.primarydob = 'primary dob'  # fix
        self.primarytobacco = 'primary tobacco'  # fix
        self.spousegender = 'spouse gender'  # fix
        self.spousedob = 'spouse dob'  # fix
        self.spousetobacco = 'spouse tobacco'  # fix
        self.dependentgender = ' gender'  # in
        self.dependentdob = ' dob'  # in
        self.dependenttobacco = ' tobacco'  # in
        self.quotecartplan = 'quote cart plan'  # in
        self.plan = 'plan #'  # make this fix and just append the number
        self.plancoveragestartdate = ' coverage start date'  # in
        self.plancoverageenddate = ' coverage end date'  # in
        self.planmaxduration = ' max duration'  # in
        self.plandeductiblecoinsurance = ' deductible & coinsurance'  # in
        self.plandeductibletype = ' deductible type'  # in
        self.planotheroptions = ' other options'  # in
        self.planappquestions = ' app questions'  # in
        self.planpaymenttype = ' payment type'  # in
        self.plannotes = ' notes for testing'     # in
        self.planappnumber = ' app #'  # in
        self.planbrochurenumber = ' brochure #'  # in
        self.eftroutingnumber = 'eft routing number'  # fix
        self.eftaccountnumber = 'eft account number'  # fix
        self.creditcardtype = 'credit card type'  # fix
        self.creditcardnumber = 'credit card number'  # fix
        self.creditcardexpdate = 'credit card exp date'  # fix
        self.creditcardzip = 'credit card zip'  # fix
        self.fox = 'THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG!!!'

        # ##################################################
        # Plan terms
        # ##################################################
        self.plan_tl = 'Term Life'
        self.plan_stm = 'STM'
        # self.plan_asg = 'Accident Safeguard'
        self.plan_asg = 'Accident'
        self.plan_apg = 'Accident Pro'
        self.plan_aeg = 'Accident Expense'
        self.plan_hpg = 'Health ProtectorGuard'
        self.plan_hsg = 'Hospital'  # SafeGuard
        self.plan_dental = 'Dental'
        self.plan_vision = 'Vision'
        self.plan_discount = 'Discount'
        self.plan_disability = 'Disability'
        self.plan_critical = 'Critical'
        self.plan_ihc = 'Core Access'
        self.plan_dental_plus = 'Dental 50+'
        self.plan_supplemental = 'Supplemental'

        # ##################################################
        # Variable declarations
        # ##################################################
        self.testname = None
        self.desc = None
        self.type = None
        self.url = None
        self.paymentdict = dict()
        self.line = list()
        self.coveragestart = list()
        self.coverageend = list()
        self.has_ssn = False
        self.applicantfname = ['Primary', 'Spouse', 'Dependent One', 'Dependent Two']
        self.applicantlname = 'Dela Cruz'
        self.applicantgender = ['Male', 'Female']
        self.applicantdob = ['12/12/1982', '01/01/1981']
        self.applicanttobacco = ['Yes', 'No']
        self.applicantheightft = ['5', '5']
        self.applicantheightin = ['8', '7']
        self.applicantweightlbs = ['170', '160']
        self.applicantemailadd = 'wcamposo@unitedhealthone.com'
        self.applicantgmailadd = 'uhonetesting@gmail.com'
        self.applicantphonenum = '9333333333'
        self.applicantoccupation = 'Engineer'
        self.applicantaddress = 'General Delivery'
        self.applicantcity = 'City of Angels'
        self.applicantbeneficiary = 'John'
        self.applicantrelationship = 'Nephew'
        self.applicantbeneficiaryage = '18'
        self.creditcardexpmonth = 'month: 04'
        self.creditcardexpyear = 'year: 2019'
        self.creditcardexpday = 'day: 1'
        self.ssn = '135791357'
        self.eftroutingnum = '074000010'
        self.eftaccountnum = '123456789'
        self.lt = '<'
        self.gt = '>'
        self.comma = ','
        self.pipe = ' | '

        # ##################################################
        # Broker variables
        # ##################################################
        # self.brokerpsswd

        # ##################################################
        # Action variables
        # ##################################################
        self.testname = 'Testname'
        self.description = 'Description'
        self.type = 'Type'
        self.url = 'URL'
        self.release = 'Release'
        self.enter = 'Enter'
        self.select = 'Select'
        self.click = 'Click'
        self.check = 'Check'
        self.choose = 'Choose'
        self.verify = 'Verify'
        self.wait = 'Wait'
        self.pause = 'Pause'
        self.switch = 'Switch'

        # ##################################################
        # Element variables
        # ##################################################
        # self.elmnt_zipcode = '<zip_code_fld>'
        self.elmnt_zipcode = '<ghi_zip_code_fld>'
        # self.elmnt_county = '<uho_county_fld>'
        self.elmnt_county = '<ghi_county_fld>'
        # self.elmnt_uho_app_gendr_lst = '<uho_applicant_gender_list_'
        self.elmnt_uho_app_gendr_lst = '<applicant_gender_list_'
        # self.elmnt_uho_app_dob_fld = '<uho_applicant_dob_field_'
        self.elmnt_uho_app_dob_fld = '<applicant_dob_field_'
        # self.elmnt_uho_app_tobacco_lst = '<uho_applicant_tobacco_list_'
        self.elmnt_uho_app_tobacco_lst = '<applicant_tobacco_list_'
        # self.elmnt_uho_view_plans_bttn = '<view_plans_bttn>'
        self.elmnt_uho_view_plans_bttn = '<ghi_view_plans_bttn>'
        self.elmnt_uho_stm_tab = '<uho_short_term_tab>'
        self.elmnt_uho_hospital_tab = '<uho_hospital_doctor_tab>'
        self.elmnt_uho_dental_tab = '<uho_dental_tab>'
        self.elmnt_uho_vision_tab = '<uho_vision_tab>'
        self.elmnt_uho_discount_tab = '<uho_discount_tab>'
        self.elmnt_uho_accident_tab = '<uho_accident_tab>'
        self.elmnt_uho_accident_pro = '<uho_accident_pro>'
        self.elmnt_uho_term_life_tab = '<uho_term_life_tab>'
        self.elmnt_uho_ancillary_tab = '<uho_ancillary_tab>'
        self.elmnt_uho_ancillary_tab2 = '<uho_ancillary_tab2>'
        self.elmnt_uho_disability_tab = '<uho_disability_tab>'
        self.elmnt_uho_supplemental_tab = '<uho_supplemental_tab>'
        self.elmnt_uho_crit_illness_tab = '<uho_critical_illness_tab>'
        self.elmnt_uho_plan_lst = '<plan_list>'
        self.elmnt_uho_add_to_cart = '<add_to_cart>'
        # self.elmnt_uho_plan_name_lbl = '<plan_name_lbl>'
        self.elmnt_uho_plan_name_lbl = '<ghi_plan_name>'
        self.elmnt_uho_apply_bttn = '<apply_bttn>'
        self.elmnt_uho_shopping_cart_page = '<uho_shopping_cart_page>'
        self.elmnt_uho_modal_65_dlg = 'div#dialogAgeRule'
        self.elmnt_uho_modal_65_continue_bttn = 'button#btnAgeRuleContinue'
        self.elmnt_uho_app_info_header_page = '<uho_applicant_info_header_ar>'
        self.elmnt_uho_question_header_page = '<uho_question_page_header>'
        self.elmnt_uho_payment_summary_header_page = '<uho_payment_summary_header>'
        self.elmnt_uho_payment_type_header_page = '<uho_payment_type_header>'
        self.elmnt_uho_review_submit_header_page = '<uho_review_and_submit_header>'
        self.elmnt_uho_app_fname_fld = '<uho_applicant_fname_field_'
        self.elmnt_uho_app_lname_fld = '<uho_applicant_lname_field_'
        self.elmnt_uho_app_marital_fld = '<uho_marital_status_'
        self.elmnt_uho_app_height_ft_fld = '<uho_applicant_height_ft_field_'
        self.elmnt_uho_app_height_in_fld = '<uho_applicant_height_in_field_'
        self.elmnt_uho_app_weight_lb_fld = '<uho_applicant_weight_lbs_field_'
        self.elmnt_uho_app_driver_lcnse_fld = '<uho_driver_license_field_'
        self.elmnt_uho_app_driver_state_fld = '<uho_driver_license_state_list_1>'
        self.elmnt_uho_app_email_fld = '<uho_applicant_emailadd_field_'
        self.elmnt_uho_app_phone_fld = '<uho_applicant_phonenum_field_'
        self.elmnt_uho_app_occupation_fld = '<uho_applicant_occupation_field_'
        self.elmnt_uho_app_relationship_fld = '<uho_applicant_relationship_field_'
        self.elmnt_uho_app_ssn_fld = '<uho_applicant_ssn_field_'
        self.elmnt_uho_app_contact_info_add_fld = '<ghi_contact_info_address_fld>'
        self.elmnt_uho_app_contact_info_city_fld = '<ghi_contact_info_city_fld>'
        self.elmnt_uho_beneficiary_fname_fld = '<uho_beneficiary_fname_field>'
        self.elmnt_uho_beneficiary_lname_fld = '<uho_beneficiary_lname_field>'
        self.elmnt_uho_beneficiary_relationship_fld = '<uho_beneficiary_relationship_field>'
        self.elmnt_uho_beneficiary_age_fld = '<uho_beneficiary_age_field>'
        self.elmnt_uho_emp_occupation_fld = '<uho_emp_occupation_fld>'
        self.elmnt_uho_emp_employer_name_fld = '<uho_emp_employer_name_fld>'
        self.elmnt_uho_emp_duties_fld = '<uho_emp_duties_fld>'
        self.elmnt_uho_emp_occupation_length_fld = '<uho_emp_occupation_length_fld>'
        self.elmnt_uho_emp_employer_address_fld = '<uho_emp_employer_address_fld>'
        self.elmnt_uho_emp_employer_city_fld = '<uho_emp_employer_city_fld>'
        self.elmnt_uho_emp_employer_state_fld = '<uho_emp_employer_state_fld>'
        self.elmnt_uho_emp_employer_zipcode_fld = '<uho_emp_employer_zipcode_fld>'
        self.elmnt_uho_emp_nonbusiness_owner_fld = '<uho_emp_nonbusiness_owner_fld>'
        self.elmnt_uho_emp_nonbusiness_monthly_fld = '<uho_emp_nonbusiness_monthly_fld>'
        self.elmnt_uho_emp_nonbusiness_no_bttn = '<uho_emp_nonbusiness_no_bttn>'
        self.elmnt_uho_emp_nonbusiness_annual_fld = '<uho_emp_nonbusiness_annual_fld>'
        self.elmnt_uho_continue_bttn = '<ghi_continue_bttn>'
        self.elmnt_uho_question_all_no_bttn = '<uho_question_all_no_button>'
        self.elmnt_uho_question_one_yes_bttn = '<uho_question_one_yes_bttn>'
        self.elmnt_uho_question_one__yes_bttn = '<uho_question_one__yes_bttn>'
        self.elmnt_uho_question_primary_response_bttn = '<uho_question_primary_response_bttn>'
        self.elmnt_uho_question_carrier_fld = '<uho_question_carrier_fld>'
        self.elmnt_uho_question_policy_fld = '<uho_question_policy_fld>'
        self.elmnt_uho_question_coverage_fld = '<uho_question_coverage_fld>'
        self.elmnt_uho_question_spouse_response_bttn = '<uho_question_spouse_response_bttn>'
        self.elmnt_uho_question_dependent_one_response_bttn = '<uho_question_dependent_one_response_bttn>'
        self.elmnt_uho_question_dependent_two_response_bttn = '<uho_question_dependent_two_response_bttn>'
        self.elmnt_uho_question_replacement_yes_bttn = '<uho_question_replacement_yes_bttn>'
        self.elmnt_uho_payment_eft_bttn = '<uho_payment_type_eft>'
        self.elmnt_uho_payment_cc_bttn = '<uho_payment_type_cc>'
        self.elmnt_uho_payment_checking_bttn = '<uho_payment_account_checking>'
        self.elmnt_uho_payment_eft_routing_fld = '<ghi_accnt_routing_num_fld>'
        self.elmnt_uho_payment_eft_account_fld = '<ghi_accnt_number_fld>'
        self.elmnt_uho_payment_cc_number_fld = '<uho_credit_card_number_field>'
        self.elmnt_uho_payment_cc_zipcode_fld = '<ghi_payment_zipcode_fld>'
        self.elmnt_uho_payment_cc_expiry_month_lst = '<ghi_exp_date_month_lst>'
        self.elmnt_uho_payment_cc_expiry_year_lst = '<ghi_exp_date_year_lst>'
        self.elmnt_uho_payment_cc_expiry_day_lst = '<uho_exp_date_day_lst>'
        self.elmnt_uho_e_signature = '<uho_e_signature_'
        self.elmnt_uho_o_signature = '<uho_o_signature>'
        self.elmnt_uho_e_signature_fact = '<uho_e_signature_fact>'
        self.elmnt_uho_app_e_signature_bttn = '<uho_applicant_e-signature_bttn_'
        self.elmnt_uho_loading_img = '<uhone_loading>'
        self.elmnt_uho_thank_you_page = '<uho_thank_you_page>'


from src.lib.prep import Prep as prep


class Auxiliary(prep):
    def redirect_page(self, zipcode):
        """zipcode redirects to ghi page"""
        if zipcode in ['05050', '56372']:
            return True
        else:
            return False

    def has_county_selection(self, zipcode, kind=None):
        """for zipcode with county selections"""
        if kind == 'pa':    # for product availability auto test script generation
            zipcodes = ['71601', '83702', '46278', '59001', '97086']
        else:
            # ##################################################
            # 10/27/2017
            # 12/15/2017
            # added: ['82242', '43331', '37048', '18042', '22980', '46234', '66025', '49880', '38619', '68759',
            #         '43548', '57196', '47380', '67031']:
            # ##################################################
            z1 = ['97867', '70647', '85739', '71752', '71457', '80498', '72436', '68640', '69147', '68424', '88120',
                  '38864', '43469', '45845', '16629', '57213', '37774', '37881', '43115', '78360', '75490', '23924',
                  '54457', '54451', '53929', '54981', '26321', '71642', '30511', '30528', '83856', '62918', '47944',
                  '66854', '67530', '41219', '40464', '42256', '71107', '39470', '39325', '39145', '39756', '27565',
                  '97086', '82242', '43331', '37048', '18042', '22980', '46234', '66025', '49880', '38619', '68759',
                  '43548', '57196', '47380', '67031', '67572', '28739', '30413', '17331', '40409', '97635', '44628',
                  '38366', '55088', '58224', '56760', '55943', '48866', '67232', '30258', '31719', '23177', '33559',
                  '31033']

            # ##################################################
            # 03/09/2018
            # ##################################################
            z2 = ['50075', '38965', '80137', '37811', '61345', '49067', '27262', '16822', '80863', '34787', '54452',
                  '58301', '72501', '78121', '53017', '39629', '37806', '48451', '30645']
            # ##################################################
            # 04/06/2018
            # ##################################################
            z3 = ['72946', '43081', '28676', '46278', '74015', '45869', '43045', '48877', '63957', '63621']
            # ##################################################
            # 07/20/2018
            # ##################################################
            z4 = ['68031', '45344', '97527', '63351', '72847', '57328', '57422', '37888', '37118', '53010', '06242',
                  '39641', '32163', '31017', '50242', '38652', '61526', '61114', '47240', '42320', '48849', '36850',
                  '27244', '72852', '68845']

        zipcodes = list(set(z1 + z2 + z3 + z4))
        if zipcode in zipcodes:
            return True
        else:
            return False

    def has_height_weight_field(self, zipcode, plan='', i=0):
        if self.plan_hpg in plan or self.plan_stm in plan or self.plan_critical in plan:
            return True
        elif self.plan_tl in plan and i < 2:
            return True
        elif self.plan_hsg in plan:
            return True
        elif self.plan_ihc in plan:
            return True
        elif self.plan_disability in plan:
            return True
        elif self.plan_apg in plan:
            return True
        elif self.plan_aeg in plan:
            return True
        else:
            return False

    def has_email_field(self, zipcode, plan='', i=0):
        """for plan with email fields"""
        if (self.plan_hpg in plan or self.plan_stm in plan) and i < 2:
            return True
        elif (self.plan_apg in plan or self.plan_aeg in plan) and i < 2:
            return True
        elif (self.plan_dental in plan
              or plan in ['Essential', 'Primary', 'Essential Preferred', 'Primary Plus', 'Primary Preferred',
                          'Premier Choice', 'Premier Elite', 'Premier Plus', 'Premier Max',
                          'Primary Preferred Plus']
              or self.plan_vision in plan) and i == 0:
            return True
        elif (self.plan_asg in plan or self.plan_hsg in plan) and i == 0:
            return True
        elif self.plan_critical in plan and i == 0:
            return True
        elif self.plan_discount in plan and i == 0:
            return True
        elif self.plan_tl in plan and i == 0:
            return True
        elif self.plan_ihc in plan and i == 0:
            return True
        elif self.plan_disability in plan and i == 0:
            return True
        else:
            return False

    def has_phone_field(self, zipcode, plan='', i=0):
        """for plan with phone fields"""
        zipcode_stm = ['37774', '19966', '97022', '82426', '46713', '43317']
        if self.plan_hpg in plan and i < 2:
            return True
        elif (self.plan_stm in plan and i < 2) and zipcode not in zipcode_stm:
            return True
        elif (self.plan_dental in plan
              or plan in ['Essential', 'Primary', 'Essential Preferred', 'Primary Plus', 'Primary Preferred',
                          'Premier Choice', 'Premier Elite', 'Premier Plus', 'Premier Max',
                          'Primary Preferred Plus']
              or self.plan_vision in plan) and i in [0, 1]:
            return True
        elif (self.plan_asg in plan or self.plan_hsg in plan) and i == 0:
            return True
        elif self.plan_critical in plan and i == 0:
            return True
        elif self.plan_discount in plan and i == 0:
            return True
        elif self.plan_tl in plan and i == 0:
            return True
        elif self.plan_ihc in plan and i == 0:
            return True
        elif self.plan_disability in plan and i == 0:
            return True
        elif (self.plan_apg in plan or self.plan_aeg in plan) and i < 2:
            return True
        else:
            return False

    def has_occupation_field(self, zipcode, plan='', i=0):
        """for plan with occupation input"""
        if (self.plan_hpg in plan or self.plan_critical in plan) and i == 0:
            return True
        # elif (self.plan_dental in plan or self.plan_vision in plan) and i == 0:
        #     return True
        elif self.plan_asg in plan and i == 0:
            return True
        elif self.plan_tl in plan and i == 0:
            return True
        else:
            return False

    def has_driver_license(self, zipcode, plan='', i=0):
        """for plan with drivers's license input"""
        if self.plan_disability in plan and i == 0:
            return True
        else:
            return False

    def has_relationship_field(self, zipcode, plan='', i=0):
        """for zipcode with relationship input"""
        if (self.plan_vision in plan or self.plan_dental in plan) and i > 1:
            return True
        else:
            return False

    def has_marital_status_field(self, zipcode, plan='', i=0):
        """for plan with marital status input"""
        zipcodes_ihc = ['82422', '04848', '57358']
        if (self.plan_ihc in plan and i == 0) and zipcode not in zipcodes_ihc:
            return True
        # elif self.plan_disability in plan and i == 0:
        #     return True
        else:
            return False

    def has_place_of_birth_field(self, zipcode, plan='', i=0):
        """for plan with place of birth field"""
        if self.plan_disability in plan and i == 0:
            return True
        else:
            return False

    def has_employment_info(self, zipcode, plan='', i=0):
        """for plan with employment information input"""
        if self.plan_disability in plan and i == 0:
            return True
        else:
            return False

    def has_employer_address(self, zipcode, plan='', i=0):
        """for plan with employment information input"""
        if self.plan_disability in plan and i == 0:
            return True
        else:
            return False

    def has_beneficiary_fields(self, plan=''):
        """for plan with beneficiary fields"""
        plans_with_beneficiary = [self.plan_critical, self.plan_asg, self.plan_apg, self.plan_hsg, self.plan_tl,
                                  self.plan_hpg, self.plan_aeg]
        for pwb in plans_with_beneficiary:
            if pwb in plan:
                return True
        return False

    def has_question_page(self, state, plan=''):
        """for states without question page"""
        states_dental_plus = ['AZ', 'IN', 'MI', 'MO', 'OH']
        # 12/15 release: added CA
        states_dental = ['AL', 'AZ', 'DC', 'GA', 'HI', 'IN', 'KS', 'LA', 'MD', 'MI', 'MN', 'MS', 'MO', 'NE',
                         'NV', 'NC', 'ND', 'OH', 'OR', 'SC', 'SD', 'TN', 'WI', 'WY', 'AK', 'CA', 'RI']  # is AK included? 'CA'
        states_vision = ['AL', 'AZ', 'CA', 'DC', 'GA', 'HI', 'IN', 'KS', 'KY', 'LA', 'MD', 'MI', 'MS', 'MO', 'NE', 'NV',
                         'NC', 'ND', 'OH', 'OR', 'SC', 'SD', 'TN', 'WY']
        # 10/27 release: CQ: adding OH for 12/15
        states_discount = ['MA', 'NM', 'OH', 'AK']
        states_acc_pro = ['LA', 'MS', 'WI', 'FL', 'MI']
        if self.plan_dental_plus in plan:
            if state in states_dental_plus:
                return False
            return True
        elif state in states_dental and \
                (self.plan_dental in plan
                 or plan in ['Essential', 'Primary', 'Essential Preferred', 'Primary Plus', 'Primary Preferred',
                             'Premier Choice', 'Premier Elite', 'Premier Plus', 'Premier Max',
                             'Primary Preferred Plus']):
            return False
        elif state in states_vision and self.plan_vision in plan:
            return False
        # 10/27 release: CQ
        elif state in states_discount and self.plan_discount in plan:
            return False
        # 03/09 release
        elif state in states_acc_pro and self.plan_apg in plan:
            return False
        else:
            return True

    def has_expand_coverage_pop_up(self, zipcode, plan='', i=0):
        """for zipcode with or without expand coverage pop-up dialog"""
        zipcodes_dental = ['57358', '86031', '61772']
        zipcodes_vision = ['74545', '82426', '94043']
        zipcodes_critical = ['84767', '85929', '95910']
        zipcodes_asg = ['19953', '72718', '50003', '48161', '48092']
        zipcodes_ihc = ['57358']
        zipcodes_hpg = ['00000']    # dummy
        zipcodes_discount = ['06770']
        if zipcode in zipcodes_dental and self.plan_dental in plan:
            return False
        elif zipcode in zipcodes_vision and self.plan_vision in plan:
            return False
        elif zipcode in zipcodes_critical and self.plan_critical in plan:
            return False
        elif zipcode in zipcodes_asg and self.plan_asg in plan:
            return False
        elif zipcode in zipcodes_ihc and self.plan_ihc in plan:
            return False
        elif zipcode in zipcodes_hpg and self.plan_hpg in plan:
            return False
        elif zipcode in zipcodes_discount and self.plan_discount in plan:
            return False
        else:
            return True

    def has_consecutive_stm_pop_up(self, state, plans, i=0):
        """for state with or without consecutive stm pop-up dialog"""
        states = ['AZ', 'AR', 'AL', 'FL', 'GA', 'IN', 'KY', 'LA', 'MS', 'NE', 'NC', 'NV', 'OH', 'OK', 'SC', 'TN',
                  'TX', 'VA', 'WI', 'WV', 'WY']  # 'MI',
        for plan in plans:
            if self.plan_stm in plan and state in states:
                return True
        return False

    def has_registration_pop_up(self, zipcode, plan=''):
        """for zipcode with registration pop-up dialog"""
        # 12/15 release: added 82442', '43331', '47330', '48887', '67031', '19964', '37048'
        # 07/20/2018 release: added '45121', 79378, 63013, 53167, 26704, 92124, 94066, 80906, 19940, 99656, 46807,
        #                           47441, 42356, 21094, 04254
        # if zipcode in ['75802', '30304', '35183', '62084', '06377', '65680', '28070', '82442', '43331', '47330',
        #                '48887', '67031', '19964', '37048', '45121', '79378', '63013', '53167', '26704', '92124',
        #                '94066', '80906', '19940', '99656', '46807', '47441', '42356', '21094', '04254']:
        #     return False
        # else:
        #     return True
        return False

    def has_signature_checkbox(self, zipcode, plan='', i=0):
        """for zipcode without spouse signature button"""
        if i == 0:
            return True
        elif self.plan_tl in plan and i == 1:
            return True
        elif self.plan_dental in plan and i == 1:
            #  12/15 release: added if zipcode in []
            if zipcode in ['85730', '19896', '21770', '28110', '25710', '85732', '65541', '49880', '38619', '50517',
                           '73115', '84306', '04850', '57197']:
                return False
            else:
                return True
        elif self.plan_hpg in plan and i == 1:
            return True
        elif self.plan_critical in plan and i == 1:
            return True
        elif self.plan_asg in plan and i == 1:
            return True
        elif self.plan_hsg in plan and i == 1:
            return True
        elif self.plan_ihc in plan and i == 1:
            return True
        else:
            return False

    def has_ancillary_tab(self, state, quote_type, plan=''):
        """for states with or without ancillary tab"""
        morecoverage = ['AK', 'MN', 'VA', 'WI']
        visionandmore = ['AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS',
                         'KY', 'LA', 'MD', 'ME', 'MI', 'MO', 'MS', 'NC', 'NE', 'NV', 'OH', 'OK', 'OR', 'PA', 'SD', 'TN',
                         'TX', 'WV', 'WY']
        nomorebutton = ['MT', 'NM', 'RI', 'UT']
        if state in morecoverage:
            return 'morecoverage'
        elif state in visionandmore:
            return 'visionandmore'
        else:
            return 'nomorebutton'

    def plan_available(self, state, plan='', rdate=None):
        # available_states_hpg1 = ['IN', 'MO', 'TN']
        available_states_hpg2 = ['AK', 'AL', 'AR', 'AZ', 'CO', 'DE', 'FL', 'GA', 'HI', 'ID', 'IA', 'IL', 'KY', 'LA',
                                 'ME', 'MD', 'MI', 'MN', 'MS', 'NE', 'NC', 'NV', 'OH', 'OK', 'OR', 'PA', 'SC', 'TX',
                                 'UT', 'WV', 'WI', 'WY']
        available_states_stm = ['AL', 'AR', 'AZ', 'CT', 'DE', 'FL', 'GA', 'IA', 'IL', 'IN', 'KS', 'KY', 'LA', 'MI',
                                'MO', 'MS', 'MT', 'NC', 'NE', 'NV', 'OH', 'OK', 'OR', 'PA', 'SC', 'TN', 'TX', 'VA',
                                'WI', 'WV', 'WY']
        available_states_dental = ['AZ', 'CA', 'CT', 'FL', 'IN', 'MI', 'MO', 'OH', 'TX']
        available_states_dental_plus = ['AZ', 'CA', 'CT', 'FL', 'IN', 'MI', 'MO', 'OH', 'TX']
        available_states_critical = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'DE', 'FL', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS',
                                     'KY', 'LA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NV',
                                     'NM', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'WI', 'WV', 'WY']
        available_states_asg2 = ['AK', 'AL', 'AR', 'AZ', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'IA', 'IL', 'IN', 'KS',
                                 'KY', 'LA', 'MD', 'MI', 'MN', 'MO', 'MS', 'NC', 'NE', 'NV', 'OH', 'OK', 'OR', 'PA',
                                 'SC', 'SD', 'TN', 'TX', 'WI', 'WV']
        available_states_vision = ['AL', 'AR', 'AZ', 'CA', 'CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL', 'IN',
                                   'KS', 'KY', 'LA', 'MD', 'ME', 'MI', 'MO', 'MS', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NV',
                                   'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'WA', 'WV', 'WY']
        available_states_hsg = ['AK', 'AL', 'AR', 'AZ', 'CT', 'DC', 'DE', 'FL', 'GA', 'IA', 'IL', 'IN', 'KS', 'KY',
                                'LA', 'MD', 'MI', 'MN', 'MO', 'MS', 'NC', 'NE', 'NV', 'OH', 'OK', 'OR', 'PA', 'SC',
                                'SD', 'TN', 'TX', 'VA', 'WI', 'WV']
        available_states_tl = ['AK', 'AL', 'AR', 'AZ', 'CT', 'DC', 'DE', 'FL', 'GA', 'IA', 'IL', 'IN', 'KS', 'KY', 'LA',
                               'MD', 'MI', 'MN', 'MO', 'MS', 'NC', 'NE', 'NV', 'OH', 'OK', 'PA', 'SC', 'SD', 'TN', 'TX',
                               'VA', 'WI', 'WV']
        available_states_discount = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'GA', 'HI', 'IA', 'ID', 'IL',
                                     'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND',
                                     'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'SC', 'SD', 'TN', 'TX',
                                     'VA', 'WI', 'WV', 'WY']
        if self.plan_hpg in plan and state in available_states_hpg2:
            return True
        elif self.plan_stm in plan and state in available_states_stm:
            return True
        elif self.plan_dental in plan and state in available_states_dental:
            return True
        elif self.plan_dental_plus in plan and state in available_states_dental_plus:
            return True
        elif self.plan_critical in plan and state in available_states_critical:
            return True
        elif self.plan_asg in plan and state in available_states_asg2:
            return True
        elif self.plan_vision in plan and state in available_states_vision:
            return True
        elif self.plan_hsg in plan and state in available_states_hsg:
            return True
        elif self.plan_tl in plan and state in available_states_tl:
            return True
        elif self.plan_discount in plan and state in available_states_discount:
            return True
        return False