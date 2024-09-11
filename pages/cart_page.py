from pages.basepage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class CartPage(BasePage):
    BASE_PAGE_URL = ':8081'
    CART_PAGE_URL = ':8081/en-gb?route=checkout/cart'

    LOCATOR_BUTTON_PRODUCT = (By.XPATH, "//*[contains(text(),'Canon "
                                        "EOS')]/../../following-sibling::form//div//button")
    LOCATOR_PRODUCT_COLOR = (By.ID, "input-option-226")
    LOCATOR_BUTTON_ADD_PRODUCT = (By.ID, 'button-cart')
    LOCATOR_PRODUCT_NAME = (By.XPATH, "//*[contains(text(),'Canon EOS')]")

    def choose_product_color(self, value='15'):
        select_elem = Select(self.find_elem_clickable(self.LOCATOR_PRODUCT_COLOR))
        return select_elem.select_by_value(value)
