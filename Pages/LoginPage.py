import keyboard

from Pages.BasePage import BasePage
import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep


class LoginPage(BasePage):
    login = '[placeholder="Логин"]'
    password = '[placeholder="Пароль"]'
    enter = '//button[text()[contains(.,"войти")]]'

    with open("../config_connections.json") as json_data_file:
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
        self.find_element_by_locator(self.enter)

    def login_as_agent(self):
        self.log_in(self.connections_data['agent'])

    def login_as_bank(self):
        self.log_in(self.connections_data['bank'])

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