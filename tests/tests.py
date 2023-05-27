import time
import pytest
from selenium.webdriver.common.by import By
from generators.generator import Fake
from src.pages import *
import pickle


def test_redirection(driver, wait):

    driver.get(STEPIC_START_PAGE)

    test_value = wait.url_is(STEPIC_BASE_PAGE)
    assert test_value, 'Redirection failed'


def test_account_creating(driver, wait):

    fake = Fake('ru_RU')
    fullname = fake.create_full_name()
    email = fake.create_email()
    password = fake.create_password()

    driver.get(STEPIC_BASE_PAGE)
    wait.title_is(STEPIC_EXPECTED_TITLE)
    time.sleep(1)

    wait.element_is_visible((By.XPATH, REGISTRATION_BUTTON)).click()
    wait.element_is_clickable((By.NAME, REG_FULLNAME_FIELD)) \
        .send_keys(fullname)
    driver.find_element(By.NAME, REG_EMAIL_FIELD) \
        .send_keys(email)
    driver.find_element(By.NAME, REG_PASS_FIELD) \
        .send_keys(password)
    driver.find_element(By.XPATH, REGISTRATION_CONFIRMATION_BUTTON).click()

    test_value = wait.element_is_presence((By.XPATH, ACCOUNT_BUTTON))
    assert test_value, 'Failed to create an account'

    with open('users_data.txt', 'a', encoding='utf-8') as file:
        file.write(f'{fullname} {email} {password}\n')

    with open('cookie', 'wb') as file:
        pickle.dump(driver.get_cookies(), file)
    driver.delete_all_cookies()


def test_login_with_cookie(driver, wait):
    """Cookies must be created by 'test_account_creating'
        or something else"""

    driver.get(STEPIC_BASE_PAGE)
    wait.title_is(STEPIC_EXPECTED_TITLE)
    time.sleep(1)

    with open('cookie', 'rb') as file:
        [driver.add_cookie(i) for i in pickle.load(file)]

    driver.refresh()

    test_value = wait.element_is_presence((By.XPATH, ACCOUNT_BUTTON))
    assert test_value, 'Failed to login into account'


def test_subscribe_to_course(driver, wait):
    """Use together with 'test_login_with_cookie' """

    driver.get(COURSE_PAGE)
    time.sleep(1)
    wait.element_is_clickable(
        (By.XPATH, SUBSCRIBE_TO_COURSE_BUTTON)) \
        .click()
    wait.url_contain('https://stepik.org/lesson')
    driver.get(CURRENTLY_COURSES_PAGE)

    test_value = wait.element_is_presence(
        (By.XPATH, CURRENTLY_COURSES_FIRST_ITEM)) \
        .accessible_name
    assert CODE_WORD == test_value, 'Failed to subscribing'


def test_logout(driver, wait):
    """Use together with 'test_login_with_cookie' """

    driver.get(STEPIC_BASE_PAGE)
    wait.title_is(STEPIC_EXPECTED_TITLE)
    time.sleep(1)

    driver.find_element(By.XPATH, ACCOUNT_BUTTON) \
        .click()
    wait.element_is_clickable((By.XPATH, LOGOUT_BUTTON)) \
        .click()
    wait.element_is_visible((By.XPATH, LOGOUT_CONFIRMATION_BUTTON)) \
        .click()
    wait.title_is(STEPIC_EXPECTED_TITLE)

    test_value = wait.element_is_presence((By.XPATH, REGISTRATION_BUTTON))
    assert test_value, 'Failed to logout from account'


def test_search_by_code_word(driver, wait):

    driver.get(STEPIC_BASE_PAGE)
    wait.title_is(STEPIC_EXPECTED_TITLE)
    time.sleep(1)

    driver.find_element(By.CSS_SELECTOR, SEARCH_INPUT) \
        .send_keys(CODE_WORD)
    wait.element_is_visible((By.XPATH, SEARCH_DROPDOWN))
    driver.find_element(By.CSS_SELECTOR, SEARCH_BUTTON) \
        .click()

    test_value = wait.title_is(f'{CODE_WORD} · Каталог · Stepik')
    assert test_value, 'The system incorrectly processed the input of information'

    test_value = wait.element_is_visible(
        (By.XPATH, SEARCH_RESULT_FIRST_ITEM)) \
        .accessible_name
    assert CODE_WORD == test_value, 'The system returned incorrectly data'


@pytest.mark.parametrize('language, expected_text, li', [
    ('Беларуская', 'Рэгістрацыя', '1'),
    ('Deutsch', 'Anmelden', '2'),
    ('English', 'Register', '3'),
    ('Español', 'Registro', '4'),
    ('Português', 'Registrar', '5'),
    ('Русский', 'Регистрация', '6'),
    ('Українська', 'Реєстрація', '7'),
    ('简体中文', '寄存器', '8')
])
def test_language_switch(language, expected_text, li,
                         driver, wait):
    driver.get(STEPIC_BASE_PAGE)
    wait.title_is(STEPIC_EXPECTED_TITLE)
    time.sleep(1)

    wait.element_is_clickable((By.XPATH, LANGUAGE_BUTTON)) \
        .click()
    time.sleep(1)
    wait.element_is_visible((By.XPATH, f'/html/body/header/nav/div[3]/div[2]/div/div/ul/li[{li}]/button')) \
        .click()
    time.sleep(2)
    driver.delete_all_cookies()

    test_value = wait.until(
        lambda x: driver.find_element(
            By.XPATH, REGISTRATION_BUTTON).text)
    assert test_value == expected_text, 'Failed to switch a language'
