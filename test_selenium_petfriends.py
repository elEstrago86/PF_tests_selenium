import time
import pytest
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_petfriends(web_browser):
    web_browser.get("https://petfriends.skillfactory.ru/")
    time.sleep(5)

    btn_newuser = web_browser.find_element(By.XPATH, "//button[@onclick=\"document.location='/new_user';\"]")
    btn_newuser.click()

    btn_exist_acc = web_browser.find_element(By.LINK_TEXT, "У меня уже есть аккаунт")
    btn_exist_acc.click()

    field_email = web_browser.find_element(By.ID, "email")
    field_email.clear()
    field_email.send_keys("estragox@gmail.com")

    field_pass = web_browser.find_element(By.ID, "pass")
    field_pass.clear()
    field_pass.send_keys("QweszxC007")

    btn_submit = web_browser.find_element(By.XPATH, "//button[@type='submit']")
    btn_submit.click()

    time.sleep(5)

    my_pets_link = WebDriverWait(web_browser, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Мои питомцы"))
    )
    my_pets_link.click()

    expected_url = "https://petfriends.skillfactory.ru/my_pets"
    assert web_browser.current_url == expected_url, f"URL после перехода не соответствует ожидаемому. Ожидаемый URL: {expected_url}, текущий URL: {web_browser.current_url}"

    pet_count_element = web_browser.find_element(By.XPATH, "//div[contains(@class, 'col-sm-4 left')]")
    pet_count_text = pet_count_element.text

    pet_count_match = re.search(r'Питомцев: (\d+)', pet_count_text)
    if pet_count_match:
        pet_count = int(pet_count_match.group(1))
    else:
        raise ValueError("Не удалось извлечь количество питомцев")

    assert pet_count == 19, f"Количество питомцев не соответствует ожидаемому. Ожидаемое количество: 19, текущее количество: {pet_count}"
