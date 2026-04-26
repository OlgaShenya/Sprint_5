# Sprint 5 — UI-автотесты для qa-desk

Набор UI-автотестов на **Python + Selenium + pytest** для учебного сервиса
объявлений `qa-desk.education-services.ru`. Тесты покрывают ключевые
пользовательские сценарии: вход, выход, регистрацию и создание объявления.

## Стек

- Python 3
- [pytest](https://docs.pytest.org/) — раннер тестов
- [Selenium WebDriver](https://www.selenium.dev/) — управление браузером
- Google Chrome + ChromeDriver (запускается через `webdriver.Chrome`)

## Структура проекта

```
Sprint_5/
├── conftest.py            # фикстуры pytest (driver, open_reg_form)
├── locators.py            # все XPath-локаторы и цвета ошибок валидации
├── utils.py               # константы + общие хелперы (логин, ожидания и т.д.)
├── pytest.ini             # конфигурация pytest
├── README.md              # этот файл
└── tests/
    ├── __init__.py
    ├── test_login.py          # авторизация существующего пользователя
    ├── test_logout.py         # выход из аккаунта
    ├── test_registration.py   # регистрация нового пользователя и негативные кейсы
    └── test_create_advert.py  # создание объявления и проверка без авторизации
```

### `conftest.py`

Содержит только pytest-фикстуры:

- `driver` — поднимает Chrome с отключённой проверкой утечки паролей
  (`profile.password_manager_leak_detection = False`), отдаёт его тесту
  и закрывает браузер после теста.
- `open_reg_form` — открывает главную, переходит на форму входа, кликает
  «Нет аккаунта» и возвращает `driver` уже на форме регистрации.

### `locators.py`

Класс `PageLocators` со всеми XPath-локаторами, сгруппированными по разделам:

- общие селекторы попап-формы;
- главная страница (кнопка входа, аватар, имя пользователя);
- форма входа;
- форма регистрации (поля, кнопки и обёртки полей с ошибками);
- форма создания объявления (поля, дропдауны категории и города,
  переключатель состояния, кнопка публикации);
- блок «Мои объявления» и пагинация;
- модалка «Чтобы разместить объявление, авторизуйтесь».

Также экспортируются константы цвета валидационной рамки
(`ERROR_BORDER_HEX`, `ERROR_BORDER_RGB`) и шаблон локатора
`MY_CARD_BY_TITLE_TEMPLATE`, в который при использовании подставляется
заголовок объявления.

### `utils.py`

Единая точка переиспользования: константы и helper-функции, чтобы тесты
не дублировали друг друга.

Константы:

- `BASE_URL` — адрес стенда;
- `DEFAULT_TIMEOUT` — таймаут ожиданий по умолчанию (5 секунд);
- `TEST_EMAIL`, `TEST_PASSWORD` — учётка существующего пользователя.

Обёртки над `WebDriverWait`:

- `wait_visible(driver, locator)` — `visibility_of_element_located`;
- `wait_clickable(driver, locator)` — `element_to_be_clickable`;
- `wait_present(driver, locator)` — `presence_of_element_located`;
- `wait_invisible(driver, locator)` — `invisibility_of_element_located`;
- `wait_visible_of(driver, element)` — `visibility_of` для уже найденного
  WebElement.

Шаги UI:

- `open_login_form(driver)` — открыть главную и перейти к форме входа.
- `open_registration_form(driver)` — открыть форму регистрации (через форму
  входа → «Нет аккаунта»). Используется фикстурой `open_reg_form`.
- `login(driver, email=TEST_EMAIL, password=TEST_PASSWORD)` — полный
  сценарий авторизации, с ожиданием появления аватара в шапке.
- `fill_registration_form(driver, email, password, submit_password=None)` —
  заполняет поля формы регистрации и жмёт «Создать аккаунт». Если
  `submit_password` не указан, по умолчанию совпадает с `password`. Пустые
  значения паролей пропускаются (для негативных сценариев).

Проверки валидации формы регистрации:

- `assert_field_has_error_border(driver, wrapper_locator)` — у поля стоит
  красная рамка ошибки (`#FF6972` / `rgb(255, 105, 114)`).
- `assert_all_registration_fields_have_errors(driver)` — у всех трёх
  полей (email, password, submitPassword) есть валидационная рамка, и в
  span с ошибкой отображается текст «Ошибка». Перед проверкой ждём
  появления обёртки с классом `input_inputError`.

Прочее:

- `format_locator(template_locator, *args)` — подставляет аргументы в
  xpath-шаблон, например для поиска карточки объявления по её заголовку.

### `pytest.ini`

```
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
pythonpath = .
```

`pythonpath = .` позволяет тестам импортировать `locators` и `utils`
напрямую, без относительных путей.

## Тесты

### `tests/test_login.py` — `TestLogin`

- **`test_login_success`** — открывает главную, вводит существующие
  email/пароль, отправляет форму. Проверяет, что в шапке появились
  аватар и имя пользователя «User», и что URL остаётся на `BASE_URL`.

### `tests/test_logout.py` — `TestLogout`

- **`test_logout_success`** — авторизуется хелпером `login(driver)`,
  кликает «Выйти». Проверяет, что в шапке снова виден «Вход и
  регистрация», а аватар и имя пользователя пропали из DOM.

### `tests/test_registration.py` — `TestRegistration`

Использует фикстуру `open_reg_form`, которая сразу открывает форму
регистрации.

- **`test_register_new_user_success`** — регистрирует пользователя с
  уникальным email вида `user_<timestamp>@test.com` и валидным паролем.
  Проверяет появление аватара/имени и редирект на главную.
- **`test_register_with_invalid_email_format`** — параметризованный
  негативный тест, отправляет форму только с невалидным email и
  пустыми паролями. Перебираемые значения:
  - `invalid-email`
  - `user@domain`
  - `@nodomain.com`
  - `user@.com`
  - `user name@domain.com`
  
  Ожидает красные рамки у всех полей и текст «Ошибка».
- **`test_register_existing_user_should_fail`** — пробует
  зарегистрировать пользователя с уже занятыми `TEST_EMAIL` /
  `TEST_PASSWORD`. Ожидает те же индикаторы ошибки.

### `tests/test_create_advert.py` — `TestCreateAdvert`

- **`test_create_advert_success`** — полный путь создания объявления:
  1. логинится через `login(driver)`;
  2. открывает форму создания объявления;
  3. заполняет название (с timestamp для уникальности), описание, цену
     (15000);
  4. выбирает категорию «Хобби» и город «Казань» из дропдаунов;
  5. отмечает состояние «Б/У» и публикует;
  6. ждёт закрытия формы публикации, скроллит вверх и переходит в
     профиль через клик по аватару;
  7. в блоке «Мои объявления» прокручивает пагинацию до конца и
     находит карточку по заголовку через
     `format_locator(MY_CARD_BY_TITLE_TEMPLATE, advert_title)`;
  8. проверяет, что заголовок и цена в карточке совпадают с тем, что
     ввёл пользователь.
- **`test_create_advert_no_auth_fail`** — без авторизации жмёт
  «Разместить объявление» и проверяет, что появилась модалка с
  заголовком «Чтобы разместить объявление, авторизуйтесь».

## Запуск

Установите зависимости (Selenium и pytest) и убедитесь, что в системе
установлен Google Chrome совместимой с ChromeDriver версии.

Запуск всех тестов из корня проекта:

```
pytest
```

Запуск отдельного файла:

```
pytest tests/test_login.py
```

Запуск одного теста:

```
pytest tests/test_create_advert.py::TestCreateAdvert::test_create_advert_success
```

Подробный вывод:

```
pytest -v
```

## Тестовые данные

Тесты, которым нужен уже существующий пользователь
(`test_login_success`, `test_logout_success`, `test_create_advert_success`,
`test_register_existing_user_should_fail`), используют учётку из
`utils.py`:

- email: `123qw@mail.ru`
- пароль: `123qw`

Тест регистрации нового пользователя каждый раз использует уникальный
email на основе текущего времени, поэтому может перезапускаться без
ручной очистки данных.
