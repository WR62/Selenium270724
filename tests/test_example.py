import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.keys import Keys


def test_hello_google(browser, url_address):
    browser.get(url_address + ':8081')
    assert "Store" in browser.title


def test_main_page(browser, url_address):
    browser.get(url_address + ':8081')
    browser.find_element(By.ID, "common-home")
    browser.find_element(By.ID, "carousel-banner-0")
    browser.find_element(By.CLASS_NAME, "carousel-indicators")
    browser.find_element(By.ID, "top")
    browser.find_element(By.ID, "menu")


def test_catalog(browser, url_address):
    browser.get(url_address + ':8081/en-gb/catalog/laptop-notebook')
    browser.find_element(By.CLASS_NAME, "breadcrumb-item")
    browser.find_element(By.CLASS_NAME, "list-group")
    browser.find_element(By.ID, "carousel-banner-0")
    browser.find_element(By.ID, "display-control")
    browser.find_element(By.CLASS_NAME, "text-end")


def test_product_card(browser, url_address):
    browser.get(url_address + ':8081/en-gb/product/apple-cinema')
    browser.find_element(By.CLASS_NAME, "img-thumbnail")
    browser.find_element(By.CLASS_NAME, "btn-light")
    browser.find_element(By.XPATH, "//*[contains(text(),'Available Options')]")
    browser.find_element(By.ID, "input-product-id")
    wait = WebDriverWait(browser, 3)
    wait.until(EC.element_to_be_clickable((By.ID, "button-upload-222")))


def test_login(browser, url_address):
    browser.get(url_address + ':8081/administration')
    browser.find_element(By.CLASS_NAME, "card-header")
    wait = WebDriverWait(browser, 2)
    wait.until(EC.presence_of_element_located((By.ID, "input-username")))
    wait.until(EC.presence_of_element_located((By.ID, "input-password")))
    browser.find_element(By.CLASS_NAME, "btn-primary")
    browser.find_element(By.CLASS_NAME, "input-group-text")


def test_register(browser, url_address):
    browser.get(url_address + ':8081/index.php?route=account/register')
    browser.find_element(By.ID, "column-right")
    browser.find_element(By.ID, "account")
    browser.find_element(By.CLASS_NAME, "col-sm-10")
    browser.find_element(By.ID, "input-newsletter")
    wait = WebDriverWait(browser, 2)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Continue']")))


def test_login_logout(browser, url_address):
    browser.get(url_address + ':8081/administration')
    wait = WebDriverWait(browser, 2)
    input_username = wait.until(EC.element_to_be_clickable((By.NAME, 'username')))
    input_username.click()
    input_username.send_keys('user')
    input_password = browser.find_element(By.NAME, 'password')
    input_password.click()
    input_password.send_keys('bitnami')
    btn_login = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-primary')))
    btn_login.click()
    wait = WebDriverWait(browser, 4)
    btn_logout = wait.until(EC.element_to_be_clickable((By.ID, 'nav-logout')))
    btn_logout.click()
    btn_login = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-primary')))


def test_cart(browser, url_address):
    browser.get(url_address + ':8081')
    wait = WebDriverWait(browser, 4)
    # Находим на странице товар Canon EOS и переходим на страницу добавления товара в корзину
    btn_cart = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Canon "
                                                                "EOS')]/../../following-sibling::form//div//button")))
    btn_cart.send_keys(Keys.ENTER)
    # Выбираем цвет товара
    select_elem = Select(wait.until(EC.element_to_be_clickable((By.ID, "input-option-226"))))
    select_elem.select_by_value('15')
    # Добавляем товар в корзину
    btn_cart = browser.find_element(By.ID, 'button-cart')
    btn_cart.send_keys(Keys.ENTER)
    time.sleep(2)
    # Переходим в корзину. Проверяем, что выбранный товар есть в корзине
    browser.get(url_address + ':8081/en-gb?route=checkout/cart')
    assert browser.find_element(By.XPATH, "//*[contains(text(),'Canon EOS')]") is not None


def change_currency(browser, url_address_base, url_address_add):
    browser.get(url_address_base + url_address_add)
    # Проверяем наличие символа $ в цене первого товара на странице
    orig_text = browser.find_element(By.CLASS_NAME, "price-new").get_attribute('innerText')
    assert '$' in orig_text
    time.sleep(2)
    # Изменяем валюту отображения через Javascript (не сумел этого добиться через Selenium)
    browser.execute_script('document.querySelector("body > nav:nth-child(2) > div:nth-child(1) > div:nth-child(1) > '
                           'ul:nth-child(1) > li:nth-child(1) > form:nth-child(1) > div:nth-child(1) > ul:nth-child('
                           '2) > li:nth-child(1) > a:nth-child(1)").click()')
    time.sleep(2)
    # Проверяем наличие символа € в цене первого товара на странице
    orig_text = browser.find_element(By.CLASS_NAME, "price-new").get_attribute('innerText')
    assert '€' in orig_text


def test_change_currency_main(browser, url_address):
    change_currency(browser, url_address, ':8081')


def test_change_currency_catalog(browser, url_address):
    change_currency(browser, url_address, ':8081/en-gb/catalog/desktops/mac')
