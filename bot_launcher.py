import json
import sys
import time
import os
import pyperclip

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

USERNAME = os.getenv("PA_USERNAME")
PASSWORD = os.getenv("PA_PASSWORD")

if not USERNAME or not PASSWORD:
    raise ValueError("Не найдены переменные среды PA_USERNAME или PA_PASSWORD")

# Получаем stdin как строку
json_input = sys.stdin.read()

# Настройки для headless
options = uc.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

driver = uc.Chrome(options=options)
wait = WebDriverWait(driver, 20)

# Вход на PythonAnywhere
driver.get("https://www.pythonanywhere.com/login/")
wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(USERNAME)
driver.find_element(By.NAME, "password").send_keys(PASSWORD + Keys.RETURN)

# Переход к редактору moon_data.json
driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/files/home/{USERNAME}")
edit_link = wait.until(EC.element_to_be_clickable((
    By.CSS_SELECTOR,
    f'a[href="/user/{USERNAME}/files/home/{USERNAME}/moon_data.json?edit"]'
)))
edit_link.click()

# Вставка json в редактор
time.sleep(2)
editor = wait.until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))
editor.click()
actions = ActionChains(driver)
actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
pyperclip.copy(json_input)
actions.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()

# Сохраняем (Ctrl+S)
actions.key_down(Keys.CONTROL).send_keys("s").key_up(Keys.CONTROL).perform()
time.sleep(3)

# Открытие новой консоли и запуск скрипта
driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/consoles/")
open_console = wait.until(EC.element_to_be_clickable((
    By.CSS_SELECTOR,
    f'a[href="/user/{USERNAME}/consoles/bash//home/{USERNAME}/new"]'
)))
open_console.click()

time.sleep(10)
driver.switch_to.frame(driver.find_element(By.ID, "id_console"))
body = driver.find_element(By.TAG_NAME, "body")
actions = ActionChains(driver)
actions.move_to_element(body).click().send_keys("python3 pythonanywhere_starter.py", Keys.ENTER).perform()
time.sleep(20)
driver.switch_to.default_content()

# Открытие обработанного файла
driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/files/home/{USERNAME}")
processed_link = wait.until(EC.element_to_be_clickable((
    By.CSS_SELECTOR,
    f'a[href="/user/{USERNAME}/files/home/{USERNAME}/moon_data_processed.json?edit"]'
)))
processed_link.click()

# Копируем результат
editor = wait.until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))
editor.click()
actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
actions.key_down(Keys.CONTROL).send_keys("c").key_up(Keys.CONTROL).perform()
time.sleep(2)

result_text = editor.get_attribute("value")
print(result_text)

driver.quit()
