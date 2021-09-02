import json
import unittest
from time import sleep

from selenium import webdriver

from Pages.AgentPages import AgentPage, CreateBidPage, CreateBidForm, AgentQuestionnaire, InfoAboutClientForm, \
    BeneficiaryForm, InfoAboutAdministration, Finance, DocsPage, OfferForm, StockholderForm, CommissionForm, LoginPage, \
    EDS
from Pages.Api import AgentApi
from Pages.BankPages import BankPage, BankBidCommonPage, ProfilePage, BidOfferPage, GeneralForm, CommissionExpoForm, \
    ExceedingForm
from Pages.BasePages import DatabaseConnect, BasePage, Loaders

from classes.entities import Bid, BankAccount, BankAccountOtp, Beneficiary, Administration, BankBidBasic, Client, \
    Customer, Commission, BankBidInfoAccordion, BankBidInfoAboutClientAccordion, BankBidInfoAboutStructure, \
    Stockholder, CommissionExpo, BidType, BidLaw
from parameterized import parameterized


class TestMainWaysCheck(unittest.TestCase):
    browser = None

    @classmethod
    def setUpClass(cls):
        database_connect = DatabaseConnect()
        cls.database_connect = database_connect
        cls.browser = BasePage(cls.browser).make_settings_and_return_driver()

    # @unittest.skip("test")
    def testUsualBidWay(self):
        """Обычная заявка больше 10 млн"""
        with open("files/stop_factors_usual_entity.json", encoding='utf-8') as json_data_file:
            stop_factors = json.load(json_data_file)
        bid = Bid("0320100018021000009", "67 874 332.8", "20 362 299.84", "2 582 921.47", 1429,
                  BidType.execution, "25.03.2021",
                  "Выполнение работ по противопаводковым мероприятиям на объекте: "
                  "Сиваковский межхозяйственный магистральный канал, "
                  "с. Сиваковка, Хорольского района, Приморского края (правая дамба канала)",
                  region="Российская Федерация, Приморский край, Хорольский р-н, Сиваковка с")
        bank_account = BankAccount()
        beneficiary = Beneficiary()
        administration = Administration()
        fin = {
            "balance1600": 1000,
            "balance1700": 1000,
            "earnings2110": 3000
        }
        commission = CommissionExpo("3,24", "3,24", "3,24", bid.days_count, "0", "0", "2582921,47", "0,00",
                                    "2 582 921,47")
        client = Client("2312150358", "1082312005456", "231201001",
                        "Общество с ограниченной ответственностью \"Кейсистемс-Кубань\"", "ООО \"Кейсистемс-Кубань\"",
                        "350018, край Краснодарский, г Краснодар, ул Сормовская, дом 7, литера Г, пом 163/3",
                        "12300", "03701000001", "62.01")
        principal = Customer(
            "ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ \"УПРАВЛЕНИЕ МЕЛИОРАЦИИ"
            " ЗЕМЕЛЬ И СЕЛЬСКОХОЗЯЙСТВЕННОГО ВОДОСНАБЖЕНИЯ ПО ПРИМОРСКОМУ И ХАБАРОВСКОМУ КРАЯМ\"",
            "690091, край Приморский, г Владивосток, ул Прапорщика Комарова, дом 21",
            "1022501285993", "2536042398", "253601001", "05701000001", "Приморский край", "16.01.1995")
        self.database_connect.cleanup_data_by_inn(client.inn)

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        agent_page = login_page.login_as_agent()

        self.bid_id = agent_page.create_bid(bid, client, bank_account, beneficiary, administration)

        agent_questionnaire = AgentQuestionnaire(self.browser)
        agent_questionnaire.click_on_elem(agent_questionnaire.finance)

        finance_page = Finance(self.browser)
        finance_page.check_open()
        finance_page.fill_required_fields_finance(fin)

        agent_questionnaire.click_on_elem(agent_questionnaire.docs)
        docs_page = DocsPage(self.browser)
        docs_page.load_docs_for_usual_bid('file.jpg')
        docs_page.check_open_sign_link_for_usual()

        agent_api = AgentApi()
        agent_api.upload_package_usual(self.bid_id, 'file.jpg.sig')
        agent_api.transfer_to_bank(self.bid_id)
        self.database_connect.check_bid_status(self.bid_id, 'Передано в Банк')

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        login_page.login_as_bank()

        bank_page = BankPage(self.browser)
        bank_page.check_open()
        bank_page.set_required_users(self.bid_id)
        bank_page.open_bid(self.bid_id)
        self.database_connect.check_bid_status(self.bid_id, 'Рассмотрение')
        bank_bid_common_page = BankBidCommonPage(self.browser)
        bank_bid_common_page.check_open()

        general_form_page = GeneralForm(self.browser)
        general_form_page.check_bank_accordion_data(BankBidBasic(bid, principal, client))
        general_form_page.check_bank_accordion_data(BankBidInfoAccordion(bid, principal))
        general_form_page.check_bank_accordion_data(
            BankBidInfoAboutClientAccordion(client, bank_account, beneficiary))
        general_form_page.check_bank_accordion_data(BankBidInfoAboutStructure(administration))
        general_form_page.select_required_locators_for_usual()

        bank_bid_common_page.select_menu_item(bank_bid_common_page.prof_text)

        profile_page = ProfilePage(self.browser)
        profile_page.check_open()

        profile_page.check_stop_factors(stop_factors)
        profile_page.check_selected_default(stop_factors)
        profile_page.select_required_factors(stop_factors)
        profile_page.click_on_elem(profile_page.calculate_btn)
        profile_page.check_calculated()
        profile_page.check_ratings_results('2.58', 'B+', 'Хорошее')
        profile_page.use_rating()
        profile_page.generate_doc_by_name('Профсуждение')
        profile_page.generate_doc_by_name('Отчет о проверке и идентификации клиента')
        profile_page.generate_doc_by_name('Решение о выпуске БГ')

        self.database_connect.check_bid_status(self.bid_id, 'Рассмотрение')
        self.database_connect.change_bid_status(self.bid_id, 'Формирование предложения')
        self.database_connect.check_bid_status(self.bid_id, 'Формирование предложения')

        self.browser.refresh()
        bank_bid_common_page.check_open()
        bank_bid_common_page.select_menu_item(bank_bid_common_page.proposal_text)
        bid_offer_page = BidOfferPage(self.browser)
        bid_offer_page.check_open()
        bid_offer_page.select_signer()
        bid_offer_page.check_loaded()

        commission_form = CommissionExpoForm(self.browser)
        commission_form.check_tariff_expo(commission)
        bid_offer_page.send_to_client()
        self.database_connect.check_bid_status(self.bid_id, 'Предложение направлено')

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        login_page.login_as_agent()

        agent_page = AgentPage(self.browser)
        agent_page.check_open()
        agent_page.open_bid_use_filter(self.bid_id)

        commission_form = CommissionForm(self.browser)
        commission_form.check_open()
        commission_form.accept_commission()

        sign_page = DocsPage(self.browser)
        sign_page.check_open_sign_link_for_usual()

        agent_api.accept_proposal(self.bid_id, 'act.sig')
        self.database_connect.check_bid_status(self.bid_id, 'Предложение принято')

    def testExpressPlusBidWay(self):
        """Заявка Э+"""
        with open("files/stop_factors_express_plus.json", encoding='utf-8') as json_data_file:
            stop_factors = json.load(json_data_file)
        bid = Bid("0320100018021000009", "256 500", "256 500.00", "33 540.78", 1429,
                  BidType.execution, "25.03.2021",
                  "Выполнение работ по противопаводковым мероприятиям на объекте: Сиваковский межхозяйственный магистральный канал, с. Сиваковка, Хорольского района, Приморского края (правая дамба канала)",
                  region="Российская Федерация, Приморский край, Хорольский р-н, Сиваковка с",
                  start_price="67 874 332,80")
        bank_account = BankAccount()
        beneficiary = Beneficiary()
        administration = Administration()
        principal = Customer(inn="2536042398",
                             full_orgname="ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ \"УПРАВЛЕНИЕ МЕЛИОРАЦИИ ЗЕМЕЛЬ И СЕЛЬСКОХОЗЯЙСТВЕННОГО ВОДОСНАБЖЕНИЯ ПО ПРИМОРСКОМУ И ХАБАРОВСКОМУ КРАЯМ",
                             address="690091, край Приморский, г Владивосток, ул Прапорщика Комарова, дом 21",
                             ogrn="1022501285993", kpp="253601001", oktmo="05701000001", rf_subject="Приморский край",
                             tax_date_registration="16.01.1995")
        client = Client('2312150358', "1082312005456", "231201001",
                        "Общество с ограниченной ответственностью \"Кейсистемс-Кубань\"",
                        "ООО \"Кейсистемс-Кубань",
                        "350018, край Краснодарский, г Краснодар, ул Сормовская, дом 7, литера Г, пом 163/3",
                        "12300", "03701000001", "62.01")
        commission = CommissionExpo("3.34", "3,34", "3,34", "1429", "0", "0", "33 540,78", "0", "33 540,78")
        self.database_connect.cleanup_data_by_inn(client.inn)

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        agent_page = login_page.login_as_agent()

        self.bid_id = agent_page.create_bid(bid, client, bank_account, beneficiary, administration)

        docs_page = DocsPage(self.browser)
        docs_page.check_open_express()
        docs_page.load_passport('file.jpg')

        agent_api = AgentApi()
        agent_api.upload_package_passport_anketa(self.bid_id, 'file.jpg.sig')
        agent_api.transfer_to_bank(self.bid_id)
        agent_api.accept_proposal(self.bid_id, 'act.sig')

        self.database_connect.check_bid_status(self.bid_id, 'Верификация')

        self.browser.refresh()
        Loaders(self.browser).wait_until_agent_loader_disappear()

        # agent_questionnaire = AgentQuestionnaire(self.browser)
        # agent_questionnaire.check_open()
        # agent_questionnaire.check_section_disabled(agent_questionnaire.offer)

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        login_page.login_as_bank()

        bank_page = BankPage(self.browser)
        bank_page.check_open()
        bank_page.set_required_users(self.bid_id)
        bank_page.open_bid(self.bid_id)
        self.database_connect.check_bid_status(self.bid_id, 'Верификация')
        bank_bid_common_page = BankBidCommonPage(self.browser)
        bank_bid_common_page.check_open()

        general_form_page = GeneralForm(self.browser)
        general_form_page.check_bank_accordion_data(BankBidBasic(bid, principal, client))
        general_form_page.check_bank_accordion_data(BankBidInfoAccordion(bid, principal))
        general_form_page.check_bank_accordion_data(
            BankBidInfoAboutClientAccordion(client, bank_account, beneficiary))
        general_form_page.check_bank_accordion_data(BankBidInfoAboutStructure(administration))
        general_form_page.select_required_locators_without_finance()

        self.browser.refresh()
        bank_bid_common_page.check_open()
        bank_bid_common_page.select_menu_item(bank_bid_common_page.prof_text)

        profile_page = ProfilePage(self.browser)
        profile_page.check_open()
        profile_page.check_stop_factors(stop_factors)
        profile_page.check_selected_default(stop_factors)
        profile_page.select_required_factors(stop_factors)
        profile_page.click_on_elem(profile_page.calculate_btn)
        profile_page.check_calculated()
        profile_page.check_ratings_results('2.5', 'B', 'Среднее')
        profile_page.use_rating()
        profile_page.generate_doc_by_name('Профсуждение')
        profile_page.generate_doc_by_name('Отчет о проверке и идентификации клиента')
        profile_page.generate_doc_by_name('Решение о выпуске БГ')
        profile_page.approve_doc('Профсуждение')
        profile_page.approve_doc('Отчет о проверке и идентификации клиента')
        profile_page.approve_doc('Решение о выпуске БГ')
        sleep(10)
        self.database_connect.check_bid_status(self.bid_id, 'Предложение принято')
        self.browser.refresh()
        bank_bid_common_page.select_menu_item(bank_bid_common_page.proposal_text)
        bid_offer_page = BidOfferPage(self.browser)
        bid_offer_page.check_open()
        bid_offer_page.check_loaded()

        commission_form_expo = CommissionExpoForm(self.browser)
        commission_form_expo.check_tariff_expo(commission)

        bid_offer_page.check_success_company_data()
        bid_offer_page.transfer_to_sign('file.jpg')
        self.database_connect.check_bid_status(self.bid_id, 'Подписание банком')

    def testMSPipExpress(self):
        """Заявка Э+ путь МСП методика"""
        with open("files/stop_factors_msp_ip.json", encoding='utf-8') as json_data_file:
            stop_factors = json.load(json_data_file)
        bid = Bid("0338200005321000012", "344 433.5", "10 000.00", "5 013.7", 50,
                  BidType.execution, "23.04.2021", "Поставка лекарственных препаратов не ЖНВЛП",
                  "Российская Федерация, Камчатский край, Петропавловск-Камчатский г")
        client = Client('252691919497', "306250631900028", "", "ИП Бегматов Мирали Палвонович",
                        "ИП Бегматов Мирали Палвонович", "край Приморский, пгт Лучегорск, р-н Пожарский",
                        "50102", "05634151051", "43.3")
        principal = Customer(
            "Государственное бюджетное учреждение здравоохранения \"Камчатский краевой наркологический диспансер",
            "683024, край Камчатский, г Петропавловск-Камчатский, пр-кт 50 лет Октября, дом 2",
            "1024101036838",
            "4101036378", "410101001", "30701000001", "Камчатский край", "25.04.2000")

        bank_account = BankAccount()
        beneficiary = Beneficiary(birth_place="692001, Приморский край, Пожарский р-н, пгт Лучегорск",
                                  registration_address="край Приморский, пгт Лучегорск, р-н Пожарский")

        commission = CommissionExpo("5000", "366", "366,00", bid.days_count, "0", "0", "5013,70", "0", "5013,70")
        self.database_connect.cleanup_data_by_inn(client.inn)

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        agent_page = login_page.login_as_agent()

        self.bid_id = agent_page.create_bid_ip_and_get_bid_id(bid, client, bank_account, beneficiary)

        docs_page = DocsPage(self.browser)
        docs_page.check_open_express()
        docs_page.load_passport('file.jpg', docs_page.msp_passport_load_btn)
        # docs_page.submit()
        #
        # commission_form.check_open()
        # commission_form.accept_commission()
        #
        # self.database_connect.check_bid_status(self.bid_id, 'Предложение направлено')

        agent_api = AgentApi()
        agent_api.upload_package_passport_anketa(self.bid_id, 'file.jpg.sig', ip=True)
        agent_api.transfer_to_bank(self.bid_id)
        agent_api.accept_proposal(self.bid_id, 'act.sig')

        self.database_connect.check_bid_status(self.bid_id, 'Верификация')

        self.browser.refresh()
        commission_form = CommissionForm(self.browser)
        commission_form.check_closed()

        agent_questionnaire = AgentQuestionnaire(self.browser)
        agent_questionnaire.check_section_disabled(agent_questionnaire.offer)

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        login_page.login_as_bank()

        bank_page = BankPage(self.browser)
        bank_page.check_open()
        bank_page.set_required_users(self.bid_id)
        bank_page.open_bid(self.bid_id)
        self.database_connect.check_bid_status(self.bid_id, 'Верификация')
        bank_bid_common_page = BankBidCommonPage(self.browser)
        bank_bid_common_page.check_open()

        general_form_page = GeneralForm(self.browser)
        general_form_page.check_bank_accordion_data(BankBidBasic(bid, principal, client))
        general_form_page.check_bank_accordion_data(BankBidInfoAccordion(bid, principal))
        general_form_page.check_bank_accordion_data(
            BankBidInfoAboutClientAccordion(client, bank_account, beneficiary))
        general_form_page.select_required_locators_for_msp_ip()

        self.browser.refresh()
        bank_bid_common_page.check_open()
        bank_bid_common_page.select_menu_item(bank_bid_common_page.prof_text)

        profile_page = ProfilePage(self.browser)
        profile_page.check_open()
        profile_page.check_stop_factors(stop_factors)
        profile_page.check_selected_default(stop_factors)
        profile_page.select_required_factors(stop_factors)
        profile_page.click_on_elem(profile_page.calculate_btn)
        profile_page.check_calculated()
        profile_page.check_ratings_results(category='B')
        profile_page.use_rating()
        profile_page.generate_doc_by_name('Профсуждение')
        profile_page.generate_doc_by_name('Отчет о проверке и идентификации клиента')
        profile_page.generate_doc_by_name('Решение о выпуске БГ')
        profile_page.approve_doc('Профсуждение')
        profile_page.approve_doc('Отчет о проверке и идентификации клиента')
        profile_page.approve_doc('Решение о выпуске БГ')
        sleep(10)
        self.database_connect.check_bid_status(self.bid_id, 'Предложение принято')
        self.browser.refresh()
        Loaders(self.browser).wait_until_bank_loader_disappear(6)
        bank_bid_common_page.select_menu_item(bank_bid_common_page.proposal_text)
        bid_offer_page = BidOfferPage(self.browser)
        bid_offer_page.check_open()
        bid_offer_page.check_loaded()

        commission_form_expo = CommissionExpoForm(self.browser)
        commission_form_expo.check_tariff_expo(commission)
        bid_offer_page.check_success_company_data(check_egr=False)
        bid_offer_page.transfer_to_sign('file.jpg')
        self.database_connect.check_bid_status(self.bid_id, 'Подписание банком')

    def testOTPUsual(self):
        """ОТП обычная методика"""
        bid = Bid("0320100018021000009", "67 874 332.8", "20 362 299.84", "2 582 921.47", 1429,
                  BidType.execution, "25.03.2021",
                  "Выполнение работ по противопаводковым мероприятиям на объекте: "
                  "Сиваковский межхозяйственный магистральный канал, "
                  "с. Сиваковка, Хорольского района, Приморского края (правая дамба канала)",
                  region="Российская Федерация, Приморский край, Хорольский р-н, Сиваковка с")
        bank_account = BankAccountOtp()
        client = Client('2312150358', "1082312005456", "231201001",
                        "Общество с ограниченной ответственностью \"Кейсистемс-Кубань\"",
                        "ООО \"Кейсистемс-Кубань",
                        "350018, край Краснодарский, г Краснодар, ул Сормовская, дом 7, литера Г, пом 163/3",
                        "12300", "03701000001", "62.01")

        beneficiary = Beneficiary(birth_place="692001, Приморский край, Пожарский р-н, пгт Лучегорск, мкр 1-й, д 1",
                                  registration_address="692001, Приморский край, Пожарский р-н, пгт Лучегорск, мкр 1-й, д 1",
                                  fact_address="124365, г Москва, г Зеленоград, поселок Крюково, д 1, кв 1")
        principal = Customer(
            "ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ \"УПРАВЛЕНИЕ МЕЛИОРАЦИИ ЗЕМЕЛЬ И СЕЛЬСКОХОЗЯЙСТВЕННОГО ВОДОСНАБЖЕНИЯ ПО ПРИМОРСКОМУ И ХАБАРОВСКОМУ КРАЯМ\"",
            "690091, край Приморский, г Владивосток, ул Прапорщика Комарова, дом 21",
            "1022501285993", "2536042398", "253601001", "05701000001", "Приморский край", "16.01.1995")
        administration = Administration(
            birth_place="630040, Новосибирская обл, г Новосибирск, Заельцовский р-н, мкр Стрижи, д 1, кв 1",
            registration_address="630040, Новосибирская обл, г Новосибирск, Заельцовский р-н, мкр Стрижи, д 1, кв 1",
            fact_address="124365, г Москва, г Зеленоград, поселок Крюково, д 1, кв 1")

        fin = {
            "balance1600": 1000,
            "balance1700": 1000,
            "earnings2110": 3000
        }
        commission = Commission("3.24", "3,24", "4,15", bid.days_count, "0", "2 582 921,47", '3 311 437,78', "22,00000",
                                "728 516,31")

        self.database_connect.cleanup_data_by_inn(client.inn)
        with open("files/stop_factors_OTP_usual.json", encoding='utf-8') as json_data_file:
            stop_factors = json.load(json_data_file)

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        agent_page = login_page.login_as_agent()

        agent_page.create_bid_first_form(bid, client)

        create_bid_form = CreateBidForm(self.browser)
        create_bid_form.change_bank('ОТП-Банк')
        create_bid_form.click_on_elem(create_bid_form.go_to_bid_btn)

        agent_questionnaire = AgentQuestionnaire(self.browser)
        agent_questionnaire.check_open()
        self.bid_id = agent_questionnaire.get_bid_number()
        self.database_connect.check_bid_status(self.bid_id, 'Черновик')

        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_client)

        info_about_client_form = InfoAboutClientForm(self.browser)
        info_about_client_form.fill_OTP_required_fields(bank_account)

        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_client)
        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_beneficiary)

        beneficiary_form = BeneficiaryForm(self.browser)
        beneficiary_form.fill_required_fields_beneficiary(beneficiary)

        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_beneficiary)
        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_structure)

        info_about_structure = InfoAboutAdministration(self.browser)
        info_about_structure.fill_required_fields_administration(administration)
        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_structure)
        agent_questionnaire.click_on_elem(agent_questionnaire.finance)

        finance_page = Finance(self.browser)
        finance_page.check_open()
        finance_page.fill_required_fields_finance(fin)

        agent_questionnaire.click_on_elem(agent_questionnaire.docs)

        docs_page = DocsPage(self.browser)
        docs_page.check_open()
        docs_page.check_anketa_generated()
        docs_page.load_docs_for_OTP_usual('file.jpg')
        # docs_page.check_open_sign_link_for_usual()
        agent_api = AgentApi()
        agent_api.upload_package_otp_usual(self.bid_id, 'file.jpg.sig')
        agent_api.transfer_to_bank(self.bid_id)
        self.database_connect.check_bid_status(self.bid_id, 'Передано в Банк')

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        login_page.login_as_bank()

        bank_page = BankPage(self.browser)
        bank_page.check_open()
        bank_page.set_required_users(self.bid_id)
        bank_page.open_bid(self.bid_id)
        self.database_connect.check_bid_status(self.bid_id, 'Рассмотрение')
        bank_bid_common_page = BankBidCommonPage(self.browser)
        bank_bid_common_page.check_open()

        general_form_page = GeneralForm(self.browser)
        general_form_page.check_bank_accordion_data(BankBidBasic(bid, principal, client))
        general_form_page.check_bank_accordion_data(BankBidInfoAccordion(bid, principal))
        general_form_page.check_bank_accordion_data(
            BankBidInfoAboutClientAccordion(client, bank_account, beneficiary))
        general_form_page.check_bank_accordion_data(BankBidInfoAboutStructure(administration))
        general_form_page.select_required_locators_for_usual()

        bank_bid_common_page.select_menu_item(bank_bid_common_page.prof_text)

        profile_page = ProfilePage(self.browser)
        profile_page.check_open()

        profile_page.check_stop_factors(stop_factors)
        profile_page.check_selected_default(stop_factors)
        profile_page.select_required_factors(stop_factors)
        profile_page.click_on_elem(profile_page.calculate_btn)
        profile_page.check_calculated()
        profile_page.check_ratings_results('2.58', 'BB', 'Среднее', '9')
        profile_page.use_rating()
        profile_page.generate_doc_by_name('Профсуждение')

        self.database_connect.check_bid_status(self.bid_id, 'Рассмотрение')
        self.database_connect.change_bid_status(self.bid_id, 'Формирование предложения')
        self.database_connect.check_bid_status(self.bid_id, 'Формирование предложения')

        self.browser.refresh()
        bank_bid_common_page.check_open()
        bank_bid_common_page.select_menu_item(bank_bid_common_page.proposal_text)
        bid_offer_page = BidOfferPage(self.browser)
        bid_offer_page.check_open()
        bid_offer_page.select_signer('Тест Тестов Тестович (2040-01-01)')
        bid_offer_page.check_tariff(commission)
        bid_offer_page.send_to_client()
        self.database_connect.check_bid_status(self.bid_id, 'Предложение направлено')

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        login_page.login_as_agent()

        agent_page = AgentPage(self.browser)
        agent_page.check_open()
        agent_page.open_bid_use_filter(self.bid_id)

        commission_form = CommissionForm(self.browser)
        commission_form.check_open()
        commission_form.accept_commission()
        sign_page = DocsPage(self.browser)
        sign_page.check_open_sign_link_for_usual()

        agent_api.accept_proposal_otp(self.bid_id, 'act.sig')
        self.database_connect.check_bid_status(self.bid_id, 'Предложение принято')

    def testOTPExpress(self):
        """ОТП экспресс методика менее 10 млн"""
        bid = Bid("0338200005321000012", "344 433.5", "10 000.00", "5 000", 50,
                  BidType.execution, "23.04.2021", "Поставка лекарственных препаратов не ЖНВЛП",
                  "Российская Федерация, Камчатский край, Петропавловск-Камчатский г")
        bank_account = BankAccountOtp()
        client = Client('2312150358', "1082312005456", "231201001",
                        "Общество с ограниченной ответственностью \"Кейсистемс-Кубань\"",
                        "ООО \"Кейсистемс-Кубань",
                        "350018, край Краснодарский, г Краснодар, ул Сормовская, дом 7, литера Г, пом 163/3",
                        "12300", "03701000001", "62.01")
        principal = Customer(
            "Государственное бюджетное учреждение здравоохранения \"Камчатский краевой наркологический диспансер",
            "683024, край Камчатский, г Петропавловск-Камчатский, пр-кт 50 лет Октября, дом 2",
            "1024101036838",
            "4101036378", "410101001", "30701000001", "Камчатский край", "25.04.2000")
        beneficiary = Beneficiary(birth_place="692001, Приморский край, Пожарский р-н, пгт Лучегорск, мкр 1-й, д 1",
                                  registration_address="692001, Приморский край, Пожарский р-н, пгт Лучегорск, мкр 1-й, д 1",
                                  fact_address="124365, г Москва, г Зеленоград, поселок Крюково, д 1, кв 1")

        administration = Administration(
            birth_place="630040, Новосибирская обл, г Новосибирск, Заельцовский р-н, мкр Стрижи, д 1, кв 1",
            registration_address="630040, Новосибирская обл, г Новосибирск, Заельцовский р-н, мкр Стрижи, д 1, кв 1",
            fact_address="124365, г Москва, г Зеленоград, поселок Крюково, д 1, кв 1")

        fin = {
            "balance1600": 1000,
            "balance1700": 1000,
            "earnings2110": 3000
        }
        commission = Commission("5000", "365,00", "467,95", bid.days_count, "0", " 5000,00", '6410,26', "22,00000",
                                "1410,26")

        self.database_connect.cleanup_data_by_inn(client.inn)
        with open("files/stop_factors_OTP_express.json", encoding='utf-8') as json_data_file:
            stop_factors = json.load(json_data_file)

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        login_page.login_as_agent()

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
        create_bid_form.check_form_data(bid)

        create_bid_form.change_bank('ОТП-Банк')
        bid.commission = '6 410,26'
        create_bid_form.go_to_bid()

        agent_questionnaire = AgentQuestionnaire(self.browser)
        agent_questionnaire.check_open()
        self.bid_id = agent_questionnaire.get_bid_number()
        self.database_connect.check_bid_status(self.bid_id, 'Черновик')

        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_client)

        info_about_client_form = InfoAboutClientForm(self.browser)
        info_about_client_form.fill_OTP_required_fields(bank_account)

        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_client)
        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_beneficiary)

        beneficiary_form = BeneficiaryForm(self.browser)
        beneficiary_form.fill_required_fields_beneficiary(beneficiary)

        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_beneficiary)
        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_structure)

        info_about_structure = InfoAboutAdministration(self.browser)
        info_about_structure.fill_required_fields_administration(administration)
        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_structure)
        agent_questionnaire.click_on_elem(agent_questionnaire.finance)

        finance_page = Finance(self.browser)
        finance_page.check_open_otp_express()
        finance_page.fill_manual()
        finance_page.fill_required_fields_finance(fin)

        agent_questionnaire.click_on_elem(agent_questionnaire.docs)

        docs_page = DocsPage(self.browser)
        docs_page.check_open_express()
        docs_page.load_docs_for_OTP_express('file.jpg')

        # commission_form = CommissionForm(self.browser)
        # commission_form.check_open()
        # commission_form.accept_commission()
        #
        # offer_form = OfferForm(self.browser)
        # offer_form.check_open()
        # offer_form.confirm_otp_express()
        # offer_form.check_open_sign_link()

        agent_api = AgentApi()
        agent_api.upload_package_otp_express(self.bid_id, 'file.jpg.sig')
        agent_api.transfer_to_bank(self.bid_id)
        agent_api.accept_proposal_otp(self.bid_id, 'act.sig')
        self.database_connect.check_bid_status(self.bid_id, 'Рассмотрение')

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        login_page.login_as_bank()

        bank_page = BankPage(self.browser)
        bank_page.check_open()
        bank_page.set_required_users(self.bid_id)
        bank_page.open_bid(self.bid_id)
        bank_bid_common_page = BankBidCommonPage(self.browser)
        bank_bid_common_page.check_open()

        general_form_page = GeneralForm(self.browser)
        general_form_page.check_bank_accordion_data(BankBidBasic(bid, principal, client))
        general_form_page.check_bank_accordion_data(BankBidInfoAccordion(bid, principal))
        general_form_page.check_bank_accordion_data(
            BankBidInfoAboutClientAccordion(client, bank_account, beneficiary))
        general_form_page.check_bank_accordion_data(BankBidInfoAboutStructure(administration))
        general_form_page.select_required_locators_for_usual()

        bank_bid_common_page.select_menu_item(bank_bid_common_page.prof_text)

        profile_page = ProfilePage(self.browser)
        profile_page.check_open()

        profile_page.check_stop_factors(stop_factors)
        profile_page.check_selected_default(stop_factors)
        profile_page.select_required_factors(stop_factors)
        profile_page.click_on_elem(profile_page.calculate_btn)
        profile_page.check_calculated()
        profile_page.check_ratings_results('4', 'A', 'Хорошее', '9')
        profile_page.use_rating()
        profile_page.generate_doc_by_name('Профсуждение')

        self.database_connect.change_bid_status(self.bid_id, 'Предложение принято')
        self.browser.refresh()

        bank_bid_common_page.check_open()
        bank_bid_common_page.select_menu_item(bank_bid_common_page.proposal_text)
        bid_offer_page = BidOfferPage(self.browser)
        bid_offer_page.check_open()
        bid_offer_page.check_tariff(commission)

    def testCreditEurope(self):
        """Заявка банка КредитЕвропа"""
        bid = Bid("0338200005321000012", "344 433.5", "10 000.00", "5 000", 50,
                  BidType.execution, "23.04.2021", "Поставка лекарственных препаратов не ЖНВЛП",
                  "Российская Федерация, Камчатский край, Петропавловск-Камчатский г")
        bank_account = BankAccount()
        client = Client('1901019320', "1021900532752", "190101001",
                        "Общество с ограниченной ответственностью \"Автодорпроект \"Трасса",
                        "ООО \"Автодорпроект \"Трасса", "655017, респ Хакасия, г Абакан, ул Вяткина, дом 3",
                        "12300", "95701000001", "71.11")
        principal = Customer(
            "Государственное бюджетное учреждение здравоохранения \"Камчатский краевой наркологический диспансер",
            "683024, край Камчатский, г Петропавловск-Камчатский, пр-кт 50 лет Октября, дом 2",
            "1024101036838",
            "4101036378", "410101001", "30701000001", "Камчатский край", "25.04.2000")
        beneficiary = Beneficiary(birth_place="692001, Приморский край, Пожарский р-н, пгт Лучегорск, мкр 1-й, д 1",
                                  registration_address="692001, Приморский край, Пожарский р-н, пгт Лучегорск, мкр 1-й, д 1",
                                  fact_address="124365, г Москва, г Зеленоград, поселок Крюково, д 1, кв 1",
                                  inn="190102049125", fio="Ромулов Владислав Михайлович")
        administration = Administration(
            birth_place="630040, Новосибирская обл, г Новосибирск, Заельцовский р-н, мкр Стрижи, д 1, кв 1",
            registration_address="630040, Новосибирская обл, г Новосибирск, Заельцовский р-н, мкр Стрижи, д 1, кв 1",
            fact_address="124365, г Москва, г Зеленоград, поселок Крюково, д 1, кв 1", role="Директор",
            fio="Шлойда Василий Геннадьевич", inn="")
        commission = Commission("5000", "365,00", "467,95", bid.days_count, "0", " 5000,00", "6410,26", "22,00000",
                                "1410,26")
        self.database_connect.cleanup_data_by_inn(client.inn)
        with open("files/stop_factors_Credit_Europe.json", encoding='utf-8') as json_data_file:
            stop_factors = json.load(json_data_file)

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        agent_page = login_page.login_as_agent()

        agent_page.create_bid_first_form(bid, client)

        create_bid_form = CreateBidForm(self.browser)
        create_bid_form.change_bank('Кредит Европа Банк')

        create_bid_form.click_on_elem(create_bid_form.go_to_bid_btn)

        agent_questionnaire = AgentQuestionnaire(self.browser)
        agent_questionnaire.check_open()
        self.bid_id = agent_questionnaire.get_bid_number()
        self.database_connect.check_bid_status(self.bid_id, 'Черновик')

        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_client)

        info_about_client_form = InfoAboutClientForm(self.browser)
        info_about_client_form.fill_required_fields_bank_account(bank_account)

        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_client)
        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_beneficiary)

        beneficiary_form = BeneficiaryForm(self.browser)
        beneficiary_form.add_beneficiary()
        beneficiary_form.fill_beneficiary_fio(beneficiary)
        beneficiary_form.fill_required_fields_Credit_Europe(beneficiary)

        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_beneficiary)
        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_structure)

        info_about_structure = InfoAboutAdministration(self.browser)
        info_about_structure.fill_required_fields_administration(administration)
        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_structure)
        agent_questionnaire.click_on_elem(agent_questionnaire.docs)

        docs_page = DocsPage(self.browser)
        docs_page.check_open()
        docs_page.load_passport('file.jpg')
        docs_page.check_open_sign_link_for_usual()
        agent_api = AgentApi()
        agent_api.upload_package_passport_anketa(self.bid_id, 'file.jpg.sig')
        agent_api.transfer_to_bank(self.bid_id)
        self.database_connect.check_bid_status(self.bid_id, 'Передано в Банк')

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        login_page.login_as_bank()

        bank_page = BankPage(self.browser)
        bank_page.check_open()
        bank_page.set_required_users(self.bid_id)
        bank_page.open_bid(self.bid_id)
        self.database_connect.check_bid_status(self.bid_id, 'Рассмотрение')
        bank_bid_common_page = BankBidCommonPage(self.browser)
        bank_bid_common_page.check_open()

        general_form_page = GeneralForm(self.browser)
        general_form_page.check_bank_accordion_data(BankBidBasic(bid, principal, client))
        general_form_page.check_bank_accordion_data(BankBidInfoAccordion(bid, principal))
        general_form_page.check_bank_accordion_data(
            BankBidInfoAboutClientAccordion(client, bank_account, beneficiary))
        general_form_page.check_bank_accordion_data(BankBidInfoAboutStructure(administration))
        general_form_page.select_required_locators_without_finance()

        self.browser.refresh()
        bank_bid_common_page.check_open()
        bank_bid_common_page.select_menu_item(bank_bid_common_page.prof_text)

        profile_page = ProfilePage(self.browser)
        profile_page.check_open()

        profile_page.check_stop_factors(stop_factors)
        profile_page.check_selected_default(stop_factors)
        profile_page.select_required_factors(stop_factors)
        profile_page.click_on_elem(profile_page.calculate_btn)
        profile_page.check_calculated()
        profile_page.check_ratings_results('4.5', 'BBB', 'Хорошее')
        profile_page.use_rating()
        profile_page.generate_doc_by_name('Заключение СП')
        profile_page.generate_doc_by_name('Вопросник')
        profile_page.generate_doc_by_name('Профсуждение')

        self.database_connect.check_bid_status(self.bid_id, 'Рассмотрение')
        self.database_connect.change_bid_status(self.bid_id, 'Формирование предложения')
        self.database_connect.check_bid_status(self.bid_id, 'Формирование предложения')

        self.browser.refresh()
        bank_page.check_open()
        bank_bid_common_page.check_open()
        bank_bid_common_page.select_menu_item(bank_bid_common_page.proposal_text)
        bid_offer_page = BidOfferPage(self.browser)
        bid_offer_page.check_open()
        bid_offer_page.select_signer('Вердиев Асад Йылмаз оглы (2025-01-15)')
        bid_offer_page.check_tariff(commission)
        bid_offer_page.send_to_client()
        self.database_connect.check_bid_status(self.bid_id, 'Предложение направлено')

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        login_page.login_as_agent()

        agent_page = AgentPage(self.browser)
        agent_page.check_open()
        agent_page.open_bid_use_filter(self.bid_id)

        commission_form = CommissionForm(self.browser)
        commission_form.check_open()
        commission_form.accept_commission()
        sign_page = DocsPage(self.browser)
        sign_page.check_open_sign_link_for_usual()

        agent_api.accept_proposal(self.bid_id, 'act.sig')
        self.database_connect.check_bid_status(self.bid_id, 'Предложение принято')

    def testGroupBid(self):
        """Подача групповой заявки, заполнение анкеты """
        bid = Bid("0873500000821002536", "48 199 726.80",
                  ["524 521.42", "774 145.41", "1 647 833.40", "280 197.15", "1 196 633.50",
                   "396 641.80"], ['13 968.08', '20 615.6', '41 985.89', '7 461.69', '30 489.57', '10 562.63'], 300,
                  BidType.execution, "31.03.2021",
                  "Оказание услуг по уборке и содержанию прилегающей территории образовательных организаций,"
                  " подведомственных Департаменту образования и науки города Москвы, в 2021-2023 годах",
                  "город Москва, бульвар Сиреневый, дом 68")
        bank_account = BankAccount()
        beneficiary = Beneficiary()
        client = Client('2312150358', "1082312005456", "231201001",
                        "Общество с ограниченной ответственностью \"Кейсистемс-Кубань\"",
                        "ООО \"Кейсистемс-Кубань",
                        "350018, край Краснодарский, г Краснодар, ул Сормовская, дом 7, литера Г, пом 163/3",
                        "12300", "03701000001", "62.01")
        administration = Administration()
        fin = {
            "balance1600": 1000,
            "balance1700": 1000,
            "earnings2110": 3000
        }
        self.database_connect.cleanup_data_by_inn(client.inn)

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        login_page.login_as_agent()

        agent_page = AgentPage(self.browser)
        agent_page.check_open()
        agent_page.click_on_create_bid_btn()

        create_bid_page = CreateBidPage(self.browser)
        create_bid_page.check_open()
        create_bid_page.fill_required_fields_client(bid, client)
        create_bid_page.fill_required_field_group(bid)
        create_bid_page.click_on_create_bid_btn()

        create_bid_form = CreateBidForm(self.browser)
        create_bid_form.check_open()
        self.assertEqual(bid.commission, create_bid_form.get_commission_for_group())
        for bank in create_bid_form.get_banks_for_group():
            self.assertEqual("Экспобанк", bank)
        self.bid_ids = create_bid_form.get_bid_id_for_group()
        create_bid_form.click_on_elem(create_bid_form.go_to_bid_btn)

        agent_questionnaire = AgentQuestionnaire(self.browser)
        agent_questionnaire.check_open()

        agent_questionnaire = AgentQuestionnaire(self.browser)
        agent_questionnaire.check_open()
        self.bid_id = agent_questionnaire.get_bid_number()
        self.database_connect.check_bid_status(self.bid_id, 'Черновик')
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
        agent_questionnaire.click_on_elem(agent_questionnaire.finance)

        finance_page = Finance(self.browser)
        finance_page.check_open()
        finance_page.fill_required_fields_finance(fin)

        agent_questionnaire.click_on_elem(agent_questionnaire.docs)

        docs_page = DocsPage(self.browser)
        docs_page.check_open_express()
        docs_page.load_docs_for_group('file.jpg')
        docs_page.submit(100)

        # загрузить доки и принять предложение для e+ для 1,2,4,6 заявок
        loaders = Loaders(self.browser)
        loaders.wait_until_disappear(loaders.loaderAgent, 'xpath', 70)
        self.browser.refresh()

        commission_form = CommissionForm(self.browser)
        commission_form.check_open()
        commission_form.accept_commission()

        offer_form = OfferForm(self.browser)
        offer_form.check_open()

    def testMspUsual(self):
        """Заявка методика МСП путь обычный"""
        with open("files/stop_factors_msp_ip.json", encoding='utf-8') as json_data_file:
            stop_factors = json.load(json_data_file)
        bid = Bid("0320100018021000009", "67 874 332.8", "9 000 000.00", "1 010 958.9", 1000,
                  BidType.execution, "25.03.2021",
                  "Выполнение работ по противопаводковым мероприятиям на объекте: "
                  "Сиваковский межхозяйственный магистральный канал, "
                  "с. Сиваковка, Хорольского района, Приморского края (правая дамба канала)",
                  region="Российская Федерация, Приморский край, Хорольский р-н, Сиваковка с")
        client = Client('252691919497', "306250631900028", "", "ИП Бегматов Мирали Палвонович",
                        "ИП Бегматов Мирали Палвонович", "край Приморский, пгт Лучегорск, р-н Пожарский",
                        "50102", "05634151051", "43.3")
        principal = Customer(
            "ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ \"УПРАВЛЕНИЕ МЕЛИОРАЦИИ ЗЕМЕЛЬ И"
            " СЕЛЬСКОХОЗЯЙСТВЕННОГО ВОДОСНАБЖЕНИЯ ПО ПРИМОРСКОМУ И ХАБАРОВСКОМУ КРАЯМ\"",
            "690091, край Приморский, г Владивосток, ул Прапорщика Комарова, дом 21",
            "1022501285993", "2536042398", "253601001", "05701000001", "Приморский край", "16.01.1995")
        bank_account = BankAccount()
        beneficiary = Beneficiary(birth_place="692001, Приморский край, Пожарский р-н, пгт Лучегорск",
                                  registration_address="край Приморский, пгт Лучегорск, р-н Пожарский")
        commission = CommissionExpo("3.1", "4,10", "4,10", bid.days_count, "0", "0", "1 010 958,90", "0", "1 010 958,90"
                                    )
        self.database_connect.cleanup_data_by_inn(client.inn)

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        agent_page = login_page.login_as_agent()

        self.bid_id = agent_page.create_bid_ip_and_get_bid_id(bid, client, bank_account, beneficiary)

        docs_page = DocsPage(self.browser)
        docs_page.load_passport('file.jpg', docs_page.msp_passport_load_btn)
        docs_page.check_open_sign_link_for_usual()

        agent_api = AgentApi()
        agent_api.upload_package_passport_anketa(self.bid_id, 'file.jpg.sig', ip=True)
        agent_api.transfer_to_bank(self.bid_id)
        self.database_connect.check_bid_status(self.bid_id, 'Передано в Банк')

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        login_page.login_as_bank()

        bank_page = BankPage(self.browser)
        bank_page.check_open()
        bank_page.set_required_users(self.bid_id)
        bank_page.open_bid(self.bid_id)
        self.database_connect.check_bid_status(self.bid_id, 'Рассмотрение')
        bank_bid_common_page = BankBidCommonPage(self.browser)
        bank_bid_common_page.check_open()

        general_form_page = GeneralForm(self.browser)
        general_form_page.check_bank_accordion_data(BankBidBasic(bid, principal, client))
        general_form_page.check_bank_accordion_data(BankBidInfoAccordion(bid, principal))
        general_form_page.check_bank_accordion_data(
            BankBidInfoAboutClientAccordion(client, bank_account, beneficiary))
        general_form_page.select_required_locators_for_msp_ip()

        bank_bid_common_page.select_menu_item(bank_bid_common_page.prof_text)

        profile_page = ProfilePage(self.browser)
        profile_page.check_open()

        profile_page.check_stop_factors(stop_factors)
        profile_page.check_selected_default(stop_factors)
        profile_page.select_required_factors(stop_factors)
        profile_page.click_on_elem(profile_page.calculate_btn)
        profile_page.check_calculated()
        profile_page.check_ratings_results(category="B")
        profile_page.use_rating()
        profile_page.generate_doc_by_name('Профсуждение')
        profile_page.generate_doc_by_name('Отчет о проверке и идентификации клиента')
        profile_page.generate_doc_by_name('Решение о выпуске БГ')

        self.database_connect.check_bid_status(self.bid_id, 'Рассмотрение')
        self.database_connect.change_bid_status(self.bid_id, 'Формирование предложения')
        self.database_connect.check_bid_status(self.bid_id, 'Формирование предложения')

        self.browser.refresh()
        bank_bid_common_page.check_open()
        bank_bid_common_page.select_menu_item(bank_bid_common_page.proposal_text)
        bid_offer_page = BidOfferPage(self.browser)
        bid_offer_page.check_open()
        bid_offer_page.select_signer()

        commission_expo_form = CommissionExpoForm(self.browser)
        commission_expo_form.check_tariff_expo(commission)
        bid_offer_page.send_to_client()
        self.database_connect.check_bid_status(self.bid_id, 'Предложение направлено')

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        login_page.login_as_agent()

        agent_page = AgentPage(self.browser)
        agent_page.check_open()
        agent_page.open_bid_use_filter(self.bid_id)

        commission_form = CommissionForm(self.browser)
        commission_form.check_open()
        commission_form.accept_commission()

        sign_page = DocsPage(self.browser)
        sign_page.check_open_sign_link_for_usual()

        agent_api.accept_proposal(self.bid_id, 'act.sig')
        self.database_connect.check_bid_status(self.bid_id, 'Предложение принято')

    def test_questionnaire_two_beneficiaries(self):
        """Заполнение анкеты с двумя бенефициарами"""
        with open("files/stop_factors_msp_ip.json", encoding='utf-8') as json_data_file:
            stop_factors = json.load(json_data_file)
        bid = Bid("0338200005321000012", "344 433.50", "10 000.00", "5 000", 50,
                  BidType.execution, "23.04.2021", "Поставка лекарственных препаратов не ЖНВЛП",
                  "Российская Федерация, Камчатский край, Петропавловск-Камчатский г")
        client = Client('4710011043', "", "", "",
                        "", "",
                        "", "", "")
        bank_account = BankAccount()
        beneficiary = Beneficiary(fio="Степанов Владимир Николаевич", inn="471002009648", part="70")
        beneficiary2 = Beneficiary(fio="Козловский Николай Владимирович", inn="782020590778", part="30")
        administration = Administration(inn="471002009648", fio="Степанов Владимир Николаевич", role="Директор")
        stockholder = Stockholder("Козловский Николай Владимирович", "782020590778", "30", 1)
        stockholder2 = Stockholder("Степанов Владимир Николаевич", "471002009648", "70", 2)
        self.database_connect.cleanup_data_by_inn(client.inn)

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        agent_page = login_page.login_as_agent()

        agent_page.create_bid_first_form(bid, client)

        create_bid_form = CreateBidForm(self.browser)
        create_bid_form.click_on_elem(create_bid_form.go_to_bid_btn)

        agent_questionnaire = AgentQuestionnaire(self.browser)
        agent_questionnaire.check_open()
        self.bid_id = agent_questionnaire.get_bid_number()
        self.database_connect.check_bid_status(self.bid_id, 'Черновик')

        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_beneficiary)
        beneficiary_form = BeneficiaryForm(self.browser)
        beneficiary_form.add_beneficiary()
        beneficiary_form.add_beneficiary()
        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_beneficiary)

        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_client)
        info_about_client_form = InfoAboutClientForm(self.browser)
        info_about_client_form.fill_required_fields_bank_account(bank_account)
        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_client)

        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_structure)
        stockholder_form = StockholderForm(self.browser)
        stockholder_form.add_percentage_to_exist_stockholder(stockholder)
        stockholder_form.add_percentage_to_exist_stockholder(stockholder2)
        info_about_structure = InfoAboutAdministration(self.browser)
        info_about_structure.fill_required_fields_administration(administration)
        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_structure)

        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_beneficiary)
        beneficiary_form = BeneficiaryForm(self.browser)
        beneficiary_form.fill_beneficiary_fio(beneficiary)
        beneficiary_form.fill_beneficiary_fio(beneficiary2)
        beneficiary_form.fill_phone_number(beneficiary)
        beneficiary_form.fill_required_fields_beneficiary_by_number(beneficiary2, 2)

        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_beneficiary)
        agent_questionnaire.click_on_elem(agent_questionnaire.docs)

        docs_page = DocsPage(self.browser)
        docs_page.load_passport('file.jpg')
        sleep(1)
        docs_page.submit()

        commission_form = CommissionForm(self.browser)
        commission_form.check_open()
        commission_form.accept_commission()

    def testMspCommissionAgentDiscountRateB(self):
        """Автонадбавка МСП заявки по инн с рейтингом B"""
        with open("files/ip_262311277845.json", encoding='utf-8') as json_data_file:
            stop_factors = json.load(json_data_file)
        bid = Bid("0338200005321000012", "344 433.50", "800 000", "37 172.6", 400,
                  BidType.execution, "23.04.2021", "Поставка лекарственных препаратов не ЖНВЛП",
                  "Российская Федерация, Камчатский край, Петропавловск-Камчатский г")
        client = Client('262311277845', "312265103900014", "", "ИП Беняминян Гарик Саргисович",
                        "ИП Беняминян Гарик Саргисович", "",
                        "", "", "")
        bank_account = BankAccount()
        beneficiary = Beneficiary(birth_place="692001, Приморский край, Пожарский р-н, пгт Лучегорск",
                                  registration_address="край Приморский, пгт Лучегорск, р-н Пожарский")
        commission = CommissionExpo("3.24", "4,24", "3,90", bid.days_count, "0", "3000", "37 172.60", "0", "34 172.60")
        discount = "3000"
        self.database_connect.cleanup_data_by_inn(client.inn)

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        agent_page = login_page.login_as_agent()

        self.bid_id = agent_page.create_bid_ip_and_get_bid_id(bid, client, bank_account, beneficiary)

        docs_page = DocsPage(self.browser)
        docs_page.check_open_express()
        docs_page.load_passport('file.jpg', docs_page.msp_passport_load_btn)

        agent_api = AgentApi()
        agent_api.upload_package_passport_anketa(self.bid_id, 'file.jpg.sig', ip=True)
        agent_api.transfer_to_bank(self.bid_id)

        self.browser.refresh()
        commission_form = CommissionForm(self.browser)
        commission_form.check_open()
        commission_form.fill_agent_discount(discount)

        commission_form.accept_commission()

        agent_api.accept_proposal(self.bid_id, 'act.sig')

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        login_page.login_as_bank()

        bank_page = BankPage(self.browser)
        bank_page.check_open()
        bank_page.set_required_users(self.bid_id)
        bank_page.open_bid(self.bid_id)
        self.database_connect.check_bid_status(self.bid_id, 'Верификация')
        bank_bid_common_page = BankBidCommonPage(self.browser)
        bank_bid_common_page.check_open()

        general_form_page = GeneralForm(self.browser)
        general_form_page.select_required_locators_for_msp_ip()

        self.browser.refresh()
        bank_bid_common_page.check_open()
        bank_bid_common_page.select_menu_item(bank_bid_common_page.prof_text)

        profile_page = ProfilePage(self.browser)
        profile_page.check_open()
        profile_page.check_stop_factors(stop_factors)
        profile_page.check_selected_default(stop_factors)
        profile_page.select_required_factors(stop_factors)
        profile_page.calculate()
        profile_page.check_ratings_results(category='B')
        profile_page.use_rating()
        profile_page.generate_doc_by_name('Профсуждение')
        profile_page.generate_doc_by_name('Отчет о проверке и идентификации клиента')
        profile_page.generate_doc_by_name('Решение о выпуске БГ')
        profile_page.approve_doc('Профсуждение')
        profile_page.approve_doc('Отчет о проверке и идентификации клиента')
        profile_page.approve_doc('Решение о выпуске БГ')
        sleep(10)
        self.database_connect.check_bid_status(self.bid_id, 'Предложение принято')
        self.browser.refresh()
        Loaders(self.browser).wait_until_bank_loader_disappear(6)
        bank_bid_common_page.select_menu_item(bank_bid_common_page.proposal_text)
        bid_offer_page = BidOfferPage(self.browser)
        bid_offer_page.check_open()
        bid_offer_page.check_loaded()

        commission_form_expo = CommissionExpoForm(self.browser)
        commission_form_expo.check_tariff_expo(commission)

    def testMspRateBMinusUsualBankAgentDiscount(self):
        """Автонадбавка МСП заяявки с рейтингом B-, скидка банка и агента"""
        with open("files/stop_factors_msp.json", encoding='utf-8') as json_data_file:
            stop_factors = json.load(json_data_file)
        client = Client("9201007718", "1149204023100", "920101001",
                        "ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ \"АЗЗУРРО ТРЕЙД\"", "ООО \"Аззурро Трейд\"",
                        "299040, г Севастополь, ул Индустриальная, дом 3Г",
                        "12300", "67312000000", "33.15")
        bid = Bid("0320100018021000009", "67 874 332.8", "9 000 000.00", "764 383.56", 1000,
                  BidType.execution, "25.03.2021",
                  "Выполнение работ по противопаводковым мероприятиям на объекте: "
                  "Сиваковский межхозяйственный магистральный канал, "
                  "с. Сиваковка, Хорольского района, Приморского края (правая дамба канала)",
                  region="Российская Федерация, Приморский край, Хорольский р-н, Сиваковка с")
        principal = Customer(
            "ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ \"УПРАВЛЕНИЕ МЕЛИОРАЦИИ ЗЕМЕЛЬ И"
            " СЕЛЬСКОХОЗЯЙСТВЕННОГО ВОДОСНАБЖЕНИЯ ПО ПРИМОРСКОМУ И ХАБАРОВСКОМУ КРАЯМ\"",
            "690091, край Приморский, г Владивосток, ул Прапорщика Комарова, дом 21",
            "1022501285993", "2536042398", "253601001", "05701000001", "Приморский край", "16.01.1995")
        bank_account = BankAccount()
        beneficiary = Beneficiary(birth_place="692001, Приморский край, Пожарский р-н, пгт Лучегорск",
                                  registration_address="край Приморский, пгт Лучегорск, р-н Пожарский")
        commission = CommissionExpo("3.1", "6,10", "6,10", bid.days_count, "0", "0", "1 504 109,59", "0", "1 504 109,59"
                                    )
        commission_after_bank_discount = CommissionExpo("3.1", "4,27", "4,27", bid.days_count, "30", "0",
                                                        "1 052 876,71",
                                                        "0", "1 052 876,71"
                                                        )
        commission_after_agent_discount = CommissionExpo("3.1", "4,27", "3,05", bid.days_count, "30", "20",
                                                         "1 052 876,71",
                                                         "0", "752 054,79"
                                                         )
        administration = Administration()
        self.database_connect.cleanup_data_by_inn(client.inn)

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        agent_page = login_page.login_as_agent()

        agent_page.create_bid_first_form(bid, client)

        create_bid_form = CreateBidForm(self.browser)
        create_bid_form.click_on_elem(create_bid_form.go_to_bid_btn)

        agent_questionnaire = AgentQuestionnaire(self.browser)
        agent_questionnaire.check_open()
        self.bid_id = agent_questionnaire.get_bid_number()
        self.database_connect.check_bid_status(self.bid_id, 'Черновик')

        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_client)
        info_about_client_form = InfoAboutClientForm(self.browser)
        info_about_client_form.fill_required_fields_bank_account(bank_account)
        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_client)

        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_beneficiary)
        beneficiary_form = BeneficiaryForm(self.browser)
        beneficiary_form.fill_phone_number(beneficiary)
        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_beneficiary)

        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_structure)
        info_about_structure = InfoAboutAdministration(self.browser)
        info_about_structure.fill_required_fields_administration(administration)

        agent_questionnaire.click_on_elem(agent_questionnaire.docs)

        docs_page = DocsPage(self.browser)
        docs_page.check_open()
        docs_page.load_passport('file.jpg')
        docs_page.check_open_sign_link_for_usual()
        agent_api = AgentApi()
        agent_api.upload_package_passport_anketa(self.bid_id, 'file.jpg.sig')
        agent_api.transfer_to_bank(self.bid_id)
        self.database_connect.check_bid_status(self.bid_id, 'Передано в Банк')

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        login_page.login_as_bank()

        bank_page = BankPage(self.browser)
        bank_page.check_open()
        bank_page.set_required_users(self.bid_id)
        bank_page.open_bid(self.bid_id)
        self.database_connect.check_bid_status(self.bid_id, 'Рассмотрение')
        bank_bid_common_page = BankBidCommonPage(self.browser)
        bank_bid_common_page.check_open()

        general_form_page = GeneralForm(self.browser)
        general_form_page.check_bank_accordion_data(BankBidBasic(bid, principal, client))
        general_form_page.check_bank_accordion_data(BankBidInfoAccordion(bid, principal))
        general_form_page.check_bank_accordion_data(
            BankBidInfoAboutClientAccordion(client, bank_account, beneficiary))
        general_form_page.update_fin('1310', '2020', '4', "-1000")
        general_form_page.select_required_locators_for_usual()

        bank_bid_common_page.select_menu_item(bank_bid_common_page.prof_text)

        profile_page = ProfilePage(self.browser)
        profile_page.check_open()

        profile_page.check_stop_factors(stop_factors)
        profile_page.check_selected_default(stop_factors)
        profile_page.select_required_factors(stop_factors)
        profile_page.click_on_elem(profile_page.calculate_btn)
        profile_page.check_calculated()
        profile_page.check_ratings_results(category="B-")
        profile_page.use_rating()
        profile_page.generate_doc_by_name('Профсуждение')
        profile_page.generate_doc_by_name('Отчет о проверке и идентификации клиента')
        profile_page.generate_doc_by_name('Решение о выпуске БГ')

        self.database_connect.check_bid_status(self.bid_id, 'Рассмотрение')
        self.database_connect.change_bid_status(self.bid_id, 'Формирование предложения')
        self.database_connect.check_bid_status(self.bid_id, 'Формирование предложения')

        self.browser.refresh()
        bank_bid_common_page.select_menu_item(bank_bid_common_page.proposal_text)
        bid_offer_page = BidOfferPage(self.browser)
        bid_offer_page.check_open()
        bid_offer_page.select_signer()

        commission_expo_form = CommissionExpoForm(self.browser)
        commission_expo_form.check_tariff_expo(commission)
        commission_expo_form.change_bank_discount("30")
        commission_expo_form.check_tariff_expo(commission_after_bank_discount)
        commission_expo_form.change_agent_discount("20")
        commission_expo_form.check_tariff_expo(commission_after_agent_discount)

        bid_offer_page.send_to_client()
        self.database_connect.check_bid_status(self.bid_id, 'Предложение направлено')

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        login_page.login_as_agent()

        agent_page = AgentPage(self.browser)
        agent_page.check_open()
        agent_page.open_bid_use_filter(self.bid_id)

        commission_form = CommissionForm(self.browser)
        commission_form.check_open()
        commission_form.check_main_fields(commission_after_agent_discount.commission, '300821,92', '0')
        commission_form.accept_commission()

        sign_page = DocsPage(self.browser)
        sign_page.check_open_sign_link_for_usual()

    @unittest.skip('не дописан, требуется помощь разработки для прямого клиента')
    def test_223_multi_lot_from_direct_client_msp_ensuring(self):
        """Подача мультилотовой заявки 223 фз"""
        client = Client('772096797832', "", "", "",
                        "", "",
                        "", "", "")
        self.database_connect.cleanup_data_by_inn(client.inn)
        bid = Bid('32110073335', '69 451 527.61', '10000', '5 002.74', 10, BidType.ensuring, '', '', '', '',
                  BidLaw.fz223)
        bank_account = BankAccount()
        beneficiary = Beneficiary()

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        login_page.login_as_direct_client()

        create_bid_page = CreateBidPage(self.browser)
        create_bid_page.fill_required_fields(bid)
        create_bid_page.fill_field(create_bid_page.lot_number, '10')
        create_bid_page.click_on_create_bid_btn()

        create_bid_form = CreateBidForm(self.browser)
        create_bid_form.check_open()
        create_bid_form.check_form_data(bid)
        bid_id = create_bid_form.get_bid_id()

        agent_questionnaire = create_bid_form.go_to_bid()
        agent_questionnaire.check_open()

        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_client)
        info_about_client = InfoAboutClientForm(self.browser)
        info_about_client.fill_required_fields_bank_account(bank_account)
        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_client)

        agent_questionnaire.click_on_elem(agent_questionnaire.info_about_beneficiary)
        beneficiary_form = BeneficiaryForm(self.browser)
        beneficiary_form.fill_required_fields_beneficiary(beneficiary)

        docs_page = agent_questionnaire.open_docs_section()
        docs_page.check_open_direct_client()
        docs_page.load_passport_msp('file.jpg')

        login_page.go_to_login_page_and_clear_cache()
        login_page.login_as_bank()

        bank_page = BankPage(self.browser)
        bank_page.check_open()
        bank_page.set_required_users(bid_id)
        bank_page.open_bid(bid_id)
        bank_bid_common_page = BankBidCommonPage(self.browser)
        bank_bid_common_page.check_open()

    @unittest.skip('баг https://trello.com/c/wrxBmwwT, дописать тест')
    def test_guarantors(self):
        """заявка с поручителями и загрузкой доков через форму эцп"""

        client = Client('772096797832', "", "", "",
                        "", "",
                        "", "", "")
        self.database_connect.cleanup_data_by_inn(client.inn)
        bid = Bid('32110073335', '69 451 527.61', '11000000', '12 235.62', 10, BidType.ensuring, '', '', '', '',
                  BidLaw.fz223)
        bank_account = BankAccount()
        beneficiary = Beneficiary()
        administration = Administration()

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        agent_page = login_page.login_as_agent()
        bid_id = agent_page.create_bid_ip_and_get_bid_id(bid, client, bank_account, beneficiary)

        docs_page = DocsPage(self.browser)
        docs_page.load_docs_for_usual_bid_ip('file.jpg')
        eds_form = docs_page.open_EDS()
        eds_form.load_ip_usual_docs('file.jpg.sig')
        self.database_connect.check_bid_status(bid_id, 'Передано в Банк')

        login_page.go_to_login_page_and_clear_cache()
        bank_page = login_page.login_as_bank()
        bank_page.set_required_users(bid_id)
        bid_page = bank_page.open_bid(bid_id)
        bid_page.request_guarantor()

        login_page.go_to_login_page_and_clear_cache()
        agent_page = login_page.login_as_agent()
        inside_bid_page = agent_page.open_bid_use_filter(bid_id)
        surety_page = inside_bid_page.open_surety_section()
        surety_page.add_ur_surety(inn='7702773300')
        inside_surety = inside_bid_page.open_surety(1)
        inside_surety.fill_fields_surety_ur(bank_account, beneficiary, administration)
        inside_surety.load_docs('file.jpg', 1)
        docs_page.check_open_sign_link_for_usual()

    # @parameterized.expand([
    #     ("7708257207", "75104"),
    #     ("7714086422", "75103"),
    #     ("2457024893", "75100"),
    #     ("3438000232", "65000"),
    #     ("8709001880", "65100"),
    #     ("1701042988", "65141"),
    #     ("2540225637", "65142"),
    #     ("6504020536", "65143"),
    #     ("7710096395", "65200"),
    #     ("7711007101", "65241"),
    #     ("7705002602", "65242"),
    #     ("4909036682", "65243")
    # ])
    def test_gos_anketa(self):
        """ гос учреждения заполнение анкеты"""
        client = Client('7806023824', "", "", "",
                        "", "",
                        "", "", "")
        self.database_connect.cleanup_data_by_inn(client.inn)
        bid = Bid('32110073335', '69 451 527.61', '10000', '5 000', 10, BidType.ensuring, '', '', '', '',
                  BidLaw.fz223)
        bank_account = BankAccount()
        administration = Administration()

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        agent_page = login_page.login_as_agent()
        agent_page.check_open()
        bid_id = agent_page.create_bid_gos(bid, client, bank_account, administration)

        self.database_connect.check_bid_status(bid_id, 'Предложение направлено')

    def test_create_bid_api(self):
        """Подача заявки по апи"""
        bid = Bid("0338200005321000012", "344 433.50", "800 000", "37 172.6", 400,
                  BidType.execution, "23.04.2021", "Поставка лекарственных препаратов не ЖНВЛП",
                  "Российская Федерация, Камчатский край, Петропавловск-Камчатский г")
        client = Client('1901019320', "1021900532752", "190101001",
                        "Общество с ограниченной ответственностью \"Автодорпроект \"Трасса",
                        "ООО \"Автодорпроект \"Трасса", "655017, респ Хакасия, г Абакан, ул Вяткина, дом 3",
                        "12300", "95701000001", "71.11")
        customer = Customer(
            "Государственное бюджетное учреждение здравоохранения \"Камчатский краевой наркологический диспансер",
            "683024, край Камчатский, г Петропавловск-Камчатский, пр-кт 50 лет Октября, дом 2",
            "1024101036838",
            "4101036378", "410101001", "30701000001", "Камчатский край", "25.04.2000")
        bank_account = BankAccount()
        beneficiary = Beneficiary(birth_place="692001, Приморский край, Пожарский р-н, пгт Лучегорск",
                                  registration_address="край Приморский, пгт Лучегорск, р-н Пожарский",
                                  fio="Мелешева Мария Александровна")
        self.database_connect.cleanup_data_by_inn(client.inn)

        api = AgentApi()
        api.create_new_bid(bid, client, customer)

        api.put_data_into_bid_by_id(bid, client, customer, bank_account, beneficiary)
        api.upload_unsigned_package_passport_anketa(bid.id, 'file.jpg')
        api.upload_package_passport_anketa(bid.id, 'file.jpg.sig')
        api.transfer_to_bank(bid.id)

    def tearDown(self):
        self.browser.get_screenshot_as_file('screens/' + self._testMethodName + '.png')

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()


@unittest.skip("нерабочий препрод")
class TestPreprod(unittest.TestCase):
    browser = None

    @classmethod
    def setUpClass(cls):
        cls.browser = webdriver.Chrome()

    def testBki(self):
        bid = Bid("0320100018021000009", "67 874 332.80", "20 362 299.84", "3 311 437.78", 1429,
                  BidType.execution, "25.03.2021",
                  "Выполнение работ по противопаводковым мероприятиям на объекте: "
                  "Сиваковский межхозяйственный магистральный канал, с. Сиваковка,"
                  " Хорольского района, Приморского края (правая дамба канала)",
                  region="Российская Федерация, Приморский край, Хорольский р-н, Сиваковка с")
        with open("../config_connections.json", encoding='utf-8') as json_data_file:
            config_connections = json.load(json_data_file)
        login_page = LoginPage(self.browser)
        url = login_page.get_login_url(config_connections["stand_preprod"],
                                       config_connections["basic_user_preprod"]["username"],
                                       config_connections["basic_user_preprod"]["password"])
        client = Client('1901019320', "1021900532752", "190101001",
                        "Общество с ограниченной ответственностью \"Автодорпроект \"Трасса",
                        "ООО \"Автодорпроект \"Трасса", "655017, респ Хакасия, г Абакан, ул Вяткина, дом 3",
                        "12300", "95701000001", "71.11")

        base_page = BasePage(self.browser)
        self.browser = base_page.make_settings_and_return_driver()

        login_page.go_to_login_page_and_clear_cache(url)
        login_page.login_as_agent_preprod()

        agent_page = AgentPage(self.browser)
        agent_page.check_open()
        agent_page.click_on_create_bid_btn()

        create_bid_page = CreateBidPage(self.browser)
        create_bid_page.check_open()
        create_bid_page.fill_required_fields_client(bid, client)
        create_bid_page.fill_guarantee_price_field(bid)
        create_bid_page.click_on_elem(create_bid_page.create_btn)

        create_bid_form = CreateBidForm(self.browser)
        create_bid_form.check_open(100)
        self.bid_id = create_bid_form.get_bid_id()

        login_page.go_to_login_page_and_clear_cache(url)
        login_page.login_as_bank_preprod()

        bank_page = BankPage(self.browser)
        bank_page.check_open()
        bank_page.open_bid(self.bid_id)
        bank_bid_common_page = BankBidCommonPage(self.browser)
        bank_bid_common_page.check_open()
        bank_bid_common_page.change_status('Верификация')

        general_form_page = GeneralForm(self.browser)
        general_form_page.click_on_elem(general_form_page.get_accordeon_locator_by_text('Прикрепленные документы'))
        bank_bid_common_page.create_bki_report()

    def tearDown(self):
        self.browser.get_screenshot_as_file('screens/' + self._testMethodName + '.png')

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()


class TestWithoutBD(unittest.TestCase):
    browser = None

    @classmethod
    def setUpClass(cls):
        cls.browser = BasePage(cls.browser).make_settings_and_return_driver()

    def testMspCommissionMinExceedingAllowances(self):
        """МСП надбавки к тарифу минималке"""
        client = Client(inn="5260426216")
        bid = Bid("0338200005321000012", "344 433.50", "10 000.00", "5 000", 50,
                  BidType.execution, "23.04.2021", "Поставка лекарственных препаратов не ЖНВЛП",
                  "Российская Федерация, Камчатский край, Петропавловск-Камчатский г")
        commission = CommissionExpo("5000", "656,45", "802,45", bid.days_count, "0", "0", "8 992,51", "2000",
                                    "10 992,51")

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        agent_page = login_page.login_as_agent()
        agent_page.create_bid_first_form(bid, client)

        create_bid_form = CreateBidForm(self.browser)
        create_bid_form.click_on_elem(create_bid_form.go_to_bid_btn)

        agent_questionnaire = AgentQuestionnaire(self.browser)
        agent_questionnaire.check_open()
        self.bid_id = agent_questionnaire.get_bid_number()
        agent_questionnaire.click_on_elem(agent_questionnaire.docs)

        docs_page = DocsPage(self.browser)
        docs_page.check_open_express()
        docs_page.submit()

        commission_form = CommissionForm(self.browser)
        commission_form.check_open()

        commission_form.fill_elevation("2000")
        commission_form.accept_commission()

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        login_page.login_as_bank()

        bank_page = BankPage(self.browser)
        bank_page.check_open()
        bank_page.open_bid(self.bid_id)

        bid_offer = BidOfferPage(self.browser)
        bid_offer.check_open()
        bid_offer.check_loaded()
        bid_offer.set_checkbox_risk()
        bid_offer.set_checkbox_oversupplied()

        bank_commission = CommissionExpoForm(self.browser)
        bank_commission.open_exceeding_panel()

        exceeding = ExceedingForm(self.browser)
        exceeding.check_open()
        exceeding.add_exceeding_avance("10", '%')
        exceeding.add_exceeding_multilot("25", "% годовых")
        exceeding.add_exceeding_beneficiary("3000", '₽')
        exceeding.add_exceeding_surety('1.59', '%')
        exceeding.add_exceeding_optional('2.15', '% годовых')
        exceeding.save()
        bank_commission.check_tariff_expo(commission)

    def test_AO_submit_two_docs(self):
        """Проверка запрашиваемых документов у АО"""
        client = Client(inn="7621000359")
        bid = Bid("0338200005321000012", "344 433.50", "10 000.00", "5 000", 50,
                  BidType.execution, "23.04.2021", "Поставка лекарственных препаратов не ЖНВЛП",
                  "Российская Федерация, Камчатский край, Петропавловск-Камчатский г")

        login_page = LoginPage(self.browser)
        login_page.go_to_login_page_and_clear_cache()
        agent_page = login_page.login_as_agent()

        agent_page.create_bid_first_form(bid, client, check_form_data=False)

        create_bid_form = CreateBidForm(self.browser)
        create_bid_form.click_on_elem(create_bid_form.go_to_bid_btn)

        agent_questionnare = AgentQuestionnaire(self.browser)
        agent_questionnare.check_open()
        agent_questionnare.open_docs_section()

        docs_page = DocsPage(self.browser)
        docs_page.check_open_express()
        docs_page.load_doc_registry_ordering_AO('file.jpg')
        docs_page.wait_until_clickable(docs_page.submit_btn, 'xpath')
        docs_page.submit()

        commission_form = CommissionForm(self.browser)
        commission_form.check_open()

    def tearDown(self):
        self.browser.get_screenshot_as_file('screens/' + self._testMethodName + '.png')

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
