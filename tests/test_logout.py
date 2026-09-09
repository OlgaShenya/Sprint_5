from locators import PageLocators
from utils import login, wait_visible


class TestLogout:

    def test_logout_success(self, driver):
        login(driver)

        driver.find_element(*PageLocators.LOGOUT_BUTTON).click()

        enter_reg_button = wait_visible(driver, PageLocators.ENTER_REG_BUTTON)

        assert enter_reg_button.is_displayed()
        assert len(driver.find_elements(*PageLocators.USER_AVATAR)) == 0
        assert len(driver.find_elements(*PageLocators.USER_NAME_LABEL)) == 0
