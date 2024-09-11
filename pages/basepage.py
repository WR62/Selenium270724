from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, browser, url_address):
        self.browser = browser
        self.url = url_address

    def find_elem_located(self, locator, timeout=3):
        return WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located(locator),
                                                          message=f"Can't find element by locator {locator}")

    def find_elem_clickable(self, locator, timeout=3):
        return WebDriverWait(self.browser, timeout).until(EC.element_to_be_clickable(locator),
                                                          message=f"Can't find element by locator {locator}")

    def go_to_site(self, additional_url):
        return self.browser.get(self.url + additional_url)

    def input_value(self, locator, text: str):
        self.find_elem_clickable(locator).click()
        self.find_elem_clickable(locator).clear()
        for ch in text:
            self.find_elem_located(locator).send_keys(ch)

    def get_element_attribute(self, add_url, locator, attrib) -> str:
        # Возвращает текстовое значение атрибута на произвольной стрaнице
        self.go_to_site(add_url)
        elem = self.find_elem_located(locator)
        return elem.get_attribute(attrib)

    def go_to_page(self, url):
        return self.browser.get(url)
