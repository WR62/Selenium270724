import time

from pages.basepage import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from faker import Faker


class RegisterPage(BasePage):
    REGISTER_PAGE_URL = ':8081/index.php?route=account/register'

    LOCATOR_COLUMN_RIGHT = (By.ID, "column-right")
    LOCATOR_ACCOUNT = (By.ID, "account")
    LOCATOR_COLUMN_FIRST_NAME = (By.CLASS_NAME, "col-sm-10")
    LOCATOR_INPUT_NEWSLETTER = (By.ID, "input-newsletter")
    LOCATOR_CONTINUE = (By.XPATH, "//*[text()='Continue']")
    LOCATOR_FIRST_NAME = (By.ID, "input-firstname")
    LOCATOR_LAST_NAME = (By.ID, "input-lastname")
    LOCATOR_EMAIL = (By.ID, "input-email")
    LOCATOR_PASSWORD = (By.ID, "input-password")
    LOCATOR_CHECK_AGREE = (By.XPATH, "//input[@name='agree']")
    LOCATOR_CREATED = (By.XPATH,"//h1[contains(text(),'Account Has Been Created')]")

    def go_to_site(self):
        BasePage.go_to_site(self, additional_url=self.REGISTER_PAGE_URL)

    def register_user(self) -> bool:
        faker = Faker('en-GB')
        self.input_value(self.LOCATOR_FIRST_NAME, faker.first_name())
        self.input_value(self.LOCATOR_LAST_NAME, faker.last_name())
        self.input_value(self.LOCATOR_EMAIL, faker.email())
        self.input_value(self.LOCATOR_PASSWORD, faker.password(length=8))
        # time.sleep(2)
        self.find_elem_clickable(self.LOCATOR_CHECK_AGREE, timeout=5).click()
        # time.sleep(2)
        self.find_elem_clickable(self.LOCATOR_CONTINUE, timeout=6).click()
        try:
            self.find_elem_located(self.LOCATOR_CREATED)
        except TimeoutException:
            return False
        else:
            return True
