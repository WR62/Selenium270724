import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import logging


class BasePage:
    def __init__(self, browser, url_address):
        self.browser = browser
        self.url = url_address
        self.logger = browser.logger
        self.class_name = type(self).__name__

    def find_elem_located(self, locator, timeout=3):
        self.logger.debug('%s - finding element %s' % (self.class_name, locator))

        try:
            elem = WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located(locator),
                                                              message=f"Can't find element by locator {locator}")
        except TimeoutException as texc:
            allure.attach(self.browser.get_screenshot_as_png(), name=f'{self.__class__}',
                          attachment_type=AttachmentType.JPG)
            raise Exception(texc)

        return elem

    def find_elem_clickable(self, locator, timeout=3):
        self.logger.debug('%s - finding clickable element %s' % (self.class_name, locator))

        try:
            elem = WebDriverWait(self.browser, timeout).until(EC.element_to_be_clickable(locator),
                                                              message=f"Can't find element by locator {locator}")
        except TimeoutException as texc:
            allure.attach(self.browser.get_screenshot_as_png(), name=f'{self.__class__}',
                          attachment_type=AttachmentType.JPG)
            raise Exception(texc)

        return elem

    def go_to_site(self, additional_url):
        self.logger.info('%s; open url %s' % (self.class_name, additional_url))
        return self.browser.get(self.url + additional_url)

    def input_value(self, locator, text: str):
        self.logger.debug('%s; input value %s in element %s' % (self.class_name, text, locator))
        self.find_elem_clickable(locator).click()
        self.find_elem_clickable(locator).clear()
        for ch in text:
            self.find_elem_located(locator).send_keys(ch)

    def get_element_attribute(self, add_url, locator, attrib) -> str:
        # Возвращает текстовое значение атрибута на произвольной стрaнице
        self.logger.debug('%s; url %s; return text value of attribute %s in element %s' % (self.class_name, attrib,
                                                                                           locator, add_url))
        self.go_to_site(add_url)
        elem = self.find_elem_located(locator)
        return elem.get_attribute(attrib)

    def go_to_page(self, url):
        with allure.step(f'Moving to page {url}'):
            return self.browser.get(url)
