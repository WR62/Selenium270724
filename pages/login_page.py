from pages.basepage import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):
    LOGIN_PAGE_URL = ':8081/administration'

    LOCATOR_CARD_HEADER = (By.CLASS_NAME, "card-header")
    LOCATOR_USERNAME = (By.ID, "input-username")
    LOCATOR_PASSWORD = (By.ID, "input-password")
    LOCATOR_BUTTON_PRIMARY = (By.CLASS_NAME, "btn-primary")
    LOCATOR_INPUT_GROUP = (By.CLASS_NAME, "input-group-text")

    def go_to_site(self):
        BasePage.go_to_site(self, additional_url=self.LOGIN_PAGE_URL)
