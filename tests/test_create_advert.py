import time

from locators import PageLocators
from utils import (
    BASE_URL,
    format_locator,
    login,
    wait_clickable,
    wait_invisible,
    wait_present,
    wait_visible,
    wait_visible_of,
)


class TestCreateAdvert:

    def test_create_advert_success(self, driver):
        login(driver)

        wait_clickable(driver, PageLocators.ADD_ADVERT).click()

        advert_title = f'Гитара акустическая {int(time.time())}'
        advert_description = 'Почти новая, в отличном состоянии, продаю за ненадобностью.'
        advert_price = 15000

        wait_visible(driver, PageLocators.GOODS_NAME).send_keys(advert_title)
        driver.find_element(*PageLocators.GOODS_DESCRIPTION).send_keys(advert_description)
        driver.find_element(*PageLocators.GOODS_PRICE).send_keys(advert_price)

        driver.find_element(*PageLocators.CATEGORY_MENU_BUTTON).click()
        wait_clickable(driver, PageLocators.CATEGORY_MENU_ITEM).click()

        wait_clickable(driver, PageLocators.CITY_MENU_BUTTON).click()
        wait_clickable(driver, PageLocators.CITY_MENU_ITEM).click()

        driver.find_element(*PageLocators.GOODS_CONDITION).click()

        driver.find_element(*PageLocators.PUBLISH_ADVERT).click()

        wait_invisible(driver, PageLocators.GOODS_FORM_CREATE)
        driver.execute_script("window.scrollTo(0, 0);")
        wait_clickable(driver, PageLocators.USER_AVATAR).click()

        my_adverts_block = wait_present(driver, PageLocators.MY_ADVERTS_BLOCK)
        driver.execute_script("arguments[0].scrollIntoView();", my_adverts_block)
        wait_visible_of(driver, my_adverts_block)

        arrow_btn = wait_present(driver, PageLocators.PAGINATION_BTN_RIGHT)
        while arrow_btn.is_enabled():
            arrow_btn.click()

        card_title = wait_visible(
            driver,
            format_locator(PageLocators.MY_CARD_BY_TITLE_TEMPLATE, advert_title),
        )

        card_price = driver.find_element(*PageLocators.MY_CARD_PRICE)
        card_price_value = int(''.join(filter(str.isdigit, card_price.text)))

        assert my_adverts_block.is_displayed()
        assert card_title.text == advert_title
        assert advert_price == card_price_value

    def test_create_advert_no_auth_fail(self, driver):
        driver.get(BASE_URL)
        wait_clickable(driver, PageLocators.ADD_ADVERT).click()

        modal = wait_visible(driver, PageLocators.AUTH_MODAL_BEFORE_ADVERT)
        assert modal.is_displayed()

        modal_header = driver.find_element(*PageLocators.AUTH_MODAL_BEFORE_ADVERT_HEADER)
        assert modal_header.text.strip() == "Чтобы разместить объявление, авторизуйтесь"

