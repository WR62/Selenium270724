import pytest

import logging
import allure
import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def pytest_addoption(parser):
    parser.addoption("--browser", default="ch", choices=["eg", "ch", "ff"])
    parser.addoption("--url", default="http://192.168.100.32")   # http://192.168.43.15
    parser.addoption("--log_level", action="store", default="INFO")
    parser.addoption("--remote", action="store_true")
    parser.addoption("--video", action="store_true")
    parser.addoption("--vnc", action="store_true")
    parser.addoption("--brver")


@pytest.fixture(scope='session')
def url_address(request):
    return request.config.getoption("--url")


@pytest.fixture(scope='session')
def browser(request):
    browser_name = request.config.getoption("--browser")
    log_level = request.config.getoption("--log_level")
    remote_run = request.config.getoption("--remote")
    video = request.config.getoption("--video")
    vnc = request.config.getoption("--vnc")
    brver = request.config.getoption("--brver")

    logger = logging.getLogger(request.node.name)
    file_handler = logging.FileHandler(f"logs/{request.node.name}.log")
    file_handler.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
    logger.addHandler(file_handler)
    logger.setLevel(log_level)

    logger.info("===> Test %s started at %s" % (request.node.name, datetime.datetime.now()))

    if remote_run is False:
        if browser_name == "ch":
            driver = webdriver.Chrome()
        elif browser_name == "ff":
            driver = webdriver.Firefox()
        elif browser_name == "eg":
            driver = webdriver.Edge()
        else:
            driver = webdriver.Chrome()
    else:
        url_for_executor = request.config.getoption("--url")
        executor_url = f"{url_for_executor}:4444/wd/hub"
        if browser_name == "ch" or browser_name == "eg":
            options = ChromeOptions()
        elif browser_name == "ff":
            options = FirefoxOptions()
        else:
            options = ChromeOptions()
            browser_name = "ch"

        def set_caps():
            dict_name_browser = {"ch": "chrome", "ff": "firefox", "eg": "MicrosoftEdge"}
            dict_default_versions = {"chrome": "128.0", "firefox": "125.0", "MicrosoftEdge": "124.0"}
            caps_br_name = dict_name_browser[browser_name]

            if brver == "":
                caps_br_version = dict_default_versions[caps_br_name]
            else:
                caps_br_version = brver

            capabilities = {
                "browserName": caps_br_name,
                "browserVersion": caps_br_version,
                "selenoid:options": {
                    "enableVideo": video,
                    "enableVNC": vnc,
                    "name": request.node.name
                }
            }
            return capabilities

        for k, v in set_caps().items():
            options.set_capability(k, v)
        driver = webdriver.Remote(command_executor=executor_url, options=options)

    driver.log_level = log_level
    driver.logger = logger
    driver.test_name = request.node.name
    driver.maximize_window()

    logger.info("Browser %s started" % browser_name)

    yield driver

    def fin():
        driver.quit()
        logger.info("===> Test %s finished at %s" % (request.node.name, datetime.datetime.now()))

    request.addfinalizer(fin)
