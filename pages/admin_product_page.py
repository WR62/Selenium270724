import time
import random

from selenium.webdriver import Keys

from pages.basepage import BasePage
from selenium.webdriver.common.by import By

from pages.login_logout_page import LoginLogoutPage


class AdminProductPage(BasePage):
    input_ = {'product_name': 'Abracadabra', 'meta_tag_title': 'ABR', 'model': 'Abr-2024', 'price': 13.13,
              'keyword': 'SEO5'}

    ADD_URL_PRODUCTS = ':8081/administration/index.php?route=catalog/product&user_token='
    ADD_URL_NEW_PRODUCT = ':8081/administration/index.php?route=catalog/product.form&user_token='

    LOCATOR_FOR_SAVE = (By.XPATH, "//*[contains(@title, 'Save')]")

    LOCATOR_PRODUCT_NAME = (By.ID, 'input-name-1')
    LOCATOR_META_TAG = (By.ID, 'input-meta-title-1')
    LOCATOR_PRODUCT_MODEL = (By.ID, 'input-model')
    LOCATOR_PRODUCT_PRICE = (By.ID, 'input-price')
    LOCATOR_PRODUCT_SEO = (By.ID, 'input-keyword-0-1')

    LOCATOR_SEARCH_PAGES = (By.XPATH, "//div[@class='col-sm-6 text-end']")
    LOCATOR_FILTER_PRODUCT = (By.ID, 'input-name')
    LOCATOR_FILTER_BUTTON = (By.ID, 'button-filter')

    LOCATOR_CHECKBOX = (By.CLASS_NAME, 'form-check-input')
    LOCATOR_BUTTON_DELETE = (By.XPATH, "//button[@class='btn btn-danger']")

    SELECTOR_JAVASCRIPT_DATA = ".nav-link[href='#tab-data']"
    SELECTOR_JAVASCRIPT_SEO = ".nav-link[href='#tab-seo']"

    def get_token(self) -> str:
        current_url = self.browser.current_url
        token = current_url[current_url.find('token=') + 6:]
        return token

    def get_href_attribute(self, locator_for_xpath) -> str:
        elem = self.find_elem_clickable(locator_for_xpath)
        attr = elem.get_attribute('href')
        return attr

    def get_javascript_query(self, selector):
        return 'document.querySelector(\"' + selector + '\").click()'

    def input_new_product(self):
        # Переход на страницу добавления нового продукта
        self.go_to_site(additional_url=self.ADD_URL_NEW_PRODUCT + self.get_token())
        # Ввод данных на вкладке General
        self.input_value(locator=self.LOCATOR_PRODUCT_NAME, text=self.input_['product_name'])
        self.find_elem_clickable(self.LOCATOR_META_TAG).send_keys(self.input_['meta_tag_title'])
        self.browser.execute_script(self.get_javascript_query(self.SELECTOR_JAVASCRIPT_DATA))
        # Ввод данных на вкладке Data
        self.input_value(locator=self.LOCATOR_PRODUCT_MODEL, text=self.input_['model'])
        self.find_elem_located(self.LOCATOR_PRODUCT_PRICE).send_keys(self.input_['price'])
        # Ввод данных на вкладке SEO
        self.browser.execute_script(self.get_javascript_query(self.SELECTOR_JAVASCRIPT_SEO))
        self.input_value(locator=self.LOCATOR_PRODUCT_SEO, text=self.input_['keyword'])

        self.find_elem_located(self.LOCATOR_FOR_SAVE).send_keys(Keys.ENTER)

    def search_for_product(self, name_of_product) -> bool:
        self.go_to_site(additional_url=self.ADD_URL_PRODUCTS + self.get_token())
        self.browser.refresh()
        self.input_value(locator=self.LOCATOR_FILTER_PRODUCT, text=name_of_product)
        self.find_elem_clickable(self.LOCATOR_FILTER_BUTTON).click()
        time.sleep(1)
        # Находим количество страниц отображения продуктов (если равно нулю - продукт не найден)
        text_pages = self.find_elem_located(self.LOCATOR_SEARCH_PAGES).text
        number_of_pages = text_pages[text_pages.find('(') + 1:]
        number_of_pages = int(number_of_pages[:number_of_pages.find(' ')])
        if number_of_pages > 0:
            return True
        else:
            return False

    def enter_to_admin_page(self):
        login_logout_page = LoginLogoutPage(self.browser, self.url)
        login_logout_page.go_to_site()
        login_logout_page.input_value(login_logout_page.LOCATOR_USERNAME, login_logout_page.LOGIN_USER)
        login_logout_page.input_value(login_logout_page.LOCATOR_PASSWORD, login_logout_page.LOGIN_PASSWORD)
        login_logout_page.find_elem_clickable(login_logout_page.LOCATOR_BUTTON_LOGIN).click()

        login_logout_page.find_elem_clickable(login_logout_page.LOCATOR_ADMIN_PRODUCTS).click()
