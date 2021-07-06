import requests
import unittest
import json

from Pages.BasePage import Base


class AgentApi(unittest.TestCase, Base):
    with open("../config_connections.json") as json_data_file:
        stand = json.load(json_data_file)['stand']
    api_url = 'https://' + stand + '/api/v1/bids/'
    with open("../config_connections.json") as json_data_file:
        basic_authorization = json.load(json_data_file)['authorization']
    with open("../config_connections.json") as json_data_file:
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
        try:
            self.assertEqual(r.status_code, 200)
        except AssertionError:
            print(r.text)
            raise
