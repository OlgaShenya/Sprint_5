import time

import pytest

from locators import PageLocators
from utils import (
    BASE_URL,
    TEST_EMAIL,
    TEST_PASSWORD,
    assert_all_registration_fields_have_errors,
    fill_registration_form,
    wait_visible,
)


class TestRegistration:

    def test_register_new_user_success(self, open_reg_form):
        driver = open_reg_form

        unique_email = f'user_{int(time.time())}@test.com'
        fill_registration_form(driver, unique_email, 'Qwerty123!')

        avatar = wait_visible(driver, PageLocators.USER_AVATAR)
        user_name = wait_visible(driver, PageLocators.USER_NAME_LABEL)

        assert avatar.is_displayed()
        assert user_name.is_displayed()
        assert 'User' in user_name.text
        assert BASE_URL in driver.current_url

    @pytest.mark.parametrize('email', [
        'invalid-email',
        'user@domain',
        '@nodomain.com',
        'user@.com',
        'user name@domain.com',
    ])
    def test_register_with_invalid_email_format(self, open_reg_form, email):
        fill_registration_form(open_reg_form, email, password='', submit_password='')
        assert_all_registration_fields_have_errors(open_reg_form)

    def test_register_existing_user_should_fail(self, open_reg_form):
        fill_registration_form(open_reg_form, email=TEST_EMAIL, password=TEST_PASSWORD)
        assert_all_registration_fields_have_errors(open_reg_form)
