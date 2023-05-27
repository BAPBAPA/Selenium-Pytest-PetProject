import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from wait_class.wait_instance import *


@pytest.fixture(scope='session')
def driver():
    driver_service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(service=driver_service, options=options)
    driver.maximize_window()

    yield driver
    driver.quit()


@pytest.fixture(scope='session')
def wait(driver):
    wait = Wait(driver)

    return wait
