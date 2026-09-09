"""Общие константы и вспомогательные функции для UI-тестов."""

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locators import PageLocators, ERROR_BORDER_HEX, ERROR_BORDER_RGB


BASE_URL = 'https://qa-desk.education-services.ru/'
DEFAULT_TIMEOUT = 5

TEST_EMAIL = '123qw@mail.ru'
TEST_PASSWORD = '123qw'


def wait_visible(driver, locator, timeout=DEFAULT_TIMEOUT):
    """Ждёт видимости элемента по локатору и возвращает его."""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )


def wait_clickable(driver, locator, timeout=DEFAULT_TIMEOUT):
    """Ждёт кликабельности элемента и возвращает его."""
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(locator)
    )


def wait_present(driver, locator, timeout=DEFAULT_TIMEOUT):
    """Ждёт появления элемента в DOM и возвращает его."""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(locator)
    )


def wait_invisible(driver, locator, timeout=DEFAULT_TIMEOUT):
    """Ждёт, пока элемент исчезнет из видимости."""
    return WebDriverWait(driver, timeout).until(
        EC.invisibility_of_element_located(locator)
    )


def wait_visible_of(driver, element, timeout=DEFAULT_TIMEOUT):
    """Ждёт видимости конкретного WebElement (а не локатора)."""
    return WebDriverWait(driver, timeout).until(EC.visibility_of(element))


def open_login_form(driver):
    """Открыть главную страницу и перейти на форму входа."""
    driver.get(BASE_URL)
    driver.find_element(*PageLocators.ENTER_REG_BUTTON).click()
    wait_visible(driver, PageLocators.LOGIN_FORM_TITLE)


def open_registration_form(driver):
    """Открыть форму регистрации (вход → Нет аккаунта)."""
    open_login_form(driver)
    driver.find_element(*PageLocators.NO_ACCOUNT_BUTTON).click()
    wait_visible(driver, PageLocators.REG_FORM_TITLE)


def login(driver, email=TEST_EMAIL, password=TEST_PASSWORD):
    """Полный сценарий авторизации существующим пользователем."""
    open_login_form(driver)
    driver.find_element(*PageLocators.LOGIN_EMAIL_INPUT).send_keys(email)
    driver.find_element(*PageLocators.LOGIN_PASSWORD_INPUT).send_keys(password)
    driver.find_element(*PageLocators.LOGIN_SUBMIT_BUTTON).click()
    wait_visible(driver, PageLocators.USER_AVATAR)


def fill_registration_form(driver, email, password, submit_password=None):
    """Заполняет форму регистрации и кликает по Создать аккаунт."""
    if submit_password is None:
        submit_password = password
    driver.find_element(*PageLocators.REG_EMAIL_INPUT).send_keys(email)
    if password:
        driver.find_element(*PageLocators.REG_PASSWORD_INPUT).send_keys(password)
    if submit_password:
        driver.find_element(*PageLocators.REG_SUBMIT_PASSWORD_INPUT).send_keys(submit_password)
    driver.find_element(*PageLocators.CREATE_ACCOUNT_BUTTON).click()


def assert_field_has_error_border(driver, wrapper_locator):
    """Проверяет, что у поля валидационная красная рамка."""
    border = driver.find_element(*wrapper_locator).value_of_css_property('border')
    assert ERROR_BORDER_HEX in border or ERROR_BORDER_RGB in border


def assert_all_registration_fields_have_errors(driver):
    """Проверяет красные рамки у email + обеих парольных полей и текст «Ошибка»."""
    wait_present(driver, PageLocators.REG_EMAIL_ERROR_WRAPPER)

    for wrapper in (
        PageLocators.REG_EMAIL_ERROR_WRAPPER,
        PageLocators.REG_PASSWORD_ERROR_WRAPPER,
        PageLocators.REG_PASSWORD_SUBMIT_ERROR_WRAPPER,
    ):
        assert_field_has_error_border(driver, wrapper)

    error_text = driver.find_element(*PageLocators.REG_EMAIL_ERROR_SPAN).text
    assert error_text == 'Ошибка'


def format_locator(template_locator, *args):
    """Подставляет аргументы в xpath-шаблон локатора."""
    return (template_locator[0], template_locator[1].format(*args))
