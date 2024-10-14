import allure

from pages.basepage import BasePage
from selenium.webdriver.common.by import By


class LoginLogoutPage(BasePage):
    LOGIN_LOGOUT_PAGE_URL = ':8081/administration'

    LOGIN_USER = 'user'
    LOGIN_PASSWORD = 'bitnami'

    LOCATOR_USERNAME = (By.NAME, 'username')
    LOCATOR_PASSWORD = (By.NAME, 'password')
    LOCATOR_BUTTON_LOGIN = (By.CLASS_NAME,'btn-primary')

    LOCATOR_ADMIN_PRODUCTS = (By.ID, 'menu-catalog')

    LOCATOR_BUTTON_LOGOUT = (By.ID, 'nav-logout')

    def go_to_site(self):
        with allure.step(f'Move to page {self.LOGIN_LOGOUT_PAGE_URL}'):
            BasePage.go_to_site(self, additional_url=self.LOGIN_LOGOUT_PAGE_URL)
