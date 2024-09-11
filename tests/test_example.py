import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.keys import Keys

from pages.admin_product_page import AdminProductPage
from pages.basepage import BasePage
from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.login_logout_page import LoginLogoutPage
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.product_card_page import ProductCardPage
from pages.register_page import RegisterPage


@pytest.mark.parametrize("locat", [MainPage.LOCATOR_MAIN_CONT, MainPage.LOCATOR_CAROUSEL_BANNER,
                                   MainPage.LOCATOR_CAROUSEL_INDICATORS, MainPage.LOCATOR_TOP, MainPage.LOCATOR_MENU])
def test_main_page(browser, url_address, locat):
    m_p = MainPage(browser, url_address)
    m_p.go_to_site(':8081')
    assert "Store" in browser.title
    assert m_p.find_elem_located(locat) is not None


@pytest.mark.parametrize("locat", [CatalogPage.LOCATOR_BREADCRUMB, CatalogPage.LOCATOR_LIST_GROUP,
                                   CatalogPage.LOCATOR_CAROUSEL_BANNER_0, CatalogPage.LOCATOR_DISPLAY_CONTROL,
                                   CatalogPage.LOCATOR_TEXT_END])
def test_catalog(browser, url_address, locat):
    catl_page = CatalogPage(browser, url_address)
    catl_page.go_to_site(':8081/en-gb/catalog/laptop-notebook')
    assert catl_page.find_elem_located(locat) is not None


@pytest.mark.parametrize("locat", [ProductCardPage.LOCATOR_IMG_THUMBNAIL, ProductCardPage.LOCATOR_BTN_LIGHT,
                                   ProductCardPage.LOCATOR_OPTIONS, ProductCardPage.LOCATOR_INPUT_PRODUCT])
def test_product_card(browser, url_address, locat):
    prod_card_page = ProductCardPage(browser, url_address)
    prod_card_page.go_to_site()
    assert prod_card_page.find_elem_located(locat) is not None
    assert prod_card_page.find_elem_clickable(prod_card_page.LOCATOR_BUTTON_UPLOAD) is not None


@pytest.mark.parametrize("locat", [LoginPage.LOCATOR_CARD_HEADER, LoginPage.LOCATOR_USERNAME,
                                   LoginPage.LOCATOR_PASSWORD, LoginPage.LOCATOR_INPUT_GROUP])
def test_login(browser, url_address, locat):
    login_page = LoginPage(browser, url_address)
    login_page.go_to_site()
    assert login_page.find_elem_located(locat) is not None
    assert login_page.find_elem_clickable(login_page.LOCATOR_BUTTON_PRIMARY) is not None


@pytest.mark.parametrize("locat", [RegisterPage.LOCATOR_COLUMN_RIGHT, RegisterPage.LOCATOR_ACCOUNT,
                                   RegisterPage.LOCATOR_COLUMN_FIRST_NAME, RegisterPage.LOCATOR_INPUT_NEWSLETTER])
def test_register(browser, url_address, locat):
    regist_page = RegisterPage(browser, url_address)
    regist_page.go_to_site()
    assert regist_page.find_elem_located(locat) is not None
    assert regist_page.find_elem_clickable(regist_page.LOCATOR_CONTINUE) is not None


def test_login_logout(browser, url_address):
    login_logout_page = LoginLogoutPage(browser, url_address)
    login_logout_page.go_to_site()
    login_logout_page.input_value(login_logout_page.LOCATOR_USERNAME, login_logout_page.LOGIN_USER)
    login_logout_page.input_value(login_logout_page.LOCATOR_PASSWORD, login_logout_page.LOGIN_PASSWORD)
    login_logout_page.find_elem_clickable(login_logout_page.LOCATOR_BUTTON_LOGIN).click()
    login_logout_page.find_elem_clickable(login_logout_page.LOCATOR_BUTTON_LOGOUT).click()
    assert login_logout_page.find_elem_clickable(login_logout_page.LOCATOR_BUTTON_LOGIN) is not None


def test_cart(browser, url_address):
    cart_page = CartPage(browser, url_address)
    cart_page.go_to_site(cart_page.BASE_PAGE_URL)
    # Находим на странице товар Canon EOS и переходим на страницу добавления товара в корзину
    btn_cart = cart_page.find_elem_clickable(cart_page.LOCATOR_BUTTON_PRODUCT)
    btn_cart.send_keys(Keys.ENTER)
    # Выбираем цвет товара
    cart_page.choose_product_color()
    # Добавляем товар в корзину
    cart_page.find_elem_clickable(cart_page.LOCATOR_BUTTON_ADD_PRODUCT).send_keys(Keys.ENTER)
    time.sleep(2)
    # Переходим в корзину. Проверяем, что выбранный товар есть в корзине
    cart_page.go_to_site(cart_page.CART_PAGE_URL)
    assert cart_page.find_elem_located(cart_page.LOCATOR_PRODUCT_NAME) is not None


def change_currency(browser, url_address, url_address_add):
    base_page = BasePage(browser, url_address)
    orig_text = base_page.get_element_attribute(add_url=url_address_add, locator=(By.CLASS_NAME, "price-new"),
                                                attrib='innerText')
    # Проверяем наличие символа $ в цене первого товара на странице
    assert '$' in orig_text
    time.sleep(2)
    # Изменяем валюту отображения через Javascript
    browser.execute_script('document.querySelector("body > nav:nth-child(2) > div:nth-child(1) > div:nth-child(1) > '
                           'ul:nth-child(1) > li:nth-child(1) > form:nth-child(1) > div:nth-child(1) > ul:nth-child('
                           '2) > li:nth-child(1) > a:nth-child(1)").click()')
    time.sleep(2)
    # Проверяем наличие символа € в цене первого товара на странице
    orig_text = base_page.get_element_attribute(add_url=url_address_add, locator=(By.CLASS_NAME, "price-new"),
                                                attrib='innerText')
    assert '€' in orig_text
    # Возвращаем валюту отображения в $ через Javascript
    browser.execute_script('document.querySelector("body > nav:nth-child(2) > div:nth-child(1) > div:nth-child(1) > '
                           'ul:nth-child(1) > li:nth-child(1) > form:nth-child(1) > div:nth-child(1) > ul:nth-child('
                           '2) > li:nth-child(3) > a:nth-child(1)").click()')



def test_change_currency_main(browser, url_address):
    # Проверка смены валюты на главной странице
    change_currency(browser, url_address, ':8081')


def test_change_currency_catalog(browser, url_address):
    # Проверка смены валюты на странице произыольного товара из каталога
    change_currency(browser, url_address, ':8081/en-gb/catalog/desktops/mac')


def test_add_product(browser, url_address):
    # noinspection DuplicatedCode
    login_logout_page = LoginLogoutPage(browser, url_address)
    login_logout_page.go_to_site()
    # Вход в админку
    login_logout_page.input_value(login_logout_page.LOCATOR_USERNAME, login_logout_page.LOGIN_USER)
    login_logout_page.input_value(login_logout_page.LOCATOR_PASSWORD, login_logout_page.LOGIN_PASSWORD)
    login_logout_page.find_elem_clickable(login_logout_page.LOCATOR_BUTTON_LOGIN).click()

    login_logout_page.find_elem_clickable(login_logout_page.LOCATOR_ADMIN_PRODUCTS).click()
    admin_prod_page = AdminProductPage(browser, url_address)
    # Переход на страницу списка продуктов
    admin_prod_page.go_to_site(additional_url=admin_prod_page.ADD_URL_PRODUCTS + admin_prod_page.get_token())
    admin_prod_page.input_new_product()

    assert admin_prod_page.search_for_product(admin_prod_page.input_['product_name']) is True


def test_delete_product(browser, url_address):
    admin_prod_page = AdminProductPage(browser, url_address)
    admin_prod_page.enter_to_admin_page()
    # Переход на страницу списка продуктов
    admin_prod_page.go_to_site(additional_url=admin_prod_page.ADD_URL_PRODUCTS + admin_prod_page.get_token())
    assert admin_prod_page.search_for_product(admin_prod_page.input_['product_name']) is True, "No such product!"
    admin_prod_page.find_elem_located(admin_prod_page.LOCATOR_CHECKBOX).click()
    admin_prod_page.find_elem_clickable(admin_prod_page.LOCATOR_BUTTON_DELETE).click()
    browser.switch_to.alert.accept()
    assert admin_prod_page.search_for_product(admin_prod_page.input_['product_name']) is False, "Such product exists!"


def test_register_user(browser, url_address):
    reg_page = RegisterPage(browser, url_address)
    reg_page.go_to_site()
    assert reg_page.register_user() is True
