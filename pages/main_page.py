from pages.basepage import BasePage
from selenium.webdriver.common.by import By


class MainPage(BasePage):
    LOCATOR_MAIN_CONT = (By.ID, "common-home")
    LOCATOR_CAROUSEL_BANNER = (By.ID, "carousel-banner-0")
    LOCATOR_CAROUSEL_INDICATORS = (By.CLASS_NAME, "carousel-indicators")
    LOCATOR_TOP = (By.ID, "top")
    LOCATOR_MENU = (By.ID, "menu")
