from pages.basepage import BasePage
from selenium.webdriver.common.by import By


class CatalogPage(BasePage):
    LOCATOR_BREADCRUMB = (By.CLASS_NAME, "breadcrumb-item")
    LOCATOR_LIST_GROUP = (By.CLASS_NAME, "list-group")
    LOCATOR_CAROUSEL_BANNER_0 = (By.ID, "carousel-banner-0")
    LOCATOR_DISPLAY_CONTROL = (By.ID, "display-control")
    LOCATOR_TEXT_END = (By.CLASS_NAME, "text-end")
