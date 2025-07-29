import os
import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc

USERNAME = os.getenv("PA_USERNAME")
PASSWORD = os.getenv("PA_PASSWORD")

MOON_DATA = os.getenv("MOON_JSON_TO_WRITE", "NO_DATA_FOUND")

def wait_and_click(driver, by, value, timeout=10):
    for _ in range(timeout * 2):
        try:
            driver.find_element(by, value).click()
            return
        except:
            time.sleep(0.5)
    raise Exception(f"Element not found: {value}")

def wait_and_type(driver, by, value, text, timeout=10):
    for _ in range(timeout * 2):
        try:
            el = driver.find_element(by, value)
            el.clear()
            el.send_keys(text)
            return
        except:
            time.sleep(0.5)
    raise Exception(f"Field not found: {value}")

def run():
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = uc.Chrome(options=options)

    # 1. Вход в PythonAnywhere
    driver.get("https://www.pythonanywhere.com/login/")
    wait_and_type(driver, By.ID, "id_auth-username", USERNAME)
    wait_and_type(driver, By.ID, "id_auth-password", PASSWORD)
    wait_and_click(driver, By.ID, "id_next")
    time.sleep(3)

    # 2. Удаляем старые консоли
    driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/consoles/")
    time.sleep(3)
    for btn in driver.find_elements(By.CSS_SELECTOR, 'span.glyphicon-remove'):
        try:
            btn.click()
            time.sleep(1)
        except:
            pass

    # 3. Открываем файл moon_data.json и записываем в него
    driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/files/home/{USERNAME}/moon_data.json")
    time.sleep(3)
    driver.switch_to.frame(driver.find_element(By.ID, "id_file_editor_iframe"))
    time.sleep(2)
    body = driver.find_element(By.TAG_NAME, "body")
    actions = ActionChains(driver)
    actions.move_to_element(body).click().perform()
    actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
    actions.send_keys(MOON_DATA).perform()
    actions.key_down(Keys.CONTROL).send_keys('s').key_up(Keys.CONTROL).perform()
    time.sleep(2)
    driver.switch_to.default_content()

    # 4. Запускаем новую консоль
    driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/files/home/{USERNAME}")
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, f'a[href="/user/{USERNAME}/consoles/bash//home/{USERNAME}/new"]').click()
    time.sleep(10)

    driver.switch_to.frame(driver.find_element(By.ID, "id_console"))
    time.sleep(5)
    body = driver.find_element(By.TAG_NAME, "body")
    ActionChains(driver).move_to_element(body).click().send_keys("python3 pythonanywhere_starter.py").send_keys(Keys.ENTER).perform()

    time.sleep(15)  # подождём выполнения скрипта
    
    # 5. Открываем файл moon_data_processed.json
    driver = uc.Chrome(options=options)  # Новый экземпляр, чтобы не использовать консольный фрейм
    driver.get("https://www.pythonanywhere.com/login/")
    wait_and_type(driver, By.ID, "id_auth-username", USERNAME)
    wait_and_type(driver, By.ID, "id_auth-password", PASSWORD)
    wait_and_click(driver, By.ID, "id_next")
    time.sleep(3)

    driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/files/home/{USERNAME}")
    time.sleep(3)

    processed_file_selector = f'a[href="/user/{USERNAME}/files/home/{USERNAME}/moon_data_processed.json?edit"]'
    wait_and_click(driver, By.CSS_SELECTOR, processed_file_selector)
    time.sleep(3)

    # 6. Копируем содержимое textarea
    driver.switch_to.frame(driver.find_element(By.ID, "id_file_editor_iframe"))
    time.sleep(2)

    editor = driver.find_element(By.TAG_NAME, "textarea")
    editor.click()
    actions = ActionChains(driver)
    actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
    actions.key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()
    time.sleep(2)

    result_text = editor.get_attribute("value")
    print(result_text)

    driver.quit()

    

run()
