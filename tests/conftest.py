import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service


def pytest_addoption(parser):
    parser.addoption("--browser", default="ch", choices=["eg", "ch", "ff"])
    parser.addoption("--url", default="http://192.168.100.32/")


@pytest.fixture()
def url_address(request):
    return request.config.getoption("--url")


@pytest.fixture()
def browser(request):
    browser_name = request.config.getoption("--browser")
    if browser_name == "ch":
        driver = webdriver.Chrome()
    elif browser_name == "ff":
        driver = webdriver.Firefox()
    elif browser_name == "eg":
        driver = webdriver.Edge()

    yield driver

    driver.quit()
