import time

from logging import getLogger
from num2words import num2words
from datetime import datetime

from src.lib.actions import Actions
import src.lib.base as base


class UHO_ActionSeries(Actions):
    def __init__(self, test_name, driver):
        Actions.__init__(self, test_name, driver)

    def now_is_past_release(self, date):
        """Boolean: Check if current date is past release date"""
        # current = time.strptime("11/30/2018", "%m/%d/%Y")broker_login
        current = time.localtime()
        target_release = time.strptime(date, "%m/%d/%Y")

        if current < target_release:
            return False

        return True

    @staticmethod
    def census_app_formatter(data):
        return census_app_formatter(data)

    def county_selection(self, step, county):
        county = str(county).upper()
        self.wait_loading(step)
        # Check if county dropdown is present
        if len(self.driver.find_elements_by_css_selector("[id*=county]")) == 1:
            self.select(step, "County: %s" % county, "<ghi_county_fld>")

    def census_applicant_inputs(self, step, primary=None, spouse=None, child1=None, child2=None, child3=None,
                                app_type=None):
        log = getLogger('%s.ApplicantInputs.%i' % (self.test_name, step))
        self.wait_loading(0)
        if primary is not None:
            if (primary["gender"].capitalize()) == "Male" or primary["gender"].upper().strip() == "M":
                self.click(step, "Primary: Male", "label[for=primary_gender_0]")
                # self.click(step, "Primary: Male", "<applicant_gender_list_1>")
                self.wait_loading(step)
            else:
                self.click(step, "Primary: Female", "label[for=primary_gender_1]")
                # self.click(step, "Primary: Female", "[name=primary_gender][data-uib-btn-radio*=Female]")
                self.wait_loading(step)
            if primary["dob"]:
                self.enter(step, primary["dob"], "<applicant_dob_field_1>")
                self.wait_loading(step)
            if primary["tobacco"]:
                self.select(step, "Primary Tobacco: %s" % primary["tobacco"], "<applicant_tobacco_list_1>")
                self.wait_loading(step)

        if spouse is not None:
            # Check first if Spouse field is present
            # spouse_label = self.drivers.find_elements_by_css_selector("h2#label_spouse")
            # if len(spouse_label) == 0:
            # Click Add Spouse button
            if app_type is None:
                self.click(step, "Add Spouse", "<ghi_add_spouse_btn>")
                self.wait_loading(step)
                if (spouse["gender"].capitalize()) == "Male" or spouse["gender"].upper().strip() == "M":
                    self.click(step, "Spouse: Male", "<ghi_spouse_gender_male>")
                    self.wait_loading(step)
                else:
                    self.click(step, "Spouse: Female", "<ghi_spouse_gender_female>")
                    self.wait_loading(step)
                if spouse["dob"]:
                    self.enter(step, spouse["dob"], "<ghi_spouse_dob_fld>")
                    self.wait_loading(step)
                if spouse["tobacco"]:
                    self.select(step, "Spouse Tobacco: %s" % spouse["tobacco"], "<applicant_tobacco_list_2>")
                    self.wait_loading(step)
            elif app_type is not None:
                if (spouse["gender"].capitalize()) == "Male" or spouse["gender"].upper().strip() == "M":
                    self.click(step, "Spouse: Male", "<ghi_spouse_gender_male>")
                    self.wait_loading(step)
                else:
                    self.click(step, "Spouse: Female", "<ghi_spouse_gender_female>")
                    self.wait_loading(step)
                if spouse["dob"]:
                    self.enter(step, spouse["dob"], "<ghi_spouse_dob_fld>")
                    self.wait_loading(step)
                if spouse["tobacco"]:
                    self.select(step, "Spouse Tobacco: %s" % spouse["tobacco"], "<applicant_tobacco_list_2>")
                    self.wait_loading(step)

        if child1 is not None:
            # Check first if Child1 field is present
            # child_label = self.drivers.find_elements_by_css_selector("h2#label_child0")
            # if len(child_label) == 0:
            # Click Add Child button
            self.click(step, "Add Child", "<ghi_add_child_btn>")
            self.wait_loading(step)
            if (child1["gender"].capitalize()) == "Male" or child1["gender"].upper().strip() == "M":
                self.click(step, "Child1: Male", "<ghi_child1_gender_male>")
                self.wait_loading(step)
            else:
                self.click(step, "Child1: Female", "<ghi_child1_gender_female>")
                self.wait_loading(step)
            if child1["dob"]:
                self.enter(step, child1["dob"], "<applicant_dob_field_3>")
                self.wait_loading(step)
            if child1["tobacco"]:
                self.select(step, "Child1 Tobacco: %s" % child1["tobacco"], "<applicant_tobacco_list_3>")
                self.wait_loading(step)

        if child2 is not None:
            # Check first if Child1 field is present
            # child_label = self.drivers.find_elements_by_css_selector("h2#label_child1")
            # if len(child_label) == 0:
            # Click Add Child button
            self.click(step, "Add Child", "<ghi_add_child_btn>")
            self.wait_loading(step)
            if (child2["gender"].capitalize()) == "Male" or child2["gender"].upper().strip() == "M":
                self.click(step, "Child2: Male", "<ghi_child2_gender_male>")
                self.wait_loading(step)
            else:
                self.click(step, "Child2: Female", "<ghi_child2_gender_female>")
                self.wait_loading(step)
            if child2["dob"]:
                self.enter(step, child2["dob"], "<applicant_dob_field_4>")
                self.wait_loading(step)
            if child2["tobacco"]:
                self.select(step, "Child2 Tobacco: %s" % child2["tobacco"], "<applicant_tobacco_list_4>")
                self.wait_loading(step)

        if child3 is not None:
            # Check first if Child1 field is present
            # child_label = self.drivers.find_elements_by_css_selector("h2#label_child1")
            # if len(child_label) == 0:
            # Click Add Child button
            self.click(step, "Add Child", "<ghi_add_child_btn>")
            self.wait_loading(step)
            if (child3["gender"].capitalize()) == "Male" or child3["gender"].upper().strip() == "M":
                self.click(step, "Child3: Male", "<ghi_child3_gender_male>")
                self.wait_loading(step)
            else:
                self.click(step, "Child3: Female", "<ghi_child3_gender_female>")
                self.wait_loading(step)
            if child3["dob"]:
                self.enter(step, child3["dob"], "<applicant_dob_field_5>")
                self.wait_loading(step)
            if child3["tobacco"]:
                self.select(step, "Child3 Tobacco: %s" % child3["tobacco"], "<applicant_tobacco_list_5>")
                self.wait_loading(step)

    def expand_coverage_modal(self, step):
        self.wait_loading(step)
        self.verify(step, "Displayed: Expand Your Coverage Modal", "<expand_coverage_dlg>")
        self.click(step, "Go to Cart", "<go_to_cart_bttn>")
        self.wait_loading(step)

    def broker_login(self, step):
        broker_pw = base.config['broker_pw']
        self.url(step, "https://uhone.com/broker", "UHOne Broker Portal | UnitedHealthOne")
        self.wait_loading(step)
        self.enter(step, "44404", "<uho_broker_id_fld>")
        self.enter(step, broker_pw, "<uho_broker_password_fld>", mask=True)
        self.click(step, "Sign In", "<uho_broker_sign_in_bttn>")
        self.wait_loading(step)

    def broker_instant_quote(self, step):
        self.broker_login(step)
        self.click(step, "Instant Quote", "<uho_get_instant_quote_bttn>")
        self.wait_loading(step)

    def logout_broker(self, step):
        self.wait_loading(step)
        self.click(step, "Return Home", "[data-ng-click*='returnHome']")
        self.click(step, "Sign Off", "<uho_sign_off_lnk>")

    def wait_loading(self, step):
        self.pause(step, "1", "")
        self.wait(step, "Loading", "<uhone_loading>")

    def find_product(self, step, plan):
        self.wait_loading(step)
        self.verify(step, "Displayed: Plans List Page", "nav.navbar.navbar-default.mc-product-menu")
        tab_menu = "mc-product-tab-menu.mc-product-menu-container"
        tab_menu_list = "[data-ng-repeat-start*='applicationTypes']"
        more_tab = "#simple-btn-keyboard-nav"
        more_tab_list = "[data-ng-repeat*='groupedApplicationType in groupedApplicationTypes']"
        product_found = False

        # Search the product or plan from the menu tab first
        if self.driver.find_element_by_css_selector(tab_menu):
            self.wait_loading(step)
            menu_list = self.driver.find_elements_by_css_selector(tab_menu_list)
            self.wait_loading(step)
            for x in menu_list:  # (menu1, menu2, menu3, menu...)
                menu_label = str(x.text).lower()
                menu_plan = str(plan).lower()
                if menu_label.strip() == menu_plan.strip():
                    product_found = True
                    x.click()
                    break
        # If not found, then search the product or plan in the "MORE" tab
        if not product_found:
            if self.check(step, "Element: More tab", more_tab):
            # if self.drivers.find_element_by_css_selector(more_tab):
                self.wait_loading(step)
                self.click(step, "More Tab", more_tab)
                self.wait_loading(step)
                more_list = self.driver.find_elements_by_css_selector(more_tab_list)
                self.wait_loading(step)
                for y in more_list:  # (more1, more2, more3, more...)
                    more_label = str(y.text).lower()
                    more_plan = str(plan).lower()
                    if more_label == more_plan.strip():
                        y.click()
                        break
        self.wait_loading(step)

    def applicant_information(self, step, data, autofill=False, ext=None):
        """Example: autofill = False
        data = (
            {"<ghi_firstname_fld>": "Firstname"},
            {"<ghi_lastname_fld>": "Lastname"},
            {"<ghi_primary_height_ft_fld>": "5"},
            {"<ghi_primary_height_in_fld>": "5"},
            {"<ghi_primary_weight_fld>": "155"},
            {"<ghi_primary_email_fld>": "uhonetesting@gmail.com"},
            {"<uho_applicant_phonenum_field_1>": "(333) 333-3333"},
            {"<ghi_contact_info_address_fld>": "GENERAL DELIVERY"},
            {"<ghi_contact_info_city_fld>": "CITY"}
        )
        Example: autofill = True
        data = ("primary", "spouse", "dependent1", dependent2)
        """
        if not autofill:
            for d in data:
                for key, value in d.items():
                    self.enter(step, value, key)
                    self.wait_loading(step)
        else:
            ###########################################################################################################
            # Using BS4
            ###########################################################################################################
            # ht_wt = ("primary_height_feet", "spouse_height_feet", "dependent0_height_feet",
            #          "dependent1_height_feet", "dependent2_height_feet")
            # email = ("primary_emailAddress", "spouse_emailAddress", "dependent0_emailAddress",
            #          "dependent1_emailAddress", "dependent2_emailAddress")
            # phone = ("primary_phone", "spouse_phone", "dependent0_phone", "dependent1_phone", "dependent2_phone")
            # occup = ("primary_occupation", "spouse_occupation", "dummy", "dummy", "dummy")
            # relate = ("spouse_relationship", "dependent0_relationship", "dependent1_relationship",
            #           "dependent2_relationship")
            # ssnum = ("primary_SSN", "spouse_SSN", "dependent0_SSN", "dependent1_SSN", "dependent2_SSN")
            weight = 185
            height_in = "5"
            names = ("Firstname", "Spouse", "Uno", "Dos", "Tres", "Quatro", "Singko")
            lname = "Lastname"
            address = "GENERAL DELIVERY"
            city = "City"
            email_add = base.config['email_add']
            pob = "US"
            beneficiary = "Bene"
            relationship = "Nephew"
            benef_dob = "01/01/2001"
            benef_ssn = "135-79-1359"
            ss_num = "135-79-1351"
            license_num = "F255921500940"
            phone_num = "(333) 333-3333"
            state = "FL"
            salary = "123456.99"
            occupation = "IT"
            if ext:
                names, lname = self.applicant_name(ext["st"], data, ext["name"], ext["plans"])
                if ext["addrss"]:
                    address = ext["addrss"]
            # try:
            #     body = self.drivers.find_element_by_css_selector("#body").get_attribute('innerHTML')
            #     soup = BeautifulSoup(body, features="lxml")
            #     fields = soup.find_all('input')
            #     selections = soup.find_all('select')
            #     input_fields = []
            #     drop_downs = []
            #     no_spouse = True
            #     for input_field in fields:
            #         if input_field.get('id'):
            #             input_fields.append(input_field.get('id'))
            #     for selection in selections:
            #         if selection.get('id'):
            #             drop_downs.append(selection.get('id'))
            #     if len(data) > 1:
            #         for applicant in data:
            #             if "spouse" in applicant:
            #                 no_spouse = False
            #                 break
            #     for x, value in enumerate(data):
            #         index = x + 1
            #         if x > 0 and no_spouse:
            #             index = x + 2
            #         if self.check(0, "Empty: fname field", "<uho_applicant_fname_field_" + str(index) + ">"):
            #             self.enter(step, names[x], "<uho_applicant_fname_field_" + str(index) + ">")
            #         if self.check(0, "Empty: lname field", "<uho_applicant_lname_field_" + str(index) + ">"):
            #             self.enter(step, lname, "<uho_applicant_lname_field_" + str(index) + ">")
            #         if x < 1:
            #             if "primary_maritalstatus" in input_fields:
            #                 self.click(step, "Married", "<ghi_marital_status_married_btn>")
            #         if "primary_placeOfBirth" in input_fields:
            #             if self.check(0, "Empty: place of birth field", "#primary_placeOfBirth"):
            #                 self.enter(step, pob, "#primary_placeOfBirth")
            #         if ht_wt[x] in input_fields or ht_wt[index - 1] in input_fields:
            #             if self.check(0, "Empty: height field", "<uho_applicant_height_ft_field_" + str(index) + ">"):
            #                 # self.enter(step, str(6 - x), "<uho_applicant_height_ft_field_" + str(index) + ">")
            #                 self.enter(step, str(5), "<uho_applicant_height_ft_field_" + str(index) + ">")
            #             if self.check(0, "Empty: weight field", "<uho_applicant_height_in_field_" + str(index) + ">"):
            #                 self.enter(step, height_in, "<uho_applicant_height_in_field_" + str(index) + ">")
            #             if self.check(0, "Empty: lbs field", "<uho_applicant_weight_lbs_field_" + str(index) + ">"):
            #                 self.enter(step, str(weight), "<uho_applicant_weight_lbs_field_" + str(index) + ">")
            #             weight -= 30
            #         if ssnum[x] in input_fields or ss_num[index - 1] in input_fields:
            #             if self.check(0, "Empty: ssnum field", "<uho_applicant_ssn_field_" + str(index) + ">"):
            #                 self.enter(step, ss_num, "<uho_applicant_ssn_field_" + str(index) + ">")
            #         if email[x] in input_fields or email[index - 1] in input_fields:
            #             if self.check(0, "Empty: email field", "<uho_applicant_emailadd_field_" + str(index) + ">"):
            #                 self.enter(step, email_add, "<uho_applicant_emailadd_field_" + str(index) + ">")
            #         if phone[x] in input_fields or phone[index - 1] in input_fields:
            #             if self.check(0, "Empty: phone field", "<uho_applicant_phonenum_field_" + str(index) + ">"):
            #                 self.enter(step, phone_num, "<uho_applicant_phonenum_field_" + str(index) + ">")
            #         if occup[x] in input_fields:
            #             if self.check(0, "Empty: occupation field",
            #                           "<uho_applicant_occupation_field_" + str(index) + ">"):
            #                 self.enter(step, occupation, "<uho_applicant_occupation_field_" + str(index) + ">")
            #         if "primary_driverLicenseNumber" in input_fields:
            #             if self.check(0, "Empty: drivers license number field", "#primary_driverLicenseNumber"):
            #                 self.enter(step, license_num, "#primary_driverLicenseNumber")
            #         if "primary_annualSalary" in input_fields:
            #             if self.check(0, "Empty: annual salary field", "input#primary_annualSalary"):
            #                 self.enter(step, salary, "input#primary_annualSalary")
            #         if "primary_driverLicenseState" in drop_downs:
            #             if self.check(0, "Empty: drivers license state field", "select#primary_driverLicenseState"):
            #                 self.select(step, "state: " + state, "select#primary_driverLicenseState")
            #         if x > 0:
            #             if relate[x - 1] in input_fields or relate[index - 2] in input_fields:
            #                 if self.check(0, "Empty: relationship",
            #                               "<uho_applicant_relationship_field_" + str(index) + ">"):
            #                     self.enter(step, relationship, "<uho_applicant_relationship_field_" + str(index) + ">")
            #     if self.check(0, "Empty: address", "<ghi_contact_info_address_fld>"):
            #         self.enter(step, address, "<ghi_contact_info_address_fld>")
            #     if self.check(0, "Empty: city", "<ghi_contact_info_city_fld>"):
            #         self.enter(step, city, "<ghi_contact_info_city_fld>")
            #     if "contactInfo_phoneNumber" in input_fields:
            #         if self.check(0, "Empty: phone number", "<ghi_contact_info_phone_fld>"):
            #             self.enter(step, phone_num, "<ghi_contact_info_phone_fld>")
            #         if self.check(0, "Empty: email add", "<ghi_contact_info_email_fld>"):
            #             self.enter(step, email_add, "<ghi_contact_info_email_fld>")
            #     if "beneficiaryInfo_firstName" in input_fields:
            #         if self.check(0, "Empty: beneficiary", "<uho_beneficiary_fname_field>"):
            #             self.enter(step, beneficiary, "<uho_beneficiary_fname_field>")
            #         if self.check(0, "Empty: lname", "<uho_beneficiary_lname_field>"):
            #             self.enter(step, lname, "<uho_beneficiary_lname_field>")
            #         if self.check(0, "Empty: relationship", "<uho_beneficiary_relationship_field>"):
            #             self.enter(step, relationship, "<uho_beneficiary_relationship_field>")
            #         if "beneficiaryInfo_dob" in input_fields:
            #             if self.check(0, "Empty: beneficiary dob", "<uho_beneficiary_dob_field>"):
            #                 self.enter(step, benef_dob, "<uho_beneficiary_dob_field>")
            #         if "beneficiaryInfo_SSN" in input_fields:
            #             if self.check(0, "Empty: beneficiary ssn", "#beneficiaryInfo_SSN"):
            #                 self.enter(step, benef_ssn, "#beneficiaryInfo_SSN")
            # except WebDriverException as wde:
            #     print(str(wde))
            no_spouse = True
            if len(data) > 1:
                for applicant in data:
                    if "spouse" in applicant:
                        no_spouse = False
                        break
            for x, value in enumerate(data):
                index = x + 1
                if x > 0 and no_spouse:
                    index = x + 2
                if self.check(0, "Empty: fname field", "<uho_applicant_fname_field_" + str(index) + ">"):
                    self.enter(step, names[x], "<uho_applicant_fname_field_" + str(index) + ">")
                if self.check(0, "Empty: lname field", "<uho_applicant_lname_field_" + str(index) + ">"):
                    self.enter(step, lname, "<uho_applicant_lname_field_" + str(index) + ">")
                if x < 1:
                    if self.check(step, "Element: Marital Status", "<ghi_marital_status_married_btn>"):
                        self.click(step, "Married", "<ghi_marital_status_married_btn>")
                if self.check(0, "Element: place of birth field", "#primary_placeOfBirth"):
                    if self.check(0, "Empty: place of birth field", "#primary_placeOfBirth"):
                        self.enter(step, pob, "#primary_placeOfBirth")
                if self.check(0, "Element: height field", "<uho_applicant_height_ft_field_" + str(index) + ">"): # or index-1
                    if self.check(0, "Empty: height field", "<uho_applicant_height_ft_field_" + str(index) + ">"):
                        # self.enter(step, str(6 - x), "<uho_applicant_height_ft_field_" + str(index) + ">")
                        self.enter(step, str(5), "<uho_applicant_height_ft_field_" + str(index) + ">")
                    if self.check(0, "Empty: weight field", "<uho_applicant_height_in_field_" + str(index) + ">"):
                        self.enter(step, height_in, "<uho_applicant_height_in_field_" + str(index) + ">")
                    if self.check(0, "Empty: lbs field", "<uho_applicant_weight_lbs_field_" + str(index) + ">"):
                        self.enter(step, str(weight), "<uho_applicant_weight_lbs_field_" + str(index) + ">")
                    weight -= 30
                if self.check(0, "Element: ssnum field", "<uho_applicant_ssn_field_" + str(index) + ">"): #or index-1
                    if self.check(0, "Empty: ssnum field", "<uho_applicant_ssn_field_" + str(index) + ">"):
                        self.enter(step, ss_num, "<uho_applicant_ssn_field_" + str(index) + ">")
                if self.check(0, "Element: email field", "<uho_applicant_emailadd_field_" + str(index) + ">"): #or index-1
                    if self.check(0, "Empty: email field", "<uho_applicant_emailadd_field_" + str(index) + ">"):
                        self.enter(step, email_add, "<uho_applicant_emailadd_field_" + str(index) + ">")
                if self.check(0, "Element: phone field", "<uho_applicant_phonenum_field_" + str(index) + ">"): #or index-1
                    if self.check(0, "Empty: phone field", "<uho_applicant_phonenum_field_" + str(index) + ">"):
                        self.enter(step, phone_num, "<uho_applicant_phonenum_field_" + str(index) + ">")
                if self.check(0, "Element: occupation field",
                              "<uho_applicant_occupation_field_" + str(index) + ">"): #or index-1
                    if self.check(0, "Empty: occupation field",
                                  "<uho_applicant_occupation_field_" + str(index) + ">"):
                        self.enter(step, occupation, "<uho_applicant_occupation_field_" + str(index) + ">")
                if self.check(0, "Element: drivers license number field", "#primary_driverLicenseNumber"):
                    if self.check(0, "Empty: drivers license number field", "#primary_driverLicenseNumber"):
                        self.enter(step, license_num, "#primary_driverLicenseNumber")
                if self.check(0, "Element: annual salary field", "input#primary_annualSalary"):
                    if self.check(0, "Empty: annual salary field", "input#primary_annualSalary"):
                        self.enter(step, salary, "input#primary_annualSalary")
                if self.check(0, "Element: drivers license state field", "select#primary_driverLicenseState"):
                    if self.check(0, "Empty: drivers license state field", "select#primary_driverLicenseState"):
                        self.select(step, "state: " + state, "select#primary_driverLicenseState")
                if x > 0:
                    if self.check(0, "Element: relationship",
                                  "<uho_applicant_relationship_field_" + str(index) + ">"): #or x-1 or index-2
                        if self.check(0, "Empty: relationship",
                                      "<uho_applicant_relationship_field_" + str(index) + ">"):
                            self.enter(step, relationship, "<uho_applicant_relationship_field_" + str(index) + ">")
            if self.check(0, "Empty: address", "<ghi_contact_info_address_fld>"):
                self.enter(step, address, "<ghi_contact_info_address_fld>")
            if self.check(0, "Empty: city", "<ghi_contact_info_city_fld>"):
                self.enter(step, city, "<ghi_contact_info_city_fld>")
            if self.check(0, "Element: phone number", "<ghi_contact_info_phone_fld>"):
                if self.check(0, "Empty: phone number", "<ghi_contact_info_phone_fld>"):
                    self.enter(step, phone_num, "<ghi_contact_info_phone_fld>")
                if self.check(0, "Empty: email add", "<ghi_contact_info_email_fld>"):
                    self.enter(step, email_add, "<ghi_contact_info_email_fld>")
            if self.check(0, "Element: beneficiary", "<uho_beneficiary_fname_field>"):
                if self.check(0, "Empty: beneficiary", "<uho_beneficiary_fname_field>"):
                    self.enter(step, beneficiary, "<uho_beneficiary_fname_field>")
                if self.check(0, "Empty: lname", "<uho_beneficiary_lname_field>"):
                    self.enter(step, lname, "<uho_beneficiary_lname_field>")
                if self.check(0, "Empty: relationship", "<uho_beneficiary_relationship_field>"):
                    self.enter(step, relationship, "<uho_beneficiary_relationship_field>")
                if self.check(0, "Element: beneficiary dob", "<uho_beneficiary_dob_field>"):
                    if self.check(0, "Empty: beneficiary dob", "<uho_beneficiary_dob_field>"):
                        self.enter(step, benef_dob, "<uho_beneficiary_dob_field>")
                if self.check(0, "Element: beneficiary ssn", "#beneficiaryInfo_SSN"):
                    if self.check(0, "Empty: beneficiary ssn", "#beneficiaryInfo_SSN"):
                        self.enter(step, benef_ssn, "#beneficiaryInfo_SSN")

            self.click(step, "Continue", "<ghi_continue_bttn>")
            self.wait_loading(step)
            # self.verify(step, "Displayed: Resident Physical Address error", "<uho_address_mismatch_error>")
            if len(self.driver.find_elements_by_css_selector(
                    ".mc-address-found button[data-ng-click*='address.suggested']")) == 1:  # "<uho_use_this_address>"))
                self.click(step, "Use This Address button", "<uho_use_this_address>")
            else:
                self.click(step, "Continue As Entered", "button[data-ng-click*='useOriginalAddress']")
            self.wait_loading(step)
            current_url = self.driver.current_url
            if "applicants" in current_url:
                self.click(step, "Continue", "<ghi_continue_bttn>")
            self.wait_loading(step)

    def payment(self, payment_type, data=None):
        """
        Populates Payment page
        :param payment_type:
        :param data:
        :return:
        """
        if data is None:
            data = {
                "eft_routing": "074000010", "eft_acc_num": "123456789", "eft_draft": "Day: 10",
                "cc_name": "CC", "cc_num": "4111111111111111", "cc_expiry": "12/20", "cc_draft": "Draftday: 28"
            }
        self.wait_loading(0)
        payment_bttn_1 = ""
        payment_bttn_2 = ""
        if self.check(0, "Element: Payment button 1", "[for='payment_type_0_0']"):
            payment_bttn_1 = self.driver.find_element_by_css_selector("[for='payment_type_0_0']")
        if self.check(0, "Element: Payment button 1", "[for='payment_type_0_1']"):
            payment_bttn_2 = self.driver.find_element_by_css_selector("[for='payment_type_0_1']")
        # singlepayment = False
        if str(payment_type).lower().strip() == "eft":
            if "Electronic" in payment_bttn_1.text:
                payment_bttn_1.click()
            else:
                payment_bttn_2.click()
            # self.wait_loading(0)
            # if self.check(0, "Element: EFT routing number", "<ghi_accnt_routing_num_fld>"):
                # singlepayment = True
        else:  # if str(payment).lower().strip() == "credit card":
            if "Credit" in payment_bttn_1.text:
                payment_bttn_1.click()
            else:
                payment_bttn_2.click()
            # self.wait_loading(0)
            # if self.check(0, "Element: Credit Card Frame", "iframe#payment-form-iframe"):
                # singlepayment = True
        self.wait_loading(0)
        self.wait_loading(0)
        # current_url = self.drivers.current_url
        # EFT PAYMENT
        if str(payment_type).lower().strip() == "eft":
            self.enter(0, data["eft_routing"], "<ghi_accnt_routing_num_fld>")
            self.enter(0, data["eft_acc_num"], "<ghi_accnt_number_fld>")
            self.pause(0, "1", "second")
            if len(self.driver.find_elements_by_css_selector("select#draftDay")) == 1:
                self.select(0, data["eft_draft"], "select#draftDay")
        # CC PAYMENT
        else:
            # Verify, Displayed: Secure Payment Info,<uho_payment_type_header>,
            self.pause(0, "5", "seconds")
            self.switch(0, "Switch to Trust Commerce frame", "iframe#payment-form-iframe")
            self.enter(0, data["cc_name"], "input#CreditCard_name")
            self.enter(0, data["cc_num"], "input#CreditCard_cardNumber")
            self.enter(0, data["cc_expiry"], "input#CreditCard_expDate")
            # Enter, 90001, input#billingzipcode,
            self.click(0, "Save button", "input#cardPay")
            self.pause(0, "3", "seconds")
            self.wait_loading(0)
            if len(self.driver.find_elements_by_css_selector("select#creditcard_draftDay")) == 1:
                self.select(0, data["cc_draft"], "select#creditcard_draftDay")

    def applicant_name(self, st, data, name, plans):
        """
        Returns the primary name of applicant
        :param st:
        :param data:
        :param name:
        :param plans:
        :return names, lname:
        """
        names = ("Primary", "Spouse", "Uno", "Dos", "Tres", "Quatro", "Singko")
        lname = "TestLastName"
        if str(name).lower().strip() == "dynamic":
            names = []  # STPrimary HPSV
            plan_acronym = ""
            # month = str(datetime.now().strftime('%B'))[:3]
            day = num2words(datetime.now().day).capitalize()
            hr = num2words(int(datetime.now().strftime("%I"))).capitalize()
            min = num2words(int(datetime.now().minute)).capitalize()
            # sec = num2words(int(datetime.now().second)).capitalize()
            am_pm = datetime.now().strftime("%p")
            # lname = month + day + hr + min + am_pm  # AprElevenFourTwentyPM
            lname = day + hr + am_pm  # Twenty-SevenTwelveAM
            if type(plans) is str:
                plan_acronym = plan_acronym + plans[0]
            else:
                for plan in plans:
                    plan = str(plan).strip()
                    if " " in plan:
                        plan = plan.split(" ")
                        for idx, pln in enumerate(plan):
                            # if idx < 2:
                            if idx < 1:
                                plan_acronym = plan_acronym + pln[0]
                                break
                        # for pln in plan:
                        #     plan_acronym = plan_acronym + pln[0]
                    else:
                        plan_acronym = plan_acronym + plan[0]
                    # plan_acronym = plan_acronym + " "
            # plan_acronym = plan_acronym[:-1]
            for applicant in data:
                names.append(st + plan_acronym + applicant[0] + min + am_pm)  # ALSPTwenty-EightAM
                # names.append(st + applicant + plan_acronym + sec)

        elif not str(name).lower().strip() == "fix":
            if "[" in name:
                name = str(name).replace("[", "").replace("]", "")
                if "," in name:
                    name = name.split(",")
                    names = []
                    for index, name_ in enumerate(name):
                        name_ = name_.strip().split(" ")
                        names.append(name_[0])
                        if index == 0:
                            lname = name_[1]
                else:
                    name = str(name).strip().split(" ")
                    if len(name) == 3:
                        names = [name[0] + " " + name[1]]
                        lname = name[2]
                    else:
                        names = [name[0]]
                        lname = name[1]
            else:
                name = str(name).strip().split(" ")
                if len(name) == 3:
                    names = [name[0] + " " + name[1]]
                    lname = name[2]
                else:
                    names = [name[0]]
                    lname = name[1]
        return names, lname

    def release_helper(self, step, date):
        """Use this helper if release date is a must, ignored if already a past date"""
        if not self.now_is_past_release(date):
            # Update Release Date
            self.release(step, date, None)

    def broker_help_login(self, user_id=None):
        """
        1. Login to maintenance page
        2. Click Boker Help
        3. Enter Broker ID or NPN
        4. Click Submit button
        """

        # self.url(0, "https://stage.maintenance.uhone.com", "UnitedHealthOne - Maintenance")
        self.driver.get("https://stage.maintenance.uhone.com")
        self.wait_loading(0)
        self.click(0, "Click Broker Help Link", "<broker_help>")
        if user_id is None:
            self.enter(0, "44407", "<uho_osign_broker_id_fld>")
        else:
            self.enter(0, user_id, "<uho_osign_broker_id_fld>")
        self.click(0, "Submit", "<uho_osign_submit_login_btn>")
        self.wait_loading(0)

class GHI_ActionSeries(UHO_ActionSeries):
    def __init__(self, test_name, driver):
        Actions.__init__(self, test_name, driver)


class Receptacle:
    def __init__(self, x):
        self.val = x

    @property
    def val(self):
        return self.__x

    @val.setter
    def val(self, x):
        self.__x = x


def dob_formatter(dob):
    dob = str(dob)
    if "-" in dob:
        dob = dob.replace("-", "\\")

    return dob


def census_app_formatter(data=str):
    # primary = {
    #     "gender": "Male",
    #     "dob": "09\\09\\1980",
    #     "tobacco": "No"
    # }
    out = None
    if "&" in data:
        data = data.split("&")
        out = {
            "gender": data[0].strip(),
            "dob": dob_formatter(data[1]),
            "tobacco": "No"
        }
        if len(data) > 2:
            out["tobacco"] = data[2]
    return out
