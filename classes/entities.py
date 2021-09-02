import datetime


class BidLaw:
    fz44 = '44-ФЗ'
    fz223 = '223-ФЗ'


class BidType:
    execution = 'Исполнение обязательств по контракту'
    ensuring = 'Обеспечение гарантийных обязательств'
    tender = 'Для обеспечения заявки на участие в конкурсе (тендерная гарантия)'


class Bid:
    number = None
    final_price = None
    guarantee_price = None
    commission = None
    days_count = None
    date_finish = None
    type = None
    law = None
    publish_date = None
    subject = None
    start_price = None
    region = None
    id = None

    def __init__(self, number, final_price, guarantee_price, commission, days_count, type, publish_date, subject, region,
                 start_price=None, law="44-ФЗ"):
        self.number = number
        self.final_price = final_price
        self.guarantee_price = guarantee_price
        self.commission = commission
        self.days_count = days_count
        self.date_finish = (datetime.date.today() + datetime.timedelta(days_count - 1)).strftime("%d.%m.%Y")
        self.type = type
        self.law = law
        self.publish_date = publish_date
        self.subject = subject
        if start_price is not None:
            self.start_price = start_price
        else:
            self.start_price = final_price
        self.region = region


class Client:
    inn = None
    ogrn = None
    kpp = None
    fullname = None
    short_name = None
    address = None
    okoph = None
    oktmo = None
    okved = None

    def __init__(self, inn, ogrn=None, kpp=None, fullname=None, short_name=None, address=None, okoph=None, oktmo=None,
                 okved=None):
        self.inn = inn
        self.ogrn = ogrn
        self.kpp = kpp
        self.fullname = fullname
        self.short_name = short_name
        self.address = address
        self.okved = okved
        self.oktmo = oktmo
        self.okoph = okoph


class BankAccount:
    """Сведения о клиенте/поручителе"""
    bank_account_number = None
    bank_bik = None
    contact_fio = None
    contact_email = None
    contact_phone_number = None
    bank_name = None
    bank_ks = None

    def __init__(self, bank_account_number="12345678912345678901",
                 bank_bik="044525974",
                 contact_fio="Мелешева Мария Александровна",
                 contact_email="maria@maria.ru",
                 contact_phone_number="77456321021"):
        self.bank_account_number = bank_account_number
        self.bank_bik = bank_bik
        self.contact_fio = contact_fio
        self.contact_email = contact_email
        self.contact_phone_number = contact_phone_number
        self.bank_name = 'АО "ТИНЬКОФФ БАНК"'
        self.bank_ks = '30101810145250000974'


class BankAccountOtp(BankAccount):
    workers_count = None
    work_with_bank = None
    share_largest_buyer = None
    property_availability = None

    def __init__(self, bank_account_number="12345678912345678901", bank_bik="044525974",
                 contact_fio="Мелешева Мария Александровна", contact_email="maria@maria.ru",
                 contact_phone_number="77456321021", workers_count=100, work_with_bank=">=50",
                 share_largest_buyer=">1 & <=3", property_availability="Да"):
        super().__init__(bank_account_number, bank_bik, contact_fio, contact_email, contact_phone_number)
        self.workers_count = workers_count
        self.work_with_bank = work_with_bank
        self.share_largest_buyer = share_largest_buyer
        self.property_availability = property_availability


class Beneficiary:
    """Сведения о бенефициарных владельцах"""
    gender = None
    birth_date = None
    birth_place = None
    passport_series = None
    passport_number = None
    passport_date_out = None
    passport_code = None
    passport_who_give = None
    registration_address = None
    fact_address = None
    contact_information = None
    inn = None
    fio = None
    part = None

    def __init__(self, gender="Мужской",
                 birth_date="10.01.1996",
                 birth_place="630000, Новосибирская обл, г Новосибирск, Заельцовский р-н, мкр Стрижи",
                 passport_series="1234", passport_number="789654", passport_date_out="01.01.2021",
                 passport_code="753-159", passport_who_give="отделом РФ по РФ",
                 registration_address="630000, Новосибирская обл, г Новосибирск, Заельцовский р-н, мкр Стрижи",
                 fact_address="124365, г Москва, г Зеленоград, поселок Крюково", contact_information="89642858477",
                 inn="231295190304", fio=None, part=None):
        self.gender = gender
        self.birth_date = birth_date
        self.birth_place = birth_place
        self.passport_series = passport_series
        self.passport_number = passport_number
        self.passport_date_out = passport_date_out
        self.passport_code = passport_code
        self.passport_who_give = passport_who_give
        self.registration_address = registration_address
        self.fact_address = fact_address
        self.contact_information = contact_information
        self.inn = inn
        if fio is not None:
            self.fio = fio
        if part is not None:
            self.part = part


class Administration:
    """Информация о структуре и персональном составе органов управления"""
    gender = None
    birth_date = None
    birth_place = None
    passport_series = None
    passport_number = None
    passport_date_out = None
    passport_code = None
    passport_who_give = None
    registration_address = None
    fact_address = None
    inn = None
    fio = None
    role = None

    def __init__(self, gender="Мужской",
                 birth_date="10.01.1996",
                 birth_place="630000, Новосибирская обл, г Новосибирск, Заельцовский р-н, мкр Стрижи",
                 passport_series="1234",
                 passport_number="789654",
                 passport_date_out="01.01.2021",
                 passport_code="753-159",
                 passport_who_give="отделом РФ по РФ",
                 registration_address="630000, Новосибирская обл, г Новосибирск, Заельцовский р-н, мкр Стрижи",
                 fact_address="124365, г Москва, г Зеленоград, поселок Крюково",
                 inn="231295190304", fio="Масыч Игорь Владимирович", role="Ликвидатор"):
        self.gender = gender
        self.birth_date = birth_date
        self.birth_place = birth_place
        self.passport_series = passport_series
        self.passport_number = passport_number
        self.passport_date_out = passport_date_out
        self.passport_code = passport_code
        self.passport_who_give = passport_who_give
        self.registration_address = registration_address
        self.fact_address = fact_address
        self.inn = inn
        self.role = role
        self.fio = fio


class BankField:
    field_name = None
    field_value = None
    field_can_be_edit = None

    def __init__(self, field_name, field_value, field_can_be_edit):
        self.field_name = str(field_name)
        self.field_value = str(field_value)
        self.field_can_be_edit = field_can_be_edit


class Customer:
    # поставщик
    full_orgname = None
    address = None
    ogrn = None
    inn = None
    kpp = None
    oktmo = None
    rf_subject = None
    tax_date_registration = None

    def __init__(self, full_orgname, address, ogrn, inn, kpp, oktmo, rf_subject, tax_date_registration):
        self.full_orgname = full_orgname
        self.address = address
        self.ogrn = ogrn
        self.inn = inn
        self.kpp = kpp
        self.oktmo = oktmo
        self.rf_subject = rf_subject
        self.tax_date_registration = tax_date_registration


class BankBidBasic:
    fields = None
    accordion_name = 'Основные параметры'

    def __init__(self, bid: Bid, principal: Customer, client: Client,
                 factor1="Нет", factor2="Нет", factor3="Нет", factor4="Нет",
                 factor5="Нет"
                 ):
        self.fields = []
        self.fields.append(BankField("Комиссия", bid.commission.replace('.', ','), False))
        self.fields.append(BankField("Полное наименование", client.fullname, True))
        self.fields.append(BankField("Краткое наименование", client.short_name, True))
        self.fields.append(BankField("Юридический адрес", client.address, True))
        self.fields.append(BankField("ОГРН", client.ogrn, False))
        self.fields.append(BankField("ИНН", client.inn, False))
        self.fields.append(BankField("КПП", client.kpp, True))
        self.fields.append(BankField("Номер закупки или ссылка", bid.number, True))
        self.fields.append(BankField("Закон исполнения торгов", bid.law, True))
        self.fields.append(BankField("Номер протокола", "", True))
        self.fields.append(BankField("Способ определения поставщика", "Электронный аукцион", False))
        self.fields.append(BankField("Дата публикации", bid.publish_date, False))
        self.fields.append(BankField("Начальная цена контракта", bid.start_price.replace('.', ','), True))
        self.fields.append(BankField("Итоговая сумма контракта", bid.final_price.replace('.', ','), True))
        self.fields.append(BankField("Полное наименование организации", principal.full_orgname, True))
        self.fields.append(BankField("Юридический адрес", principal.address, True))
        self.fields.append(BankField("ОГРН", principal.ogrn, True))
        self.fields.append(BankField("ИНН", principal.inn, True))
        self.fields.append(BankField(" КПП", principal.kpp, True))
        self.fields.append(BankField("Предмет контракта", bid.subject, True))
        self.fields.append(BankField("Тип БГ", bid.type, True))
        self.fields.append(BankField("Требуемая сумма", bid.guarantee_price.replace('.', ','), True))
        self.fields.append(BankField("Дата выдачи", datetime.date.today().strftime("%d.%m.%Y"), True))
        self.fields.append(BankField("Дата окончания", bid.date_finish, True))
        self.fields.append(BankField("Срок БГ, дней", bid.days_count, False))
        self.fields.append(BankField("БГ по форме Бенефициара", factor1, True))
        self.fields.append(BankField("Наличие аванса", factor2, True))
        self.fields.append(BankField("Бесспорное списание", factor3, True))
        self.fields.append(BankField("Подтверждение опыта исполнения контрактов", factor4, True))
        self.fields.append(BankField("Увеличение/продление срока контракта", factor5, True))


def get_commission_simple_text(field):
    return str(field).replace(" ", "").replace(",00000", "").replace(".", ",")


class Commission:
    tariff_percentage_per_annum = None
    effective_bank_rate = None
    actual_percentage_per_annum = None
    days_count = None
    discount = None
    tariff_result = None
    commission_bg = None
    kv = None
    kv_in_rubles = None

    def __init__(self, tariff_percentage_per_annum, effective_bank_rate, actual_percentage_per_annum, days_count,
                 discount,
                 tariff_result, commission_bg, kv, kv_in_rubles):
        self.tariff_percentage_per_annum = get_commission_simple_text(tariff_percentage_per_annum)
        self.effective_bank_rate = get_commission_simple_text(effective_bank_rate)
        self.actual_percentage_per_annum = get_commission_simple_text(actual_percentage_per_annum)
        self.days_count = get_commission_simple_text(days_count)
        self.tariff_result = get_commission_simple_text(tariff_result)
        self.discount = get_commission_simple_text(discount)
        self.commission_bg = get_commission_simple_text(commission_bg)
        self.kv = get_commission_simple_text(kv)
        self.kv_in_rubles = get_commission_simple_text(kv_in_rubles)


class CommissionExpo:
    tariff_percentage_per_annum = None
    effective_bank_rate = None
    actual_percentage_per_annum = None
    days_count = None
    discount = None
    agent_discount = None
    tariff_result = None
    elevation = None
    elevation_percentage = None
    commission = None

    def __init__(self, tariff_percentage_per_annum, effective_bank_rate, actual_percentage_per_annum, days_count,
                 bank_discount, agent_discount,
                 tariff_result, elevation, commission):
        self.commission = commission
        self.elevation_percentage = "60"
        self.elevation = elevation
        self.agent_discount = agent_discount
        self.tariff_percentage_per_annum = get_commission_simple_text(tariff_percentage_per_annum)
        self.effective_bank_rate = get_commission_simple_text(effective_bank_rate)
        self.actual_percentage_per_annum = get_commission_simple_text(actual_percentage_per_annum)
        self.days_count = get_commission_simple_text(days_count)
        self.tariff_result = get_commission_simple_text(tariff_result)
        self.discount = get_commission_simple_text(bank_discount)


class BankBidInfoAccordion:
    fields = None
    accordion_name = 'Сведения о гарантии, контракте и заказчике'

    def __init__(self, bid: Bid, principal: Customer, factor1="Нет", factor2="Нет", factor3="Нет",
                 factor4="Нет",
                 factor5="Нет"
                 ):
        self.fields = []
        self.fields.append(BankField("Гарантия на", bid.type, True))
        self.fields.append(BankField("Номер закупки", bid.number, True))
        # self.fields.append(BankField("Номер лотов", "", False))
        self.fields.append(BankField("ИНН заказчика", principal.inn, True))
        self.fields.append(BankField("Предмет контракта", bid.subject, True))
        # self.fields.append(BankField("ОКПД2", okpd2, False))
        self.fields.append(BankField("Наименование заказчика", principal.full_orgname, True))
        self.fields.append(BankField("ОКТМО заказчика", principal.oktmo, True))
        self.fields.append(BankField("Наименование субъекта РФ заказчика", principal.rf_subject, True))
        self.fields.append(
            BankField("Дата постановки заказчика на учёт в налоговом органе", principal.tax_date_registration, True))
        self.fields.append(BankField("Начальная цена контракта", bid.start_price.replace('.', ','), True))
        self.fields.append(BankField("Предложенная нами цена", bid.final_price.replace('.', ','), True))
        self.fields.append(BankField("Регион оказания услуг/выполнение работ в контракте", bid.region, True))
        self.fields.append(BankField("Наличие аванса", factor1, True))
        self.fields.append(BankField("Условие бесспорного списания", factor2, True))
        self.fields.append(BankField("БГ по форме бенефициара", factor3, True))
        self.fields.append(BankField("Подтверждение опыта исполнения контрактов", factor4, True))
        self.fields.append(BankField("Увеличение/продление срока контракта", factor5, True))
        # self.fields.append(BankField("Дата подписания государственного контракта", "", False))


class BankBidInfoAboutClientAccordion:
    fields = None
    accordion_name = 'Сведения о клиенте'

    def __init__(self, client: Client, bank_account: BankAccount, beneficiary: Beneficiary):
        self.fields = []
        self.fields.append(BankField("ИНН", client.inn, False))
        self.fields.append(BankField("КПП", client.kpp, True))
        self.fields.append(BankField("Наименование", client.fullname, True))
        self.fields.append(BankField("Краткое наименование", client.short_name, True))
        self.fields.append(BankField("ОКОПФ", client.okoph, True))
        self.fields.append(BankField("ОКТМО", client.oktmo, True))
        self.fields.append(BankField("ОКВЭД", client.okved, True))
        self.fields.append(BankField("р.с. клиента", bank_account.bank_account_number, True))
        self.fields.append(BankField("БИК банка", bank_account.bank_bik, True))
        self.fields.append(BankField("Наименование банка", bank_account.bank_name, False))
        self.fields.append(BankField("к/с банка", bank_account.bank_ks, False))
        self.fields.append(BankField("Юридический адрес", client.address, True))
        self.fields.append(
            BankField("По адресу, указанному в ЕГРЮЛ, орган или представитель клиента отсутствует", "Нет", False))
        if beneficiary.fact_address == beneficiary.registration_address or len(client.inn) == 10:
            self.fields.append(BankField("Фактический адрес", "Соответствует юридическому адресу", True))
        else:
            self.fields.append(BankField("Фактический адрес", beneficiary.fact_address, True))
        self.fields.append(BankField("Почтовый адрес", "Соответствует", True))
        self.fields.append(BankField("Контактное лицо", bank_account.contact_fio, True))
        self.fields.append(BankField("Контактный e-mail", bank_account.contact_email, True))
        # self.fields.append(BankField("Контактный телефон", bank_account.contact_phone_number, True))
        # self.fields.append(BankField("Добавочный номер","", ))
        # self.fields.append(BankField("Веб-сайт",, ))
        self.fields.append(BankField("Страной регистрации (учреждения) Вашей организации является США", "Нет", False))
        self.fields.append(BankField("Ваша организация является налоговым резидентом США", "Нет", False))
        self.fields.append(BankField("Физические лица, являющиеся налоговыми резидентами США", "Нет", False))
        self.fields.append(BankField("Юридические лица, которые зарегистрированы/учреждены в США", "Нет", False))
        self.fields.append(BankField(
            "Подлежит ли сделка согласованию органом управления общества в соотвествии с положениями устава общества, ограничивающими полномочия единоличного исполнительного органа ?",
            "Нет", False))
        self.fields.append(BankField(
            "Отсутствие на последнюю отчетную дату у Клиента собственных либо находящихся в пользовании на основании договора аренды основных средств или иного имущества, необходимых для осуществления деятельности (производственных мощностей, складских помещений, транспортных средств, торговых точек, офисных помещений и прочих), в том числе переданных в залог",
            "Нет", False))
        self.fields.append(
            BankField("Клиент входит в перечень стратегических предприятий в соответствии с 213-ФЗ", "Нет", False))
        self.fields.append(BankField(
            "Клиент имеет задолженность перед федеральным бюджетом, бюджетами Российской Федерации, местными бюджетами и внебюджетными фондами",
            "Нет", False))
        self.fields.append(BankField(
            "Клиент имеет текущую картотеку неоплаченных расчетных документов к банковским счетам Клиента", "Нет",
            False))
        self.fields.append(
            BankField("Клиент имеет просроченную задолженность перед работниками по заработной плате", "Нет", False))
        self.fields.append(BankField(
            "Клиент имеет просроченную дебиторскую и/или кредиторскую задолженность, просроченные собственные векселя длительностью свыше 3 месяцев в размере более 25% от общего объема соответствующей задолженности или неликвидные запасы готовой продукции/сырья/материалов и т.п. в размере равном или более 25%  валюты баланса Клиента на последнюю календарную квартальную дату"
            , "Нет", False))
        self.fields.append(BankField(
            "Наличие действующих кредитных продуктов (кредиты, овердрафты, банковские гарантии (кроме Экспресс-гарантий), непокрытые аккредитивы) в банке",
            "Нет", False))
        self.fields.append(
            BankField("Наличие лицензий на право осуществления деятельности, подлежащей лицензированию", "Нет", False))


class BankBidInfoAboutStructure:
    fields = None
    accordion_name = 'Информация о структуре и персональном составе органов управления'

    def __init__(self, administration: Administration):
        self.fields = []
        self.fields.append(
            BankField("Исполнительным органом Клиента является", "Единоличный исполнительный орган", True))
        self.fields.append(
            BankField("Наименование должности единоличного исполнительного органа", administration.role, True))
        self.fields.append(BankField("ФИО", administration.fio, True))
        self.fields.append(BankField("Пол", administration.gender, True))
        self.fields.append(BankField("Дата рождения", administration.birth_date, True))
        self.fields.append(BankField("Место рождения", administration.birth_place, True))
        self.fields.append(BankField("ИНН", administration.inn, True))
        self.fields.append(BankField("Вид ДУЛ", "Паспорт РФ", True))
        self.fields.append(BankField("Серия", administration.passport_series, True))
        self.fields.append(BankField("Номер", administration.passport_number, True))
        self.fields.append(BankField("Дата выдачи", administration.passport_date_out, True))
        self.fields.append(BankField("Код подразделения", administration.passport_code, True))
        self.fields.append(BankField("Кем выдан", administration.passport_who_give, True))
        self.fields.append(BankField("Адрес регистрации", administration.registration_address, True))
        self.fields.append(BankField("Фактический адрес", administration.fact_address, True))
        self.fields.append(BankField("Доля в бизнесе", "0", True))
        self.fields.append(
            BankField("Является ли указанный единоличный исполнительный орган подписантом по договору", "Да", True))


class Stockholder:
    number = None
    fio = None
    percentage = None
    inn = None

    def __init__(self, fio, inn, percentage, number):
        self.percentage = percentage
        self.fio = fio
        self.inn = inn
        self.number = number
