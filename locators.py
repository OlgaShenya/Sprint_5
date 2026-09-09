from selenium.webdriver.common.by import By

ERROR_BORDER_HEX = '#FF6972'
ERROR_BORDER_RGB = 'rgb(255, 105, 114)'



def _error_wrapper(input_xpath: str) -> str:
    """XPath родительского div поля с классом ошибки."""
    return f'{input_xpath}/parent::div[contains(@class, "input_inputError")]'


class PageLocators:
    _FORM = '//form[@class="popUp_shell__LuyqR"]'
    _REG_FORM = f'{_FORM}[.//h1[text()="Зарегистрироваться"]]'
    _LOGIN_FORM = f'{_FORM}[.//h1[text()="Войти"]]'

    ENTER_REG_BUTTON = (By.XPATH, '//button[text() = "Вход и регистрация"]')
    USER_AVATAR = (By.XPATH, '//button[@class="circleSmall"]')
    USER_NAME_LABEL = (By.XPATH, '//*[@id="root"]//h3[@class="profileText name"]')

    LOGIN_FORM_TITLE = (By.XPATH, f'{_LOGIN_FORM}//h1[text()="Войти"]')
    NO_ACCOUNT_BUTTON = (By.XPATH, f'{_FORM}//button[text()="Нет аккаунта"]')
    LOGIN_EMAIL_INPUT = (By.XPATH, f'{_LOGIN_FORM}//input[@name="email"]')
    LOGIN_PASSWORD_INPUT = (By.XPATH, f'{_LOGIN_FORM}//input[@name="password"]')
    LOGIN_SUBMIT_BUTTON = (By.XPATH, f'{_LOGIN_FORM}//button[text()="Войти"]')

    LOGOUT_BUTTON = (By.XPATH, '//button[text()="Выйти"]')

    REG_FORM_TITLE = (By.XPATH, f'{_FORM}//h1[text()="Зарегистрироваться"]')
    _EMAIL_XPATH = f'{_REG_FORM}//input[@name="email"]'
    _PASSWORD_XPATH = f'{_REG_FORM}//input[@name="password"]'
    _SUBMIT_PASSWORD_XPATH = f'{_REG_FORM}//input[@name="submitPassword"]'

    REG_EMAIL_INPUT = (By.XPATH, _EMAIL_XPATH)
    REG_PASSWORD_INPUT = (By.XPATH, _PASSWORD_XPATH)
    REG_SUBMIT_PASSWORD_INPUT = (By.XPATH, _SUBMIT_PASSWORD_XPATH)
    CREATE_ACCOUNT_BUTTON = (By.XPATH, f'{_REG_FORM}//button[text()="Создать аккаунт"]')

    REG_EMAIL_ERROR_WRAPPER = (By.XPATH, _error_wrapper(_EMAIL_XPATH))
    REG_PASSWORD_ERROR_WRAPPER = (By.XPATH, _error_wrapper(_PASSWORD_XPATH))
    REG_PASSWORD_SUBMIT_ERROR_WRAPPER = (By.XPATH, _error_wrapper(_SUBMIT_PASSWORD_XPATH))
    REG_EMAIL_ERROR_SPAN = (By.XPATH, f'({_REG_FORM}//span[@class="input_span__yWPqB"])[1]')

    GOODS_FORM_CREATE = (By.XPATH, '//form[contains(@class, "createListing_shell")]')
    ADD_ADVERT = (By.XPATH, '//button[contains(text(), "Разместить объявление")]')
    PUBLISH_ADVERT = (By.XPATH, '//button[text()="Опубликовать"]')
    GOODS_NAME = (By.XPATH, '//input[@name="name"]')
    GOODS_DESCRIPTION = (By.XPATH, '//textarea[@name="description"]')
    GOODS_PRICE = (By.XPATH, '//input[@name="price"]')
    CATEGORY_MENU_BUTTON = (By.XPATH, "//div[contains(@class, 'dropDownMenu_input')]/button[contains(@class, 'arrowDown')][1]")
    CATEGORY_MENU_ITEM = (By.XPATH, '//button/span[text() = "Хобби"]')
    CITY_MENU_BUTTON = (By.XPATH, "//input[@name='city']/following-sibling::button[contains(@class, 'arrowDown')]")    
    CITY_MENU_ITEM = (By.XPATH, '//button/span[text() = "Казань"]')
    GOODS_CONDITION = (By.XPATH, "//input[@name='condition' and @value='Б/У']/following-sibling::div[contains(@class, 'radioUnput_inputRegular')]")
    MY_ADVERTS_BLOCK = (By.XPATH, '//h1[text()="Мои объявления"]/parent::div')
    MY_CARD_TITLE = (By.XPATH, '//div[contains(@class, "grid_twoColumns")]/div[@class="card"][last()]/div[@class="description"]/div[@class="about"]/h2')
    MY_CARD_BY_TITLE_TEMPLATE = (
        By.XPATH, 
        '//div[@class="card"]//div[@class="about"]//h2[contains(text(), "{}")]'
    )
    MY_CARD_CITY = (By.XPATH, '//div[@class="description"]/div[@class="about"]/h3')
    MY_CARD_PRICE = (By.XPATH, '//div[@class="description"]/div[@class="price"]/h2')

    PAGINATION_BTN_RIGHT = (By.XPATH, '//button[contains(@class, "arrowButton--right")]')
    AUTH_MODAL_BEFORE_ADVERT = (By.XPATH, '//form[.//h1[text()="Чтобы разместить объявление, авторизуйтесь"]]')
    AUTH_MODAL_BEFORE_ADVERT_HEADER = (By.XPATH, '//form[.//h1[text()="Чтобы разместить объявление, авторизуйтесь"]]//h1')
    