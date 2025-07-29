import os
import json
import time
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

USERNAME = os.environ['PA_USERNAME']
PASSWORD = os.environ['PA_PASSWORD']
MOON_JSON_RAW = os.environ['MOON_JSON']
MOON_JSON = json.dumps(json.loads(MOON_JSON_RAW), indent=2)

# --- Set up Selenium in headless mode ---
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
actions = ActionChains(driver)

# --- LOGIN ---
driver.get("https://www.pythonanywhere.com/login/")
time.sleep(2)
driver.find_element(By.ID, "id_auth-username").send_keys(USERNAME)
driver.find_element(By.ID, "id_auth-password").send_keys(PASSWORD)
driver.find_element(By.ID, "id_next").click()
time.sleep(3)

# --- OPEN moon_data.json and overwrite contents ---
driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/files/home/{USERNAME}")
time.sleep(2)
driver.find_element(By.XPATH, f'//a[@title="moon_data.json"]').click()
time.sleep(4)

pyperclip.copy(MOON_JSON)
actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
time.sleep(1)
actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
time.sleep(1)
actions.key_down(Keys.CONTROL).send_keys('s').key_up(Keys.CONTROL).perform()
time.sleep(2)

# --- OPEN CONSOLE AND RUN SCRIPT ---
driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/consoles/")
time.sleep(3)
driver.find_element(By.PARTIAL_LINK_TEXT, 'Start a new console').click()
time.sleep(10)

driver.switch_to.frame(driver.find_element(By.ID, "id_console"))
body = driver.find_element(By.TAG_NAME, "body")
actions = ActionChains(driver)
actions.move_to_element(body).click().send_keys("python3 pythonanywhere_starter.py").send_keys(Keys.ENTER).perform()
time.sleep(20)

# --- GET PROCESSED OUTPUT ---
driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/files/home/{USERNAME}")
time.sleep(2)
driver.find_element(By.XPATH, f'//a[@title="moon_data_processed.json"]').click()
time.sleep(3)

actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
time.sleep(1)
actions.key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()
time.sleep(1)

# --- Save copied text from clipboard ---
output = pyperclip.paste()
with open("moon_data_processed.json", "w") as f:
    f.write(output)

driver.quit()
