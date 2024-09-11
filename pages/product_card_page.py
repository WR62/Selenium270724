from pages.basepage import BasePage
from selenium.webdriver.common.by import By


class ProductCardPage(BasePage):
    PRODUCT_CARD_URL = ':8081/en-gb/product/apple-cinema'

    LOCATOR_IMG_THUMBNAIL = (By.CLASS_NAME, "img-thumbnail")
    LOCATOR_BTN_LIGHT = (By.CLASS_NAME, "btn-light")
    LOCATOR_OPTIONS = (By.XPATH, "//*[contains(text(),'Available Options')]")
    LOCATOR_INPUT_PRODUCT = (By.ID, "input-product-id")
    LOCATOR_BUTTON_UPLOAD = (By.ID, "button-upload-222")

    def go_to_site(self):
        BasePage.go_to_site(self, additional_url=self.PRODUCT_CARD_URL)
