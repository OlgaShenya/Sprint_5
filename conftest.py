import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils import open_registration_form


@pytest.fixture
def driver():
    chrome_options = Options()

    prefs = {
        "profile.password_manager_leak_detection": False,
    }
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()


@pytest.fixture
def open_reg_form(driver):
    """Открывает главную и переходит на форму регистрации."""
    open_registration_form(driver)
    return driver
