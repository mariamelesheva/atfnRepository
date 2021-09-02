import datetime

import requests
import unittest
import json

from Pages.BasePages import Base
from classes.entities import Bid, BidType, Client, Customer, BankAccount, Beneficiary


class AgentApi(unittest.TestCase, Base):
    with open("config_connections.json") as json_data_file:
        stand = json.load(json_data_file)['stand']
    api_url = 'https://' + stand + '/api/v1/bids/'
    with open("config_connections.json") as json_data_file:
        basic_authorization = json.load(json_data_file)['authorization']
    with open("config_connections.json") as json_data_file:
        token = json.load(json_data_file)['token']

    def upload_package_otp_usual(self, bid_id, filename):
        url = self.api_url + str(bid_id) + '/document/package/upload'

        file_dir = Base().get_file_dir('files', filename)
        file = open(file_dir, 'rb')
        file1 = open(file_dir, 'rb')
        file2 = open(file_dir, 'rb')
        file3 = open(file_dir, 'rb')
        file4 = open(file_dir, 'rb')
        file5 = open(file_dir, 'rb')
        file6 = open(file_dir, 'rb')
        file7 = open(file_dir, 'rb')
        file8 = open(file_dir, 'rb')

        values = {'certificate[expiration]': "2021-06-16",
                  'certificate[from]': "2021-03-16",
                  'certificate[issuer]': "CN=CRYPTO-PRO Test Center 2, O=CRYPTO-PRO LLC, L=Moscow, C=RU, E=support@cryptopro.ru",
                  'certificate[selectValue]': "qwe",
                  'certificate[serial]': "1200513B7743AFB99E76084EDD000100513B77",
                  'certificate[subject]': "CN=maria0",
                  'certificate[thumbprint]': "28333F412221A88AC766B5433541F7BF3A34C2DC",
                  'documents[0][file_name]': "doc_anketa",
                  'documents[1][file_name]': "doc_client_buh_report",
                  'documents[2][file_name]': "doc_order_current_redaction",
                  'documents[3][file_name]': "doc_executor_nomination",
                  'documents[4][file_name]': "doc_bug_year_report",
                  'documents[5][file_name]': "doc_tax_return",
                  'documents[6][file_name]': "doc_individual_identity_document",
                  'documents[7][file_name]': "doc_client_locate_fact",
                  'documents[8][file_name]': "doc_accept_deal",
                  'documents[0][signed]': '1',
                  'documents[1][signed]': '1',
                  'documents[2][signed]': '1',
                  'documents[3][signed]': '1',
                  'documents[4][signed]': '1',
                  'documents[5][signed]': '1',
                  'documents[6][signed]': '1',
                  'documents[7][signed]': '1',
                  'documents[8][signed]': '1',
                  }
        files = {'documents[0][file]': file,
                 'documents[1][file]': file1,
                 'documents[2][file]': file2,
                 'documents[3][file]': file3,
                 'documents[4][file]': file4,
                 'documents[5][file]': file5,
                 'documents[6][file]': file6,
                 'documents[7][file]': file7,
                 'documents[8][file]': file8,
                 }

        r = requests.post(url, data=values,
                          headers={'Accept': 'application/json, text/plain, */*',
                                   'Token': self.token,
                                   'Authorization': self.basic_authorization}, files=files)
        file.close()
        file1.close()
        file2.close()
        file3.close()
        file4.close()
        file5.close()
        file6.close()
        file7.close()
        file8.close()
        try:
            self.assertEqual(r.status_code, 200)
        except AssertionError:
            print(r.text)
            raise

    def upload_package_otp_express(self, bid_id, filename):
        url = self.api_url + str(bid_id) + '/document/package/upload'

        file_dir = Base().get_file_dir('files', filename)
        file = open(file_dir, 'rb')
        file1 = open(file_dir, 'rb')
        file2 = open(file_dir, 'rb')

        values = {'certificate[expiration]': "2021-06-16",
                  'certificate[from]': "2021-03-16",
                  'certificate[issuer]': "CN=CRYPTO-PRO Test Center 2, O=CRYPTO-PRO LLC, L=Moscow, C=RU, E=support@cryptopro.ru",
                  'certificate[selectValue]': "qwe",
                  'certificate[serial]': "1200513B7743AFB99E76084EDD000100513B77",
                  'certificate[subject]': "CN=maria0",
                  'certificate[thumbprint]': "28333F412221A88AC766B5433541F7BF3A34C2DC",
                  'documents[0][file_name]': "doc_anketa",
                  'documents[1][file_name]': "doc_bug_year_report",
                  'documents[2][file_name]': "doc_individual_identity_document",  # Паспорт
                  'documents[0][signed]': '1',
                  'documents[1][signed]': '1',
                  'documents[2][signed]': '1'}
        files = {'documents[0][file]': file,
                 'documents[1][file]': file1,
                 'documents[2][file]': file2
                 }

        r = requests.post(url,
                          data=values,
                          headers={'Accept': 'application/json, text/plain, */*',
                                   'Token': self.token,
                                   'Authorization': self.basic_authorization}, files=files)
        file.close()
        file1.close()
        file2.close()
        try:
            self.assertEqual(r.status_code, 200)
        except AssertionError:
            print(r.text)
            raise

    def upload_package_usual(self, bid_id, filename):
        url = self.api_url + str(bid_id) + '/document/package/upload'

        file_dir = Base().get_file_dir('files', filename)
        file = open(file_dir, 'rb')
        file1 = open(file_dir, 'rb')
        file2 = open(file_dir, 'rb')
        file3 = open(file_dir, 'rb')
        file4 = open(file_dir, 'rb')
        file5 = open(file_dir, 'rb')
        file6 = open(file_dir, 'rb')
        file7 = open(file_dir, 'rb')
        file8 = open(file_dir, 'rb')

        values = {'certificate[expiration]': "2021-06-16",
                  'certificate[from]': "2021-03-16",
                  'certificate[issuer]': "CN=CRYPTO-PRO Test Center 2, O=CRYPTO-PRO LLC, L=Moscow, C=RU, E=support@cryptopro.ru",
                  'certificate[selectValue]': "qwe",
                  'certificate[serial]': "1200513B7743AFB99E76084EDD000100513B77",
                  'certificate[subject]': "CN=maria0",
                  'certificate[thumbprint]': "28333F412221A88AC766B5433541F7BF3A34C2DC",
                  'documents[0][file_name]': "doc_anketa",
                  'documents[1][file_name]': "doc_client_buh_report",
                  'documents[2][file_name]': "doc_client_locate_fact",
                  'documents[3][file_name]': "doc_bug_year_report",
                  'documents[4][file_name]': "doc_individual_identity_document",
                  'documents[5][file_name]': "doc_order_current_redaction",
                  'documents[6][file_name]': "doc_executor_nomination",
                  'documents[7][file_name]': "doc_order_for_executor_nomination",
                  'documents[8][file_name]': "doc_tax_return",
                  'documents[0][signed]': "1",
                  'documents[1][signed]': "1",
                  'documents[2][signed]': "1",
                  'documents[3][signed]': "1",
                  'documents[4][signed]': "1",
                  'documents[5][signed]': "1",
                  'documents[6][signed]': "1",
                  'documents[7][signed]': "1",
                  'documents[8][signed]': "1"}
        files = {'documents[0][file]': file,
                 'documents[1][file]': file1,
                 'documents[2][file]': file2,
                 'documents[3][file]': file3,
                 'documents[4][file]': file4,
                 'documents[5][file]': file5,
                 'documents[6][file]': file6,
                 'documents[7][file]': file7,
                 'documents[8][file]': file8}

        r = requests.post(url,
                          data=values,
                          headers={'Accept': 'application/json, text/plain, */*',
                                   'Token': self.token,
                                   'Authorization': self.basic_authorization}, files=files)
        file.close()
        file1.close()
        file2.close()
        file3.close()
        file4.close()
        file5.close()
        file6.close()
        file7.close()
        file8.close()
        try:
            self.assertEqual(r.status_code, 200)
        except AssertionError:
            print(r.text)
            raise

    def upload_unsigned_package_passport_anketa(self, bid_id, filename, ip=False):
        url = self.api_url + str(bid_id) + '/document/package/upload'

        file_dir = Base().get_file_dir('files', filename)
        file = open(file_dir, 'rb')
        file1 = open(file_dir, 'rb')

        if ip:
            passport_name = "doc_identity_document"
        else:
            passport_name = "doc_individual_identity_document"

        values = {
            'documents[0][file_name]': "doc_anketa",
            'documents[1][file_name]': passport_name,
            'documents[0][signed]': '0',
            'documents[1][signed]': '0'
        }
        files = {'documents[0][file]': file,
                 'documents[1][file]': file1}

        r = requests.post(url,
                          data=values,
                          headers={'Accept': 'application/json, text/plain, */*',
                                   'Token': self.token,
                                   'Authorization': self.basic_authorization}, files=files)

        file.close()
        file1.close()
        try:
            self.assertEqual(r.status_code, 200)
        except AssertionError:
            print(r.text)
            raise

    def upload_package_passport_anketa(self, bid_id, filename, ip=False):
        url = self.api_url + str(bid_id) + '/document/package/upload'

        file_dir = Base().get_file_dir('files', filename)
        file = open(file_dir, 'rb')
        file1 = open(file_dir, 'rb')

        if ip:
            passport_name = "doc_identity_document"
        else:
            passport_name = "doc_individual_identity_document"

        values = {'certificate[expiration]': "2021-06-16",
                  'certificate[from]': "2021-03-16",
                  'certificate[issuer]': "CN=CRYPTO-PRO Test Center 2, O=CRYPTO-PRO LLC, L=Moscow, C=RU, E=support@cryptopro.ru",
                  'certificate[selectValue]': "qwe",
                  'certificate[serial]': "1200513B7743AFB99E76084EDD000100513B77",
                  'certificate[subject]': "CN=maria0",
                  'certificate[thumbprint]': "28333F412221A88AC766B5433541F7BF3A34C2DC",
                  'documents[0][file_name]': "doc_anketa",
                  'documents[1][file_name]': passport_name,
                  'documents[0][signed]': '1',
                  'documents[1][signed]': '1'
                  }
        files = {'documents[0][file]': file,
                 'documents[1][file]': file1}

        r = requests.post(url,
                          data=values,
                          headers={'Accept': 'application/json, text/plain, */*',
                                   'Token': self.token,
                                   'Authorization': self.basic_authorization}, files=files)
        file.close()
        file1.close()
        try:
            self.assertEqual(r.status_code, 200)
        except AssertionError:
            print(r.text)
            raise

    def transfer_to_bank(self, bid_id):
        url = self.api_url + str(bid_id) + '/transfer-to-bank'
        r = requests.post(url,
                          headers={'Accept': 'application/json, text/plain, */*',
                                   'Token': self.token,
                                   'Authorization': self.basic_authorization})
        try:
            self.assertEqual(r.status_code, 200)
        except AssertionError:
            print(r.text)
            raise

    def accept_proposal(self, bid_id, filename):
        url = self.api_url + str(bid_id) + '/accept-proposal'
        base = Base()
        act_file = open(base.get_file_dir('files', filename), 'rb')
        contract_file = open(base.get_file_dir('files', filename), 'rb')
        notification_file = open(base.get_file_dir('files', filename), 'rb')
        project_file = open(base.get_file_dir('files', filename), 'rb')

        values = {'certificate[expiration]': "2021-06-16",
                  'certificate[from]': "2021-03-16",
                  'certificate[issuer]': "CN=CRYPTO-PRO Test Center 2, O=CRYPTO-PRO LLC, L=Moscow, C=RU, E=support@cryptopro.ru",
                  'certificate[selectValue]': "qwe",
                  'certificate[serial]': "1200513B7743AFB99E76084EDD000100513B77",
                  'certificate[subject]': "CN=maria0",
                  'certificate[thumbprint]': "28333F412221A88AC766B5433541F7BF3A34C2DC",
                  'files[0][file_name]': "doc_bg_act",
                  'files[1][file_name]': "doc_bg_contract",
                  'files[2][file_name]': "doc_bg_notification",
                  'files[3][file_name]': "doc_bg_project"
                  }
        files = {'files[0][file]': act_file,
                 'files[1][file]': contract_file,
                 'files[2][file]': notification_file,
                 'files[3][file]': project_file,
                 }

        r = requests.post(url,
                          data=values,
                          headers={'Accept': 'application/json, text/plain, */*',
                                   'Token': self.token,
                                   'Authorization': self.basic_authorization}, files=files)

        act_file.close()
        contract_file.close()
        notification_file.close()
        project_file.close()
        try:
            self.assertEqual(r.status_code, 200)
        except AssertionError:
            print(r.text)
            raise

    def accept_proposal_otp(self, bid_id, filename):
        url = self.api_url + str(bid_id) + '/accept-proposal'
        base = Base()
        contract_file = open(base.get_file_dir('files', filename), 'rb')
        notification_file = open(base.get_file_dir('files', filename), 'rb')
        project_file = open(base.get_file_dir('files', filename), 'rb')

        values = {'certificate[expiration]': "2021-06-16",
                  'certificate[from]': "2021-03-16",
                  'certificate[issuer]': "CN=CRYPTO-PRO Test Center 2, O=CRYPTO-PRO LLC, L=Moscow, C=RU, E=support@cryptopro.ru",
                  'certificate[selectValue]': "qwe",
                  'certificate[serial]': "1200513B7743AFB99E76084EDD000100513B77",
                  'certificate[subject]': "CN=maria0",
                  'certificate[thumbprint]': "28333F412221A88AC766B5433541F7BF3A34C2DC",
                  'files[0][file_name]': "doc_bg_contract",
                  'files[1][file_name]': "doc_bg_notification",
                  'files[2][file_name]': "doc_bg_project"
                  }
        files = {
                 'files[0][file]': contract_file,
                 'files[1][file]': notification_file,
                 'files[2][file]': project_file,
                 }

        r = requests.post(url,
                          data=values,
                          headers={'Accept': 'application/json, text/plain, */*',
                                   'Token': self.token,
                                   'Authorization': self.basic_authorization}, files=files)

        contract_file.close()
        notification_file.close()
        project_file.close()
        try:
            self.assertEqual(r.status_code, 200)
        except AssertionError:
            print(r.text)
            raise

    def create_new_bid(self, bid: Bid, client: Client, customer: Customer):
        url = self.api_url + 'new'

        if bid.type == BidType.execution:
            contract_type = '0'
            bg_type = '0'

        payload = {'contract_type': contract_type,
                   'bg_type': bg_type,
                   'entity[inn]': client.inn,
                   'customer[inn]': customer.inn,
                   'purchase': bid.number,
                   'date_output': (datetime.date.today()).
                       strftime("%Y-%m-%d"),
                   'date_finish': (datetime.date.today() + datetime.timedelta(bid.days_count - 1)).
                       strftime("%Y-%m-%d"),
                   'final_price': float(bid.final_price.replace(' ', '')),
                   'required_sum': float(bid.guarantee_price.replace(' ', '')),
                   'bg_form_beneficiary': '0',
                   'avans': '0',
                   'bg_cancellation': '0',
                   'bidding_law': bid.law,
                   'provider_ident_type': 'Электронный аукцион',
                   'date_publish': '2021-06-25'}

        r = requests.post(url,
                          data=payload,
                          headers={'Accept': 'application/json, text/plain, */*',
                                   'Token': self.token,
                                   'Authorization': self.basic_authorization})
        try:
            self.assertEqual(r.status_code, 200)
        except AssertionError:
            print(r.text)
            raise
        bid.id = json.loads(r.text)["data"]["prescore"]["bid_id"]

    def put_data_into_bid_by_id(self, bid: Bid, client: Client, customer: Customer, bank_account: BankAccount,
                                beneficiary: Beneficiary):

        url = self.api_url + f'{bid.id}'

        payload = json.dumps({
            "bg_type": "0",
            "bidding_law": bid.law,
            "date_output": (datetime.date.today()).
                strftime("%Y-%m-%d"),
            "date_finish": (datetime.date.today() + datetime.timedelta(bid.days_count - 1)).
                strftime("%Y-%m-%d"),
            "start_price": float(bid.start_price.replace(" ", '')),
            "avans": False,
            "bg_cancellation": False,
            "date_publish": datetime.datetime.strptime(bid.publish_date, '%d.%m.%Y').strftime("%Y-%m-%d"),
            "another_person_benefit": False,
            "entity": {
                "kpp": client.kpp,
                "short_name": client.short_name,
                "full_name": client.fullname,
                "address": client.address,
                "real_address": client.address,
                "post_address": client.address,
                "okopf": client.okoph,
                "oktmo": client.oktmo,
                "okved": client.okved,
                "bank_account_number": bank_account.bank_account_number,
                "bank_bik": bank_account.bank_bik,
                "bank_name": bank_account.bank_name,
                "contact_fio": bank_account.contact_fio,
                "contact_email": bank_account.contact_email,
                "contact_phone": bank_account.contact_phone_number,
                "strategy_fz_213": False,
                "dept_budget_rf": False,
                "catroteka_not_pay": False,
                "long_debt_workers": False,
                "debt_debit": False,
                "process_liquid": False,
                "license_activity": False,
                "gos_tenders": True,
                "usa_org_reg": False,
                "usa_org_resident": False,
                "usa_org_boss_fiz": False,
                "usa_org_boss_ur": False,
                "management_approval": False,
                "empty_zalog": False,
                "empty_credit": False,
                "is_patent_used": False
            },
            "customer": {
                "kpp": customer.kpp,
                "full_name": customer.full_orgname,
                "ogrn": customer.ogrn,
                "address": customer.address,
                "oktmo": customer.oktmo,
                "rf_subject": "77",
                "date_nalog_reg": datetime.datetime.strptime(customer.tax_date_registration, '%d.%m.%Y').
                strftime("%Y-%m-%d"),
                "contract_region": customer.rf_subject,
                "object": bid.subject
            },
            "individual": {
                "inn": beneficiary.inn,
                "fio": beneficiary.fio,
                "position": "Генеральный директор",
                "gender": beneficiary.gender,
                "birth_date": datetime.datetime.strptime(beneficiary.birth_date, '%d.%m.%Y').strftime("%Y-%m-%d"),
                "birth_place": beneficiary.birth_place,
                "doc_type": "Паспорт РФ",
                "doc_series": beneficiary.passport_series,
                "doc_number": beneficiary.passport_number,
                "doc_date": datetime.datetime.strptime(beneficiary.passport_date_out, '%d.%m.%Y').strftime("%Y-%m-%d"),
                "doc_output_depart_code": beneficiary.passport_code,
                "doc_output": beneficiary.passport_who_give,
                "address": beneficiary.registration_address,
                "real_address": beneficiary.fact_address,
                "founder": True,
                "personal": True
            },
            "beneficiaries": [
                {
                    "full_name": beneficiary.fio,
                    "gender": beneficiary.gender,
                    "bis_part": 100,
                    "birth_date": datetime.datetime.strptime(beneficiary.birth_date, '%d.%m.%Y').strftime("%Y-%m-%d"),
                    "birth_place": beneficiary.birth_place,
                    "inn": beneficiary.inn,
                    "doc_type": "Паспорт РФ",
                    "doc_series": beneficiary.passport_series,
                    "doc_number": beneficiary.passport_number,
                    "doc_date": datetime.datetime.strptime(beneficiary.passport_date_out, '%d.%m.%Y').strftime(
                        "%Y-%m-%d"),
                    "doc_output_depart_code": beneficiary.passport_code,
                    "doc_output": beneficiary.passport_who_give,
                    "address": beneficiary.registration_address,
                    "real_address": beneficiary.fact_address,
                    "contacts": beneficiary.contact_information,
                    "owns_more25": True,
                    "can_control": True,
                    "can_decide": True,
                    "can_influence_profit": True,
                    "can_influence_decisions": True,
                    "is_single": False,
                    "is_public_executive": False
                }
            ],
            "shareholders": [
                {
                    "full_name": beneficiary.fio,
                    "inn": beneficiary.inn,
                    "share": 100
                }
            ]
        })

        headers = {
            'Token': 'Bearer f87ce2fb-6830-4b01-a309-da38abc74a14',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': 'Basic YXRmbl9kZXY6SXplWno1NExLbw==',
            'Content-Type': 'application/json'
        }

        r = requests.request("PUT", url, headers=headers, data=payload)
        try:
            self.assertEqual(r.status_code, 200)
        except AssertionError:
            print(r.text)
            raise
