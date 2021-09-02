from time import sleep

from Pages.BankPages import BankPage
from Pages.BasePages import BasePage, Loaders, Base
from classes.entities import Bid, BankAccount, BankAccountOtp, Beneficiary, Client, Stockholder, \
    Administration
from selenium.webdriver.common.keys import Keys

import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep


class AgentPage(BasePage):
    create_bid_btn = '[href="/new/create"]'
    bid_number_filter = '[placeholder="№ заявки"]'

    def check_open(self):
        self.wait_until_located(self.create_bid_btn, 'css')

    def open_bid_use_filter(self, bid_id):
        self.wait_until_located(self.bid_number_filter, 'css')
        bid_field = self.find_element_by_locator(self.bid_number_filter)
        bid_field.send_keys(bid_id)
        bid_field.send_keys(Keys.ENTER)
        bid_elem = '//b[text()[contains(.,"' + bid_id + '")]]/../..'
        Loaders(self.browser).wait_until_agent_loader_disappear()
        self.click_on_elem(bid_elem)
        agent_questionnaire = AgentQuestionnaire(self.browser)
        return agent_questionnaire

    def click_on_create_bid_btn(self):
        sleep(0.5)
        self.click_on_elem(self.create_bid_btn)

    def create_bid_ip_and_get_bid_id(self, bid: Bid, client: Client, bank_account: BankAccount,
                                     beneficiary: Beneficiary):
        self.create_bid_first_form(bid, client)

        create_bid_form = CreateBidForm(self.browser)
        create_bid_form.click_on_elem(create_bid_form.go_to_bid_btn)

        agent_questionnaire = AgentQuestionnaire(self.browser)
        agent_questionnaire.check_open()
        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_client)

        info_about_client_form = InfoAboutClientForm(self.browser)
        info_about_client_form.check_open()
        info_about_client_form.fill_required_fields_bank_account(bank_account)

        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_client)
        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_beneficiary)

        beneficiary_form = BeneficiaryForm(self.browser)
        beneficiary_form.fill_required_fields_beneficiary(beneficiary)

        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_beneficiary)
        agent_questionnaire.click_on_elem(agent_questionnaire.docs)

        return agent_questionnaire.get_bid_number()

    def create_bid_gos(self, bid: Bid, client: Client, bank_account: BankAccount, administration):
        self.create_bid_first_form(bid, client)

        create_bid_form = CreateBidForm(self.browser)
        create_bid_form.click_on_elem(create_bid_form.go_to_bid_btn)

        agent_questionnaire = AgentQuestionnaire(self.browser)
        agent_questionnaire.check_open()
        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_client)

        info_about_client_form = InfoAboutClientForm(self.browser)
        info_about_client_form.fill_required_fields_bank_account(bank_account)

        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_client)

        create_bid_page = CreateBidPage(self.browser)
        create_bid_page.fill_administration(administration)

        info_about_administration = InfoAboutAdministration(self.browser)
        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_structure)
        info_about_administration.add_holder()

        agent_questionnaire.click_on_elem(agent_questionnaire.docs)

        docs = DocsPage(self.browser)
        docs.check_open_express()
        docs.load_passport('file.jpg')
        docs.submit()

        return agent_questionnaire.get_bid_number()

    def create_bid(self, bid: Bid, client: Client, bank_account: BankAccount, beneficiary: Beneficiary,
                   administration: Administration):
        create_bid_page = CreateBidPage(self.browser)
        self.create_bid_first_form(bid, client)
        create_bid_page.fill_anketa(bank_account, beneficiary, administration)
        agent_questionnaire = AgentQuestionnaire(self.browser)
        return agent_questionnaire.get_bid_number()

    def create_bid_first_form(self, bid: Bid, client: Client, check_form_data=True):
        agent_page = AgentPage(self.browser)
        agent_page.check_open()
        agent_page.click_on_create_bid_btn()

        create_bid_page = CreateBidPage(self.browser)
        create_bid_page.check_open()
        create_bid_page.fill_required_fields_client(bid, client)

        create_bid_page.fill_guarantee_price_field(bid)
        create_bid_page.click_on_elem(create_bid_page.create_btn)

        create_bid_form = CreateBidForm(self.browser)
        create_bid_form.check_open()
        if check_form_data:
            create_bid_form.check_form_data(bid)


class CreateBidPage(BasePage):
    inn = '//div[contains(@data-vv-as, "ИНН")]//input'
    contract_number = '[name="purchase"]'
    contract_price = '[name="final_price"]'
    type = '[name="bg_types"]'
    guarantee_price = '[name="execSum"]'
    create_btn = '//button[text()[contains(.,"подать заявку")]]'
    date_finish = '[name="date_finish"]'
    page_title = '.b-page__title'
    guarantee_prices_group = '[data-vv-as="Требуемая сумма"]'
    select_btn = '.btn-select'
    select_list_elements = '.checkboxLayer .selectList li'
    date_group = '[data-vv-as="Дата выдачи"] input'
    date_end_group = '[data-vv-as="Дата окончания"] input'
    clear_btn = '[data-vv-as="Дата выдачи"] [title="Очистить дату"]:not([style*="display: none"])'
    clear_btn1 = '[data-vv-as="Дата окончания"] [title="Очистить дату"]:not([style*="display: none"])'
    days_count_group_txt = '.b-bgtime'
    lot_number = '[data-vv-as="Номер лота"]'

    def fill_required_fields(self, bid: Bid):
        agent_page = AgentPage(self.browser)
        agent_page.check_open()
        agent_page.click_on_create_bid_btn()

        self.check_open()
        self.fill_required_fields_client_direct_client(bid)

        self.fill_guarantee_price_field(bid)

    def fill_anketa(self, bank_account: BankAccount, beneficiary: Beneficiary,
                    administration: Administration):
        create_bid_form = CreateBidForm(self.browser)
        create_bid_form.click_on_elem(create_bid_form.go_to_bid_btn)

        agent_questionnaire = AgentQuestionnaire(self.browser)
        agent_questionnaire.check_open()
        self.bid_id = agent_questionnaire.get_bid_number()

        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_client)
        info_about_client_form = InfoAboutClientForm(self.browser)
        info_about_client_form.fill_required_fields_bank_account(bank_account)
        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_client)

        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_beneficiary)
        beneficiary_form = BeneficiaryForm(self.browser)
        beneficiary_form.fill_required_fields_beneficiary(beneficiary)
        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_beneficiary)

        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_structure)
        info_about_structure = InfoAboutAdministration(self.browser)
        info_about_structure.fill_required_fields_administration(administration)
        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_structure)

        agent_questionnaire.click_on_elem(agent_questionnaire.docs)

    def check_open(self):
        self.wait_until_located(self.guarantee_prices_group, 'css')

    def select_type(self, type):
        self.select_elem(self.type, type)

    def fill_required_fields_client(self, bid: Bid, client: Client, group=False):
        self.fill_field_and_check_value_click_on_focus(self.inn, client.inn, self.page_title, 'xpath')
        Loaders(self.browser).wait_until_agent_loader_disappear()
        self.fill_field_and_check_value_click_on_focus(self.contract_number, bid.number, self.page_title)
        Loaders(self.browser).wait_until_agent_loader_disappear()
        self.fill_field_and_check_value_click_on_focus(self.contract_price, bid.final_price, self.page_title)
        self.select_type(bid.type)
        if not group:
            self.fill_field_and_check_value_click_on_focus(self.date_finish, bid.date_finish, self.page_title)

    def fill_required_fields_client_direct_client(self, bid: Bid, group=False):
        self.fill_field_and_check_value_click_on_focus(self.contract_number, bid.number, self.page_title)
        Loaders(self.browser).wait_until_agent_loader_disappear()
        self.fill_field_and_check_value_click_on_focus(self.contract_price, bid.final_price, self.page_title)
        self.select_type(bid.type)
        if not group:
            self.fill_field_and_check_value_click_on_focus(self.date_finish, bid.date_finish, self.page_title)

    def click_on_create_bid_btn(self):
        self.find_element_by_locator(self.create_btn).click()

    def get_guarantee_price_value(self):
        return self.get_field_value(self.guarantee_price)

    def fill_required_field_group(self, bid):
        self.click_on_elem(self.select_btn)
        self.click_on_elements(self.select_list_elements, click_on_first=False)
        self.fill_field(self.date_end_group, bid.date_finish)
        # self.fill_fields(self.date_end_group, bid.date_finish, focus_locator=self.days_count_group_txt)

    def fill_guarantee_price_field(self, bid):
        self.clear_field(self.guarantee_price)
        self.fill_field(self.guarantee_price, bid.guarantee_price)

    def fill_administration(self, administration: Administration):
        agent_questionnaire = AgentQuestionnaire(self.browser)
        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_structure)
        info_about_structure = InfoAboutAdministration(self.browser)
        info_about_structure.fill_required_fields_administration(administration)
        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_structure)


class CreateBidForm(BasePage):
    form = '.b-popup__win'
    go_to_bid_btn = '//button[text()[contains(.,"Перейти к заявке")]]'
    commission = '.g-text-danger'
    bank = '//p[text()[contains(.,"Банк заявки")]]/b'
    banks_list = '//h3[text()[contains(.,"Список банков")]]'
    bid_id = '.b-popup__win .g-text-lg.g-text-secondary'

    def check_open(self, time=40):
        self.wait_until_located(self.form, time=time)

    def change_bank(self, new_bank):
        change_bank_item_locator = '//label[text()[contains(.,"' + new_bank + '")]]'
        self.click_on_elem(self.bank)
        self.wait_until_located(self.banks_list, 'xpath')
        self.click_on_elem(change_bank_item_locator)
        self.wait_until_located(self.go_to_bid_btn, 'xpath')

    def __get_values_for_group(self, locator):
        elements = self.find_elements_by_locator(locator)
        values = []
        for elem in elements:
            values.append(self.get_text(elem=elem))
        return values

    def get_commission_for_group(self):
        return self.__get_values_for_group(self.commission)

    def get_banks_for_group(self):
        return self.__get_values_for_group(self.bank)

    def get_bid_id_for_group(self):
        return self.__get_values_for_group(self.bid_id)

    def get_bid_id(self):
        return self.get_text(self.bid_id).replace("Ваша заявка №", "").replace(" предварительно одобрена!", "")

    def check_form_data(self, bid: Bid, bank="Экспобанк"):
        self.assertEqual(self.get_text(self.commission), bid.commission)
        self.assertEqual(self.get_text(self.bank), bank)

    def go_to_bid(self):
        self.wait_until_clickable(self.go_to_bid_btn, 'xpath')
        self.click_on_elem(self.go_to_bid_btn)
        return AgentQuestionnaire(self.browser)


class AgentQuestionnaire(BasePage):
    bid_number = "//div[contains(@class, 'b-aside__content')]//h1"
    profile = '//span[text()[contains(.,"Анкетирование")]]'
    finance = '//span[text()[contains(.,"Финансовая отчетность")]]'
    docs = '//span[text()[contains(.,"Пакет документов")]]'
    offer = '//span[text()[contains(.,"Предложение")]]'
    surety = '//span[text()[contains(.,"Поручительство")]]'

    info_about_guarantee = '//div[text()[contains(.,"Сведения о гарантии, контракте и заказчике")]]'
    info_about_client = '//div[text()[contains(.,"Сведения о клиенте")]]'
    info_about_structure = '//div[text()' \
                           '[contains(.,"Информация о структуре и персональном составе органов управления")]]'
    info = '//div[text()[contains(.,"Прочие сведения")]]'
    info_about_beneficiary = '//div[text()[contains(.,"Сведения о бенефициарных владельцах")]]'
    info_about_surety = '//div[text()[contains(.,"Сведения о поручителе")]]'

    def check_open(self):
        self.wait_until_located(self.info_about_guarantee, 'xpath')

    def get_bid_number(self):
        self.wait_until_located(self.bid_number, 'xpath')
        text = self.get_text(self.bid_number)
        return text.replace('Заявка № ', "")

    def check_section_disabled(self, section_locator):
        attr = self.find_element_by_locator(section_locator).get_attribute('class')
        self.assertIn('disabled-section', attr)

    def open_docs_section(self):
        self.click_on_elem(self.docs)
        return DocsPage(self.browser)

    def open_surety_section(self):
        self.click_on_elem(self.surety)
        surety_page = SuretyPage(self.browser)
        surety_page.check_open()
        return surety_page

    def open_surety(self, surety_number):
        surety_locator = f'//span[text()[contains(.,"Поручитель {str(surety_number)}")]]'
        self.click_on_elem(surety_locator)
        inside_surety = InsideSurety(self.browser)
        return InsideSurety(self.browser)


class SuretyPage(BasePage):
    UR = '//label[text()[contains(.,"Юридическое лицо")]]//span'
    IP = '//label[text()[contains(.,"Индивидуальный предприниматель")]]//input'
    FIZ = '//label[text()[contains(.,"Физическое лицо")]]//input'
    inn = '[placeholder="Введите инн поручителя"]'
    add_btn = '//button[text()[contains(.,"Добавить поручителя")]]'

    def check_open(self):
        self.wait_until_located(self.UR, 'xpath')

    def add_ur_surety(self, inn):
        self.click_on_elem(self.UR)
        self.fill_field(self.inn, inn)
        self.click_on_elem(self.add_btn)


class InsideSurety(BasePage):
    document_type_select = '[data-vv-as="Вид ДУЛ"]'
    buh = '[name="doc_client_buh_report"]'
    doc_client_locate_fact = '[name="doc_client_locate_fact"]'
    doc_buh_year = '[name="doc_bug_year_report"]'
    passport = '[name="doc_individual_identity_document"]'
    ee = '[name="doc_order_current_redaction"]'
    doc_nomination = '[name="doc_executor_nomination"]'
    doc_tax = '[name="doc_tax_return"]'
    docs_order = '[name="doc_order_current_redaction"]'
    doc_order_for_executor_nomination = '[name="doc_order_for_executor_nomination"]'

    def fill_fields_surety_ur(self, bank_account: BankAccount, beneficiary: Beneficiary,
                              administration: Administration):
        agent_questionnaire = AgentQuestionnaire(self.browser)
        self.wait_until_located(agent_questionnaire.info_about_surety, 'xpath')
        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_surety)
        info_about_client_form = InfoAboutClientForm(self.browser)
        info_about_client_form.fill_required_fields_bank_account(bank_account)
        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_surety)

        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_beneficiary)
        beneficiary_form = BeneficiaryForm(self.browser)
        beneficiary_form.fill_phone_number(beneficiary)
        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_beneficiary)

        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_structure)
        info_about_structure = InfoAboutAdministration(self.browser)
        self.select_elem(self.document_type_select, 'Паспорт РФ')
        info_about_structure.fill_required_fields_administration(administration)

    def load_docs(self, filename, surety_number):
        agentquestionnaire = AgentQuestionnaire(self.browser)
        agentquestionnaire.click_on_elem_with_number(agentquestionnaire.docs, surety_number)
        file_path = Base().get_file_dir('files', filename)
        docs_page = DocsPage(self.browser)
        self.wait_until_located(self.buh)
        docs_page.load_doc(self.buh, file_path)
        docs_page.load_doc(self.doc_client_locate_fact, file_path)
        docs_page.load_doc(self.doc_buh_year, file_path)
        docs_page.load_doc(self.passport, file_path)
        docs_page.load_doc(self.docs_order, file_path)
        docs_page.load_doc(self.doc_nomination, file_path)
        docs_page.load_doc(self.doc_tax, file_path)
        docs_page.load_doc(self.doc_order_for_executor_nomination, file_path)


class InfoAboutClientForm(BasePage):
    """Сведения о клиенте"""
    bank_account_number = '//label[text()[contains(.,"Расчетный счет")]]/following-sibling::input'
    bank_bik = '[placeholder="БИК банка"]'
    contact_fio = '[placeholder="Контактное лицо"]'
    contact_email = '[placeholder="Контактный email"]'
    contact_phone_number = '[placeholder="Контактный телефон"]'

    workers_count_select = '[placeholder="Кол-во сотрудников"]'
    work_with_bank_select = '//select[@data-vv-as="Доля"][@name="entity.term_work_with_bank"]'
    share_largest_buyer_select = '//select[@data-vv-as="Доля"][@name="entity.share_largest_buyer"]'
    property_availability_select = '//select[@data-vv-as="Наличие недвижимости"]'

    def fill_OTP_required_fields(self, dict: BankAccountOtp):
        self.fill_field(self.workers_count_select, dict.workers_count)
        self.fill_field(self.work_with_bank_select, dict.work_with_bank)
        self.fill_field(self.share_largest_buyer_select, dict.share_largest_buyer)
        self.fill_field(self.property_availability_select, dict.property_availability)

        self.fill_required_fields_bank_account(dict)

    def fill_required_fields_bank_account(self, bank_account: BankAccount):
        self.fill_field(self.bank_account_number, bank_account.bank_account_number)
        self.fill_field(self.bank_bik, bank_account.bank_bik)
        self.fill_field(self.contact_fio, bank_account.contact_fio)
        self.fill_field(self.contact_email, bank_account.contact_email)
        self.fill_field(self.contact_phone_number, bank_account.contact_phone_number)

    def check_open(self):
        self.wait_until_clickable(self.bank_bik)


class CommonPage(BasePage):
    gender_select = '//select[@data-vv-as="Пол"][not(@disabled)]'
    birth_place = '//div/input[@data-vv-as="Место рождения"][not(@disabled)]'
    birth_date = '//div[@data-vv-as="Дата рождения"]/input[not(@disabled)]'
    passport_series = '//div/input[@data-vv-as="Серия"][not(@disabled)]'
    passport_number = '//div/input[@data-vv-as="Номер"][not(@disabled)]'
    passport_date_out = '//div[@data-vv-as="Дата выдачи"]/input[not(@disabled)]'
    passport_code = '//div/input[@data-vv-as="Код подразделения"][not(@disabled)]'
    passport_who_give = '//div/input[@data-vv-as="Кем выдан"][not(@disabled)]'
    registration_address = '//label[text()[contains(.,"Адрес регистрации")]]/following-sibling::div/div/input[not(@disabled)]'
    fact_address = '//label[text()[contains(.,"актическ")]]/following-sibling::div/div/input[not(@disabled)]'
    inn = '//div/input[@data-vv-as="ИНН"][not(@disabled)]'
    fio = '//input[@data-vv-as="ФИО"][not(@disabled)]'

    def fill_required_fields(self, entity, form):
        self.select_elem(form + self.gender_select, entity.gender, form)
        self.fill_field(form + self.birth_date, entity.birth_date)
        self.fill_field(form + self.birth_place, entity.birth_place)
        self.wait_until_disappear(BeneficiaryForm(self.browser).success_add_beneficiary, 'css')
        self.click_on_elem(form + self.passport_date_out)  # снять фокус
        self.fill_field(form + self.passport_series, entity.passport_series)
        self.fill_field(form + self.passport_number, entity.passport_number)
        self.wait_until_clickable(form + self.passport_date_out, 'xpath')
        sleep(0.3)
        self.fill_field(form + self.passport_date_out, entity.passport_date_out)
        self.fill_field(form + self.passport_code, entity.passport_code)
        self.fill_field(form + self.passport_who_give, entity.passport_who_give)
        self.fill_field(form + self.registration_address, entity.registration_address)
        self.click_on_elem(form + self.passport_date_out)  # снять фокус
        self.fill_field(form + self.fact_address, entity.fact_address)

    def fill_inn(self, entity, form):
        self.fill_field(form + self.inn, entity.inn)


class BeneficiaryForm(BasePage):
    contact_information = '//input[@placeholder="Укажите контактные данные"]'
    form = '//div[text()[contains(.,"Сведения о бенефициарных владельцах")]]/..'
    add_beneficiary_btn = '//button[text()[contains(.,"Добавить бенефициара")]]'
    beneficiary_part = '//div/input[@data-vv-as="Доля"][not(@disabled)]'
    beneficiary_fio = '//div/input[@data-vv-as="ФИО"][not(@disabled)]'
    success_add_beneficiary = '.toast-success'
    beneficiary_inn = '//div/input[@data-vv-as="ИНН"][not(@disabled)]'

    def add_beneficiary(self):
        self.click_on_elem(self.add_beneficiary_btn)
        self.wait_until_located(self.success_add_beneficiary, 'css')

    def fill_required_fields_beneficiary(self, beneficiary: Beneficiary):
        CommonPage(self.browser).fill_required_fields(beneficiary, self.form)
        self.fill_field(self.contact_information, beneficiary.contact_information)

    def fill_required_fields_Credit_Europe(self, beneficiary: Beneficiary):
        CommonPage(self.browser).fill_inn(beneficiary, self.form)
        CommonPage(self.browser).fill_required_fields(beneficiary, self.form)
        self.fill_field(self.contact_information, beneficiary.contact_information)

    def fill_beneficiary_fio(self, beneficiary: Beneficiary):
        locator = self.form + self.beneficiary_fio
        self.fill_field(locator, beneficiary.fio)
        self.click_on_elem(self.contact_information)  # фокус

    def fill_required_fields_beneficiary_by_number(self, beneficiary: Beneficiary, beneficiary_number):
        self.fill_field_by_elem(self.find_elements_by_locator(self.contact_information)[beneficiary_number - 1],
                                beneficiary.contact_information)

        common = CommonPage(self.browser)
        man_option = '//div[text()[contains(.,"Сведения о бенефициарных владельцах")]]/..//select[@data-vv-as="Пол"][not(@disabled)]//option[2]'
        select_locator = self.form + common.gender_select
        self.click_on_elem(select_locator)
        self.click_on_elem(man_option)

        self.fill_field(self.form + common.birth_date,
                        beneficiary.birth_date)
        self.fill_field(self.form + common.birth_place,
                        beneficiary.birth_place)
        self.fill_field(self.form + common.passport_series,
                        beneficiary.passport_series)
        self.fill_field(
            self.form + common.passport_number,
            beneficiary.passport_number)
        sleep(0.3)
        self.fill_field(
            self.form + common.passport_date_out,
            beneficiary.passport_date_out)
        self.fill_field(self.form + common.passport_code,
                        beneficiary.passport_code)
        self.fill_field(
            self.form + common.passport_who_give,
            beneficiary.passport_who_give)
        self.fill_field(
            self.form + common.registration_address,
            beneficiary.registration_address)
        self.click_on_elem(self.form + common.birth_place)  # снять фокус
        self.fill_field(self.form + common.fact_address,
                        beneficiary.fact_address)

    def fill_phone_number(self, beneficiary: Beneficiary):
        self.fill_field(self.contact_information, beneficiary.contact_information)


class InfoAboutAdministration(BasePage):
    form = '//div[text()[contains(.,"Информация о структуре и персональном составе органов управления")]]/..'
    role = '[data-vv-as="Должность ЕИО"]'
    add_holder_btn = '//button[text()[contains(.,"Добавить")]]'
    holder_name = '[data-vv-as="Наименование акционера"]'
    holder_inn = '//input[@placeholder="ИНН"]'
    save_btn = '//button[text()[contains(.,"Сохранить")]]'

    def fill_required_fields_administration(self, administration):
        CommonPage(self.browser).fill_required_fields(administration, self.form)
        administration.fio = self.get_field_value(self.form + CommonPage(self.browser).fio)
        administration.inn = self.get_field_value(self.form + CommonPage(self.browser).inn)
        administration.role = self.get_field_value(self.role)

    def add_holder(self, name='test name', inn='772096797832'):
        self.click_on_elem(self.form + self.add_holder_btn)
        self.wait_until_clickable(self.holder_name)
        self.fill_field(self.holder_name, name)
        self.fill_field(self.form + self.holder_inn, inn)
        self.click_on_elem(self.save_btn)
        self.wait_until_disappear(self.save_btn, 'xpath')


class Finance(BasePage):
    balance1210 = '//input[contains(@name, "fin_1210_0")][not(@disabled)]'  # todo css->xpath+find usages
    balance1510 = '//input[contains(@name, "fin_1510_0")][not(@disabled)]'
    earnings2110 = '//input[contains(@name, "fin_2110_0")][not(@disabled)]'
    fill_manual_btn = '//button[text()[contains(.,"Заполнить вручную")]]'

    def check_open(self):
        self.wait_until_located(self.balance1510, 'xpath')

    def check_open_otp_express(self):
        self.wait_until_located(self.fill_manual_btn, 'xpath')

    def fill_required_fields_finance(self, finance):
        self.fill_field(self.balance1210, finance['balance1600'])
        self.fill_field(self.balance1510, finance['balance1700'])
        self.fill_field(self.earnings2110, finance['earnings2110'])

    def fill_manual(self):
        self.wait_until_clickable(self.fill_manual_btn, 'xpath')
        self.click_on_elem(self.fill_manual_btn)
        self.wait_until_located(self.balance1210, 'xpath')


class DocsPage(BasePage):
    buh = '[id="file_doc_client_buh_reportnull"]'
    doc_client_locate_fact = '[id="file_doc_client_locate_factnull"]'
    doc_buh_year = '[id="file_doc_bug_year_reportnull"]'
    passport = '[id="file_doc_individual_identity_documentnull"]'
    passport_ur = '[data-vv-name="doc_individual_identity_document"]'
    docs_order = '[id="file_doc_order_current_redactionnull"]'
    doc_decision = '[id="file_doc_executor_nominationnull"]'
    doc_nomination = '[id="file_doc_order_for_executor_nominationnull"]'
    doc_tax = '[id="file_doc_tax_returnnull"]'
    copy_link_btn = '//button[text()[contains(.,"Скопировать ссылку для подписи")]]'
    link = '.b-note'
    tax_result_btn = '//span[text()[contains(.,"Налоговая")]]/../following-sibling::div//a[text()[contains(.,"Загружен, скачать")]]'
    passport_result_btn = '//span[text()[contains(.,"Паспорт")]]/../following-sibling::div//a[text()[contains(.,"Загружен, скачать")]]'
    decision_result_btn = '//span[text()[contains(.,"Решение")]]/../following-sibling::div//a[text()[contains(.,"Загружен, скачать")]]'
    sign_btn = '//button[text()[contains(.,"Подписать")]]'
    submit_btn = '//button[text()[contains(.,"Подать заявку")]]'
    sign_and_submit_btn = '//button[text()[contains(.,"Подписать и передать в банк")]]'
    msp_passport_load_btn = '[id="file_doc_identity_documentnull"]'
    load_doc_btn = '[data-vv-name="doc_identity_document"]'
    anketa_loaded_download = '//a[text()[contains(.,"Загружен, скачать")]]'
    doc_accept_deal = '[id="file_doc_accept_dealnull"]'
    doc_registry_ordering_AO_btn = '[data-vv-name="doc_registry_ordering"]'
    doc_registry_ordering_AO_file = '[id="file_doc_registry_orderingnull"]'
    docs_upload_btns = ".upload-label"
    eds_btn = '//button[text()[contains(.,"Загрузить файлы с подписью")]]'

    def check_anketa_generated(self):
        self.wait_until_located(self.anketa_loaded_download, 'xpath')

    def get_docs_count(self):
        return len(self.find_elements_by_locator(self.docs_upload_btns))

    def submit(self, time=50):
        self.wait_until_clickable(self.submit_btn, 'xpath')
        self.click_on_elem(self.submit_btn)
        Loaders(self.browser).wait_until_agent_loader_disappear(time)

    def check_open(self):
        self.wait_until_located(self.copy_link_btn, 'xpath')

    def check_open_express(self):
        self.wait_until_located(self.submit_btn, 'xpath')

    def check_open_direct_client(self):
        self.wait_until_located(self.sign_and_submit_btn, 'xpath')

    def load_doc(self, locator, file_path):
        self.scroll_into_view(locator)
        self.find_element_by_locator(locator).send_keys(file_path)

    def load_passport(self, filename, btn_locator=passport):
        file_path = Base().get_file_dir('files', filename)
        self.wait_until_located(self.anketa_loaded_download, 'xpath')
        self.assertEqual(self.get_docs_count(), 1)
        self.load_doc(btn_locator, file_path)
        self.wait_until_located(self.passport_result_btn, 'xpath')

    def load_passport_msp(self, filename):
        file_path = Base().get_file_dir('files', filename)
        self.wait_until_located(self.anketa_loaded_download, 'xpath')
        self.assertEqual(self.get_docs_count(), 1)
        self.load_doc(self.msp_passport_load_btn, file_path)
        self.wait_until_located(self.passport_result_btn, 'xpath')

    def load_docs_for_usual_bid(self, filename):
        file_path = Base().get_file_dir('files', filename)
        self.wait_until_located(self.buh)
        self.assertEqual(self.get_docs_count(), 8)
        self.load_doc(self.buh, file_path)
        self.load_doc(self.doc_client_locate_fact, file_path)
        self.load_doc(self.doc_buh_year, file_path)
        self.load_doc(self.passport, file_path)
        self.load_doc(self.docs_order, file_path)
        self.load_doc(self.doc_decision, file_path)
        self.load_doc(self.doc_nomination, file_path)
        self.load_doc(self.doc_tax, file_path)
        self.wait_until_located(self.tax_result_btn, 'xpath')

    def load_docs_for_usual_bid_ip(self, filename):
        file_path = Base().get_file_dir('files', filename)
        self.wait_until_located(self.buh)
        self.assertEqual(self.get_docs_count(), 4)
        self.load_doc(self.buh, file_path)
        self.load_doc(self.doc_client_locate_fact, file_path)
        self.load_doc(self.msp_passport_load_btn, file_path)
        self.load_doc(self.doc_tax, file_path)
        self.wait_until_located(self.tax_result_btn, 'xpath')

    def load_docs_for_OTP_usual(self, filename):
        file_path = Base().get_file_dir('files', filename)
        self.wait_until_located(self.buh)
        self.assertEqual(self.get_docs_count(), 8)
        self.load_doc(self.buh, file_path)
        self.load_doc(self.doc_buh_year, file_path)
        self.load_doc(self.doc_tax, file_path)
        self.load_doc(self.passport, file_path)
        self.load_doc(self.docs_order, file_path)
        self.load_doc(self.doc_decision, file_path)
        self.load_doc(self.doc_client_locate_fact, file_path)
        self.load_doc(self.doc_accept_deal, file_path)
        self.wait_until_located(self.decision_result_btn, 'xpath')

    def load_docs_for_OTP_express(self, filename):
        file_path = Base().get_file_dir('files', filename)
        self.wait_until_located(self.passport)
        self.assertEqual(self.get_docs_count(), 2)
        self.load_doc(self.passport, file_path)
        self.load_doc(self.doc_buh_year, file_path)
        self.wait_until_clickable(self.submit_btn, 'xpath')

    def load_docs_for_group(self, filename):
        file_path = Base().get_file_dir('files', filename)
        self.wait_until_located(self.buh)
        self.assertEqual(self.get_docs_count(), 3)
        self.load_doc(self.buh, file_path)
        self.load_doc(self.passport, file_path)
        self.load_doc(self.doc_buh_year, file_path)
        self.wait_until_located(self.passport_result_btn, 'xpath')

    def check_open_sign_link_for_usual(self):
        # todo убрать в OfferForm
        sleep(1.5)
        self.wait_until_located(self.copy_link_btn, 'xpath')
        self.click_on_elem(self.copy_link_btn)
        self.wait_until_located(self.link)
        link_common = self.find_element_by_locator(self.link).text
        self.open_new_window()
        self.browser.switch_to.window(self.browser.window_handles[1])
        try:
            link_basic = LoginPage.basic_url + link_common.replace(
                'Ссылка для подписания заявки скопирована в буфер обмена https://',
                "")
            self.browser.get(link_basic)
            self.wait_until_located(self.sign_btn, locator_type='xpath', time=5)
        except:
            link_no_basic = link_common.replace('Ссылка для подписания заявки скопирована в буфер обмена ', "")
            self.browser.get(link_no_basic)
            self.wait_until_located(self.sign_btn, locator_type='xpath', time=5)
        self.close_current_tab()
        self.browser.switch_to.window(self.browser.window_handles[0])

    def load_doc_registry_ordering_AO(self, filename):
        self.wait_until_clickable(self.doc_registry_ordering_AO_btn, 'css')
        self.assertEqual(self.get_docs_count(), 2)
        file_path = Base().get_file_dir('files', filename)
        self.load_doc(self.doc_registry_ordering_AO_file, file_path)

    def open_EDS(self):
        self.wait_until_clickable(self.eds_btn, 'xpath')
        self.click_on_elem(self.eds_btn)
        eds_form = EDS(self.browser)
        eds_form.check_opened()
        return eds_form


class EDS(BasePage):
    form = '//h3[text()[contains(.,"Загрузка подписанных документов")]]/..'
    anketa = '#sig_file_doc_anketa'
    buh = '#sig_file_doc_client_buh_report'
    locate_fact = '#sig_file_doc_client_locate_fact'
    passport = '#sig_file_doc_identity_document'
    tax = '#sig_file_doc_tax_return'
    transfer_to_bank_btn = '//button[text()[contains(.,"Передать в банк")]]'

    def check_opened(self):
        self.wait_until_located(self.form, 'xpath')

    def load_ip_usual_docs(self, filename):
        file_path = Base().get_file_dir('files', filename)
        DocsPage(self.browser).load_doc(self.anketa, file_path)
        DocsPage(self.browser).load_doc(self.buh, file_path)
        DocsPage(self.browser).load_doc(self.locate_fact, file_path)
        DocsPage(self.browser).load_doc(self.passport, file_path)
        DocsPage(self.browser).load_doc(self.tax, file_path)
        self.wait_until_clickable(self.transfer_to_bank_btn, 'xpath')
        self.click_on_elem(self.transfer_to_bank_btn)
        self.wait_until_disappear(self.transfer_to_bank_btn, 'xpath')
        Loaders(self.browser).wait_until_agent_loader_disappear()


class CommissionForm(BasePage):
    accept_btn = '//button[text()[contains(.,"Принять")]]'
    commission = '//label[text()[contains(.,"Сумма комиссии")]]/following-sibling::input'
    agent_discount = '//label[text()[contains(.,"Скидка за счет вашего КВ")]]/following-sibling::input'
    elevation = '//label[text()[contains(.,"Превышение")]]/following-sibling::input'

    def check_open(self):
        self.wait_until_located(self.accept_btn, locator_type='xpath')
        Loaders(self.browser).wait_until_agent_loader_disappear()

    def accept_commission(self):
        self.wait_until_clickable(self.accept_btn, 'xpath')
        self.click_on_elem(self.accept_btn)
        self.wait_until_disappear(self.accept_btn, locator_type='xpath')

    def check_closed(self):
        self.wait_until_disappear(self.accept_btn, locator_type='xpath')

    def fill_elevation(self, number):
        self.fill_field(self.elevation, number)

    def fill_agent_discount(self, discount):
        self.fill_field(self.agent_discount, discount)

    def check_main_fields(self, commission, discount, elevation):
        self.assertEqual(commission.replace(" ", "").replace(",", "."),
                         self.get_field_value(self.commission))
        self.assertEqual(discount.replace(",", "."),
                         self.get_field_value(self.agent_discount))
        self.assertEqual(elevation,
                         self.get_field_value(self.elevation))


class OfferForm(BasePage):
    copy_link_btn = '//button[text()[contains(.,"Скопировать ссылку для подписи")]]'
    link = '.b-note'
    sign_btn = '//button[text()[contains(.,"Подписать")]]'
    otp_confirm_btn = '//button[text()[contains(.,"Подтвердить")]]'
    otp_yes_btn = '//button[text()[contains(.,"Да")]]'

    def check_open(self):
        self.wait_until_located(self.copy_link_btn, 'xpath')

    def check_open_sign_link(self):
        sleep(1.5)
        self.wait_until_located(self.copy_link_btn, 'xpath')
        self.click_on_elem(self.copy_link_btn)
        self.wait_until_located(self.link)
        link_common = self.find_element_by_locator(self.link).text
        self.open_new_window()
        self.browser.switch_to.window(self.browser.window_handles[1])
        try:
            link_basic = LoginPage.basic_url + link_common.replace(
                'Ссылка для подписания заявки скопирована в буфер обмена https://',
                "")
            self.browser.get(link_basic)
            self.wait_until_located(self.sign_btn, locator_type='xpath', time=5)
        except:
            link_no_basic = link_common.replace('Ссылка для подписания заявки скопирована в буфер обмена ', "")
            self.browser.get(link_no_basic)
            self.wait_until_located(self.sign_btn, locator_type='xpath', time=5)
        self.close_current_tab()
        self.browser.switch_to.window(self.browser.window_handles[0])

    def confirm_otp_express(self):
        self.click_on_elem(self.otp_confirm_btn)
        self.wait_until_located(self.otp_yes_btn, 'xpath')
        self.click_on_elem(self.otp_yes_btn)
        self.wait_until_disappear(self.otp_yes_btn, 'xpath')


class StockholderForm(BasePage):
    percentage = '[name="actioner.share.percentagePlain"]'
    edit_btn = '//button[text()[contains(.,"Редактировать")]]'
    save_btn = '//button[text()[contains(.,"Сохранить")]]'

    def add_percentage_to_exist_stockholder(self, stockholder: Stockholder):
        elems = self.find_elements_by_locator(self.edit_btn)
        elems[stockholder.number - 1].click()
        self.wait_until_clickable(self.percentage)
        self.fill_field(self.percentage, stockholder.percentage)
        self.click_on_elem(self.save_btn)
        self.wait_until_disappear(self.save_btn, 'xpath')


class LoginPage(BasePage):
    login = '[placeholder="Логин"]'
    password = '[placeholder="Пароль"]'
    enter = '//button[text()[contains(.,"войти")]]'

    with open("config_connections.json") as json_data_file:
        connections_data = json.load(json_data_file)
        stand = connections_data['stand']

    basic_url = 'https://' + connections_data['basic_user']['username'] + ':' + connections_data['basic_user'][
        'password'] + '@'
    url = 'https://' + connections_data['basic_user']['username'] + ':' + connections_data['basic_user'][
        'password'] + '@' + stand + '/login'

    def go_to_login_page_and_clear_cache(self, new_url=None):
        self.browser.get('chrome://settings/clearBrowserData')
        actions = ActionChains(self.browser)
        actions.send_keys(Keys.TAB)
        time = 0.2
        sleep(time)
        actions.send_keys(Keys.TAB)
        sleep(time)
        actions.send_keys(Keys.TAB)
        sleep(time)
        actions.send_keys(Keys.TAB)
        sleep(time)
        actions.send_keys(Keys.TAB)
        sleep(time)
        actions.send_keys(Keys.TAB)
        sleep(time)
        actions.send_keys(Keys.TAB)
        sleep(time)
        actions.send_keys(Keys.ENTER)
        sleep(time)

        actions.perform()
        sleep(time)
        if new_url is not None:
            self.browser.get(new_url)
        else:
            self.browser.get(self.url)
        self.wait_until_located(self.enter, 'xpath')
        self.find_element_by_locator(self.enter)

    def login_as_direct_client(self):
        self.log_in(self.connections_data['direct_client'])
        return AgentPage(self.browser)

    def login_as_agent(self):
        self.log_in(self.connections_data['agent'])
        agent_page = AgentPage(self.browser)
        agent_page.check_open()
        return agent_page

    def login_as_bank(self):
        self.log_in(self.connections_data['bank'])
        bank_page = BankPage(self.browser)
        bank_page.check_open()
        return bank_page

    def log_in(self, user):
        self.find_element_by_locator(self.login).send_keys(user.get('username'))
        self.find_element_by_locator(self.password).send_keys(user.get('password'))
        self.find_element_by_locator(self.enter).click()

    def get_login_url(self, stand, basic_username, basic_password):
        return 'https://' + basic_username + ':' + basic_password + '@' + stand + '/login'

    def login_as_agent_preprod(self):
        self.log_in(self.connections_data['agent_preprod'])

    def login_as_bank_preprod(self):
        self.log_in(self.connections_data['bank_preprod'])
