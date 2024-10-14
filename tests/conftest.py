import pytest

import logging
import allure
import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions


def pytest_addoption(parser):
    parser.addoption("--browser", default="ch", choices=["eg", "ch", "ff"])
    parser.addoption("--url", default="http://192.168.100.32")   #http://192.168.43.15
    parser.addoption("--log_level", action="store", default="INFO")


@pytest.fixture(scope='session')
def url_address(request):
    return request.config.getoption("--url")


@pytest.fixture(scope='session')
def browser(request):
    browser_name = request.config.getoption("--browser")
    log_level = request.config.getoption("--log_level")

    logger = logging.getLogger(request.node.name)
    file_handler = logging.FileHandler(f"logs/{request.node.name}.log")
    file_handler.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
    logger.addHandler(file_handler)
    logger.setLevel(log_level)

    logger.info("===> Test %s started at %s" % (request.node.name, datetime.datetime.now()))

    if browser_name == "ch":
        driver = webdriver.Chrome()
    elif browser_name == "ff":
        driver = webdriver.Firefox()
    elif browser_name == "eg":
        driver = webdriver.Edge()

    driver.log_level = log_level
    driver.logger = logger
    driver.test_name = request.node.name

    logger.info("Browser %s started" % browser_name)

    yield driver

    def fin():
        driver.quit()
        logger.info("===> Test %s finished at %s" % (request.node.name, datetime.datetime.now()))

    request.addfinalizer(fin)
