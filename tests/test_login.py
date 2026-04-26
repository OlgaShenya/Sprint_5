from locators import PageLocators
from utils import (
    BASE_URL,
    TEST_EMAIL,
    TEST_PASSWORD,
    open_login_form,
    wait_visible,
)


class TestLogin:

    def test_login_success(self, driver):
        open_login_form(driver)

        driver.find_element(*PageLocators.LOGIN_EMAIL_INPUT).send_keys(TEST_EMAIL)
        driver.find_element(*PageLocators.LOGIN_PASSWORD_INPUT).send_keys(TEST_PASSWORD)
        driver.find_element(*PageLocators.LOGIN_SUBMIT_BUTTON).click()

        avatar = wait_visible(driver, PageLocators.USER_AVATAR)
        user_name = wait_visible(driver, PageLocators.USER_NAME_LABEL)

        assert avatar.is_displayed()
        assert user_name.is_displayed()
        assert 'User' in user_name.text
        assert BASE_URL in driver.current_url

