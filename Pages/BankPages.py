import time

from Pages.BasePages import Alert
from Pages.BasePages import BasePage, Base, Loaders
from classes.entities import CommissionExpo, Commission


class BankPage(BasePage):
    bank_btn = 'a .btn.btn-outline'

    def get_str_by_bid(self, bid_id):
        return '//tr[@data-id="' + bid_id + '"]'

    def get_btn_by_bid_id_and_text(self, bid_id, text):
        locator = self.get_str_by_bid(
            bid_id) + "//td[contains(@class, 'bid-agent-col')]" \
                      "//strong[text()[contains(.,'" + text + "')]]/.." \
                                                              "/following-sibling::" \
                                                              "div[text()[contains(.,'Назначить себя')]]"
        return locator

    def set_required_users(self, bid_id):
        self.click_on_elem(self.get_btn_by_bid_id_and_text(bid_id, 'Вериф'))
        self.browser.refresh()
        self.check_open()
        self.click_on_elem(self.get_btn_by_bid_id_and_text(bid_id, 'Андер'))
        self.check_open()
        self.click_on_elem(self.get_btn_by_bid_id_and_text(bid_id, 'Выдача'))
        self.check_open()

    def check_open(self):
        self.wait_until_located(self.bank_btn, 'css')
        Loaders(self.browser).wait_until_bank_loader_disappear(10)

    def open_bid(self, bid_id):
        self.click_on_elem(self.get_str_by_bid(bid_id))
        bank_bid_page = BankBidCommonPage(self.browser)
        bank_bid_page.check_open()
        return bank_bid_page


class BankBidCommonPage(BasePage):
    prof_text = 'Профсуждение'
    proposal_text = 'Предложение'
    change_status_select = '[id="change-status"]'
    create_bki_report_btn = '//button[text()[contains(.,"Сформировать и проверить отчет БКИ")]]'
    request_guarantor_btn = '//button[text()[contains(.,"Запросить поручителя")]]'

    def get_menu_item_locator_by_text(self, text):
        return '//div[text()[contains(.,"' + text + '")]]'

    def check_open(self):
        self.wait_until_located(self.get_menu_item_locator_by_text('Профсуждение'), 'xpath')

    def select_menu_item(self, text):
        elem_locator = self.get_menu_item_locator_by_text(text)
        self.wait_until_located(elem_locator, 'xpath')
        self.click_on_elem(elem_locator)

    def change_status(self, new_status):
        self.click_on_elem(self.change_status_select)
        status_selector = '//option[text()[contains(.,"' + new_status + '")]]'
        self.click_on_elem(status_selector)
        alert_obj = self.browser.switch_to.alert
        alert_obj.accept()
        loaders = Loaders(self.browser)
        loaders.wait_until_bank_loader_disappear(40)

    def create_bki_report(self):
        good_result = '//span[text()[contains(.,"Просрочек не обнаружено")]]'
        self.click_on_elem(self.create_bki_report_btn)
        loaders = Loaders(self.browser)
        loaders.wait_until_bank_loader_disappear(70)
        self.find_element_by_locator(good_result)

    def request_guarantor(self):
        self.wait_until_clickable(self.request_guarantor_btn, 'xpath')
        self.click_on_elem(self.request_guarantor_btn)
        self.wait_until_disappear(self.request_guarantor_btn, 'xpath')


class GeneralForm(BasePage):
    input_yes = '//label[text()[contains(.,"Соответствует")]]/input'

    def get_accordeon_locator_by_text(self, text):
        return '//strong[text()[contains(.,"' + text + '")]]'

    def select_radio_result(self, accordeon_locator):
        self.click_on_elem(accordeon_locator)
        self.click_on_elem(self.input_yes)
        self.click_on_elem(accordeon_locator)

    def select_required_locators_for_usual(self):
        locators = [self.get_accordeon_locator_by_text(
            'Информация о структуре и персональном составе органов управления'), self.get_accordeon_locator_by_text(
            'Сведения о бенефициарных владельцах'), self.get_accordeon_locator_by_text(
            'Финансовые показатели'), self.get_accordeon_locator_by_text('Прикрепленные документы')]

        for locator in locators:
            self.select_radio_result(locator)

    def select_required_locators_without_finance(self):
        locators = [self.get_accordeon_locator_by_text(
            'Информация о структуре и персональном составе органов управления'), self.get_accordeon_locator_by_text(
            'Сведения о бенефициарных владельцах'), self.get_accordeon_locator_by_text(
            'Прикрепленные документы')]

        for locator in locators:
            self.select_radio_result(locator)

    def select_required_locators_for_msp_ip(self):
        locators = [self.get_accordeon_locator_by_text(
            'Сведения о бенефициарных владельцах'), self.get_accordeon_locator_by_text(
            'Финансовые показатели'), self.get_accordeon_locator_by_text(
            'Прикрепленные документы')]

        for locator in locators:
            self.select_radio_result(locator)

    def check_bank_accordion_data(self, entity):
        locator_accordion = self.get_accordeon_locator_by_text(entity.accordion_name)
        self.click_on_elem(locator_accordion)
        for field in entity.fields:
            if field.field_can_be_edit:
                locator = '//div//label[text()[contains(.,"' \
                          + field.field_name + '")]]/../following-sibling::div//span[text()[contains(.,\'' + \
                          field.field_value + '\')]]'
            else:
                locator = '//div//label' \
                          '[text()[contains(.,"' + field.field_name + '")]]' \
                                                                      '/../following-sibling' \
                                                                      '::div//label[text()[contains(.,\'' + \
                          field.field_value + '\')]]'
            self.find_element_by_locator(locator)
        self.click_on_elem(locator_accordion)

    def update_fin(self, section, year, quarter, value):
        locator = '[name="' + section + quarter + '.' + year + '"]'

        locator_accordion = self.get_accordeon_locator_by_text('Финансовые показатели')
        self.click_on_elem(locator_accordion)
        elem = self.find_element_by_locator(locator)
        self.scroll_into_view_by_elem(elem)
        elem.click()
        elem.clear()
        elem.send_keys(value)
        self.click_on_elem(locator_accordion)


class ProfilePage(BasePage):
    update_prof_btn = '//button[text()[contains(.,"Обновить расчет")]]'
    yes = 'Соответствует'
    calculate_btn = '//div[text()[contains(.,"Рассчитать и сохранить")]]'
    tbody = '//div[text()[contains(.,"Расчеты рейтинга")]]/..//tbody/tr/td'
    prof_text = 'Профсуждение'
    report_text = 'Отчет о проверке и идентификации клиента'
    decision_text = 'Решение о выпуске БГ'
    danger_txt = '.text-danger'
    use = '//div[text()[contains(.,"Расчеты рейтинга")]]/..//tbody/tr//input'

    def calculate(self):
        self.click_on_elem(self.calculate_btn)
        self.wait_until_located(self.use, 'xpath')

    def check_calculated(self):
        self.find_elements_by_locator(self.tbody)
        Loaders(self.browser).wait_until_bank_loader_disappear()

    def get_select_by_text(self, text):
        return '/following-sibling::div/label[text()[contains(.,"' + text + '")]]/input'

    def get_stop_factor_locator_by_text(self, text):
        return '//div[text()[contains(.,"' + text + '")]]'

    def check_open(self):
        self.wait_until_located(self.update_prof_btn, 'xpath')

    def get_stop_factor_selector_by_text(self, text, value='Соответствует'):
        return self.get_stop_factor_locator_by_text(text) + self.get_select_by_text(value)

    def select_required_factors(self, stop_factors):
        for stop_factor in stop_factors:
            if stop_factors[stop_factor]['value'] != "Соответствует":
                str_select_yes = self.get_stop_factor_selector_by_text(stop_factors[stop_factor]['text'])
                self.click_on_elem(str_select_yes)

    def get_cell_number_by_text(self, text):
        headings_th = '//div[text()[contains(.,"Расчеты рейтинга")]]/..//table//th'
        from selenium.webdriver.common.by import By

        elem = (By.ID, 'div')
        headings_elems = self.find_elements_by_locator(headings_th)

        i = 0
        while i < len(headings_elems):
            elem_text = headings_elems[i].text
            if elem_text == text:
                return i
            i = i + 1

    def get_cell_text_by_id(self, id):
        locators = '//div[text()[contains(.,"Расчеты рейтинга")]]/..//tbody//td'
        return self.find_elements_by_locator(locators)[id].text

    def check_ratings_results(self, rating=None, category=None, financial=None, ratingMSB=None):

        check_table = {'Балл': rating,
                       'Категория': category,
                       'Фин положение': financial,
                       'Рейтинг МСБ': ratingMSB}

        for key in check_table:
            if check_table[key] is not None:
                number = self.get_cell_number_by_text(key)
                text = self.get_cell_text_by_id(number)
                self.assertEqual(text, check_table[key])

    def use_rating(self):
        self.click_on_elem(self.tbody + '//input')

    def get_generate_btn_locator(self, btn_text):
        return '//div[text()[contains(.,"' + btn_text + '")]]/following-sibling::div/button[text()[contains(.,"Генерировать")]]'

    def get_download_btn_locator(self, btn_text):
        return '//div[text()[contains(.,"' + btn_text + '")]]/following-sibling::div/button[text()[contains(.,"Генерировать")]]'

    def generate_doc_by_name(self, doc_name):
        self.click_on_elem(self.get_generate_btn_locator(doc_name))
        self.check_download_locator(doc_name)
        self.wait_until_disappear(Loaders(self.browser).loaderBank, 'css')

    def get_approve_btn_locator(self, doc_text, approved=False):
        if not approved:
            return '//div[text()[contains(.,"' + doc_text + '")]]/following-sibling::div//button[text()[contains(.,"Подтвердить")]]'
        else:
            return '//div[text()[contains(.,"' + doc_text + '")]]/following-sibling::div//button[text()[contains(.,"Снять подтверждение")]]'

    def approve_doc(self, doc_name):
        self.click_on_elem(self.get_approve_btn_locator(doc_name))
        self.click_on_elem(Alert(self.browser).yes_btn)
        self.wait_until_located(self.get_approve_btn_locator(doc_name, approved=True), 'xpath')

    def get_download_locator(self, locator_text):
        locator = '//div[text()="' + locator_text + '"]/following-sibling::div/a[text()[contains(.,"Скачать")]]'
        return locator

    def check_download_locator(self, locator_text):
        locator = '//div[text()="' + locator_text + '"]/following-sibling::div/a[text()[contains(.,"Скачать")]]'
        self.wait_until_located(locator, 'xpath')

    def check_stop_factors(self, json_stop_factors):
        self.update_prof()
        for stop_factor in json_stop_factors:
            self.find_element_by_locator(self.get_stop_factor_locator_by_text(json_stop_factors[stop_factor]['text']))
        actual_stop_factors_count = len(self.find_elements_by_locator('//label[text()[contains(.,"Соответствует")]]'))
        expected_stop_factors_count = len(json_stop_factors)
        self.assertEqual(expected_stop_factors_count, actual_stop_factors_count)

    def check_selected_default(self, json_stop_factors):
        for stop_factor in json_stop_factors:
            locator = self.get_stop_factor_selector_by_text(json_stop_factors[stop_factor]['text'],
                                                            json_stop_factors[stop_factor]['value'])
            self.check_selected(locator)

    def update_prof(self):
        self.click_on_elem(self.update_prof_btn)
        try:
            self.wait_until_located(Loaders(self.browser).loaderBank, 'css')
        except:
            pass
        self.wait_until_disappear(Loaders(self.browser).loaderBank, 'css', 40)


class BidOfferPage(BasePage):
    choose_sign_select = '//span[text()[contains(.,"Подписант")]]/../following-sibling::select'
    send_to_client_btn = '//button[text()[contains(.,"Подтвердить и направить клиенту")]]'
    commission_inputs = "//table[contains(@class, 'commission-table')]//input"
    check_company_data_btn = '//button[text()[contains(.,"Проверить данные компании")]]'
    transfer_to_sign_btn = '//button[text()[contains(.,"Передать на подпись")]]'
    sign_btn = '//button[text()[contains(.,"Подписать документы")]]'
    payment_checkbox = 'table [type="checkbox"]'
    guarantee_scan = '[id="bg_warranty_file"]'
    coefficient_btn = '//button[text()[contains(.,"Повышающие коэффициенты")]]'

    risk_checkbox = '#bid-is-risky-checkbox'
    oversupplied_checkbox = '#bid-is-oversupply-checkbox'

    def set_checkbox_risk(self):
        self.click_on_elem(self.risk_checkbox)
        Toast(self.browser).wait_until_message_appear(Toast(self.browser).message_risk)

    def set_checkbox_oversupplied(self):
        self.click_on_elem(self.oversupplied_checkbox)
        Toast(self.browser).wait_until_message_appear(Toast(self.browser).message_oversupplied)

    def check_loaded(self):
        self.wait_until_located(self.coefficient_btn, 'xpath')

    def transfer_to_sign(self, filename):
        self.click_on_elem(self.payment_checkbox)
        self.find_element_by_locator(self.guarantee_scan).send_keys(Base().get_file_dir('files', filename))
        self.wait_until_clickable(self.transfer_to_sign_btn, 'xpath')
        self.click_on_elem(self.transfer_to_sign_btn)
        self.wait_until_located(self.sign_btn, 'xpath')

    def __get_check_company_data_text_result(self, text):
        locator = '//h5[text()[contains(.,"' + text + '")]]//following-sibling::span'
        self.wait_until_located(locator, 'xpath')
        return self.get_text(locator)

    def check_success_company_data(self, check_egr=True):
        connected_company_locator = '//h5[text()[contains' \
                                    '(.,"Связанные компании (наименование, ИНН, номера заявок и их статус):")]]' \
                                    '//following-sibling::div/span'

        self.wait_until_clickable(self.check_company_data_btn, 'xpath')
        self.click_on_elem(self.check_company_data_btn)
        self.wait_until_clickable(self.check_company_data_btn, 'xpath')
        res = self.__get_check_company_data_text_result('Паспорта')
        self.assertEqual(res, 'Действительны')
        res = self.__get_check_company_data_text_result('Безусловные факторы')
        self.assertEqual(res, 'Данные совпадают')
        if check_egr:
            res = self.__get_check_company_data_text_result('Данные ЕГРЮЛ')
            self.assertEqual(res, 'Данные совпадают')
        res = self.get_text(connected_company_locator)
        self.assertEqual(res, 'Заявок нет')

    def check_open(self):
        self.wait_until_located(self.choose_sign_select, 'xpath')
        Loaders(self.browser).wait_until_bank_loader_disappear(10)

    def select_signer(self, text='Непросроченный Подписант Подписантович обычная (2028-07-08)'):
        self.select_elem(self.choose_sign_select, text)

    def send_to_client(self):
        self.click_on_elem(self.send_to_client_btn)
        self.wait_until_disappear(self.send_to_client_btn, locator_type='xpath')

    def check_tariff(self, commission: Commission):
        elems = self.find_elements_by_locator(self.commission_inputs)
        fact_values = []
        expect_values = []
        for elem in elems:
            # удалить лишние нули и пробелы
            fact_values.append(
                elem.get_attribute('value').replace(" ", "").replace(",00000", "").replace(".", ","))
        expect_values.append(commission.tariff_percentage_per_annum)
        expect_values.append(commission.effective_bank_rate)
        expect_values.append(commission.actual_percentage_per_annum)
        expect_values.append(commission.days_count)
        expect_values.append(commission.discount)
        expect_values.append(commission.tariff_result)
        expect_values.append(commission.commission_bg)
        expect_values.append(commission.kv)
        expect_values.append(commission.kv_in_rubles)

        self.assertEqual(expect_values, fact_values)


class CommissionExpoForm(BasePage):
    tariff_percentage_per_annum = '//div[text()[contains(.,"Тариф")]]//input'
    effective_bank_rate = '//div[text()[contains(.,"Эффективная ставка банка")]]//input'
    actual_percentage_per_annum = '//div[text()[contains(.,"Факт. % годовых")]]//input'
    days_count = '//div[text()[contains(.,"Срок")]]//input'
    bank_discount = '//div[text()[contains(.,"Скидка от банка")]]//input'
    tariff_result = '//div[text()[contains(.,"Тариф, ₽")]]//input'
    agent_discount = '//div[text()[contains(.,"Скидка от агента")]]//input'
    exceeding = '//div[text()[contains(.,"Превышение, ₽")]]//input'
    exceeding_percentage = '//div[text()[contains(.,"Доля превышения агента, %")]]//input'
    commission = '//div[text()[contains(.,"Комиссия БГ, ₽")]]//input'
    exceeding_btn = '//button[text()[contains(.,"Повышающие коэффициенты")]]'

    def get_clean_number(self, value):
        return value.replace(" ", "").replace(",00000", "").replace(",00", "").replace(".", ",")

    def check_tariff_expo(self, commission: CommissionExpo):
        fact_values = []
        expect_values = []
        expect_values.append(self.get_clean_number(commission.tariff_percentage_per_annum))
        expect_values.append(self.get_clean_number(commission.effective_bank_rate))
        expect_values.append(self.get_clean_number(commission.actual_percentage_per_annum))
        expect_values.append(self.get_clean_number(commission.days_count))
        expect_values.append(self.get_clean_number(commission.discount))
        expect_values.append(self.get_clean_number(commission.agent_discount))
        expect_values.append(self.get_clean_number(commission.tariff_result))
        expect_values.append(self.get_clean_number(commission.elevation))
        expect_values.append(self.get_clean_number(commission.elevation_percentage))
        expect_values.append(self.get_clean_number(commission.commission))

        fact_values.append(self.get_clean_number(self.get_field_value(self.tariff_percentage_per_annum)))
        fact_values.append(self.get_clean_number(self.get_field_value(self.effective_bank_rate)))
        fact_values.append(self.get_clean_number(self.get_field_value(self.actual_percentage_per_annum)))
        fact_values.append(self.get_clean_number(self.get_field_value(self.days_count)))
        fact_values.append(self.get_clean_number(self.get_field_value(self.bank_discount)))
        fact_values.append(self.get_clean_number(self.get_field_value(self.agent_discount)))
        fact_values.append(self.get_clean_number(self.get_field_value(self.tariff_result)))
        fact_values.append(self.get_clean_number(self.get_field_value(self.exceeding)))
        fact_values.append(self.get_clean_number(self.get_field_value(self.exceeding_percentage)))
        fact_values.append(self.get_clean_number(self.get_field_value(self.commission)))

        self.assertEqual(expect_values, fact_values)

    def change_bank_discount(self, new_discount):
        self.fill_field(self.bank_discount, new_discount)
        self.click_on_elem(self.agent_discount)
        message = Toast(self.browser)
        message.wait_until_message_appear()
        message.wait_until_message_disappear()

    def change_agent_discount(self, new_discount):
        self.fill_field(self.agent_discount, new_discount)
        self.click_on_elem(self.bank_discount)
        message = Toast(self.browser)
        message.wait_until_message_appear()
        message.wait_until_message_disappear()

    def open_exceeding_panel(self):
        self.click_on_elem(self.exceeding_btn)


class ExceedingForm(BasePage):
    panel = "//h5[contains(@id, 'guarantor-types-label')]/../.."
    close_btn = '//button[text()[contains(.,"Закрыть")]]'

    avans_checkbox = '#ALLOWANCES_AVANS_checkbox'
    avans_input = "//input[contains(@id, 'ALLOWANCES_AVANS_input')]"
    avans_select_locator = "//input[contains(@id, 'ALLOWANCES_AVANS_input')]//following-sibling::select"

    multilot_checkbox = '#ALLOWANCES_MULTILOT_checkbox'
    multilot_input = "//input[contains(@id, 'ALLOWANCES_MULTILOT_input')]"
    multilot_select_locator = "//input[contains(@id, 'ALLOWANCES_MULTILOT_input')]//following-sibling::select"

    beneficiary_checkbox = '#ALLOWANCES_FORM_BENEFICIARY_checkbox'
    beneficiary_input = "//input[contains(@id, 'ALLOWANCES_FORM_BENEFICIARY_input')]"
    beneficiary_select_locator = "//input[contains(@id, 'ALLOWANCES_FORM_BENEFICIARY_input')]//following-sibling::select"

    surety_checkbox = '#ALLOWANCES_ADDITIONAL_PROVISION_checkbox'
    surety_input = "//input[contains(@id, 'ALLOWANCES_ADDITIONAL_PROVISION_input')]"
    surety_select_locator = "//input[contains(@id, 'ALLOWANCES_ADDITIONAL_PROVISION_input')]//following-sibling::select"

    optional_checkbox = "#ALLOWANCES_ARBITRARY_COEFFICIENT_checkbox"
    optional_input = "//input[contains(@id, 'ALLOWANCES_ARBITRARY_COEFFICIENT_input')]"
    optional_select_locator = "//input[contains(@id, 'ALLOWANCES_ARBITRARY_COEFFICIENT_input')]//following-sibling::select"

    save_btn = '//button[text()[contains(.,"Сохранить")]]'

    def check_open(self):
        self.wait_until_located(self.panel, 'xpath')

    def __add_exceeding(self, checkbox_locator, field_locator, select_locator, text_type, value):
        self.click_on_elem(checkbox_locator)
        self.select_elem(select_locator, text_type, select_locator)
        self.fill_field_and_check_value(field_locator, value, 'xpath')

    def add_exceeding_avance(self, value, text_type):
        self.__add_exceeding(self.avans_checkbox, self.avans_input, self.avans_select_locator, text_type, value)

    def add_exceeding_multilot(self, value, text_type):
        self.__add_exceeding(self.multilot_checkbox, self.multilot_input, self.multilot_select_locator, text_type,
                             value)

    def add_exceeding_beneficiary(self, value, text_type):
        self.__add_exceeding(self.beneficiary_checkbox, self.beneficiary_input, self.beneficiary_select_locator,
                             text_type, value)

    def add_exceeding_surety(self, value, text_type):
        self.__add_exceeding(self.surety_checkbox, self.surety_input, self.surety_select_locator, text_type,
                             value)

    def add_exceeding_optional(self, value, text_type):
        self.__add_exceeding(self.optional_checkbox, self.optional_input, self.optional_select_locator, text_type,
                             value)

    def close(self):
        self.click_on_elem(self.panel + self.close_btn)
        self.wait_until_disappear(self.panel, 'xpath')

    def save(self):
        self.click_on_elem(self.panel + self.save_btn)
        self.wait_until_disappear(self.panel, 'xpath')
        Toast(self.browser).wait_until_message_appear()
        Toast(self.browser).wait_until_message_disappear()


class Toast(BasePage):
    """Сообщение о изменении комиссии"""
    message_commission = '//div[text()[contains(.,"Данные о комиссии изменены")]]'
    message_risk = '//div[text()[contains(.,"Риски установлены")]]'
    message_oversupplied = '//div[text()[contains(.,"Переобеспечение установлено")]]'

    def wait_until_message_appear(self, message=message_commission):
        self.wait_until_located(message, 'xpath')

    def wait_until_message_disappear(self):
        self.wait_until_disappear(self.message_commission, 'xpath')
