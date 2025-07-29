import os
import time
import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

USERNAME = os.getenv("PA_USERNAME")
PASSWORD = os.getenv("PA_PASSWORD")
MOON_JSON = os.getenv("MOON_JSON")

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
    print("🚀 Запуск бота...")
    print(f"📋 Username: {USERNAME}")
    print(f"🌙 Moon data available: {'Yes' if MOON_JSON else 'No'}")
    
    if not USERNAME or not PASSWORD:
        print("❌ ОШИБКА: Не заданы PA_USERNAME или PA_PASSWORD")
        return
    
    if not MOON_JSON:
        print("❌ ОШИБКА: Не найдены данные MOON_JSON")
        return
    
    try:
        moon_data = json.loads(MOON_JSON)
        print(f"✅ Данные луны загружены: {len(moon_data)} разделов")
    except json.JSONDecodeError as e:
        print(f"❌ ОШИБКА парсинга JSON: {e}")
        return
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")

    print("🌐 Запуск Chrome...")
    driver = uc.Chrome(options=options)
    
    try:
        # Логин
        print("🔐 Выполняется вход в PythonAnywhere...")
        driver.get("https://www.pythonanywhere.com/login/")
        wait_and_type(driver, By.ID, "id_auth-username", USERNAME)
        wait_and_type(driver, By.ID, "id_auth-password", PASSWORD)
        wait_and_click(driver, By.ID, "id_next")
        time.sleep(3)
        print("✅ Вход выполнен")

        # Закрытие консолей
        print("🧹 Закрытие старых консолей...")
        driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/consoles/")
        time.sleep(3)
        close_buttons = driver.find_elements(By.CSS_SELECTOR, 'span.glyphicon-remove')
        print(f"📝 Найдено {len(close_buttons)} консолей для закрытия")
        for i, btn in enumerate(close_buttons):
            try:
                btn.click()
                time.sleep(1)
                print(f"✅ Закрыта консоль {i+1}")
            except Exception as e:
                print(f"⚠️ Не удалось закрыть консоль {i+1}: {e}")

        # Переход к файлам и открытие bash консоли
        print("📁 Переход к файлам...")
        driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/files/home/{USERNAME}")
        time.sleep(2)
        
        print("🖥️ Открытие новой bash консоли...")
        open_link = driver.find_element(By.CSS_SELECTOR, f'a[href="/user/{USERNAME}/consoles/bash//home/{USERNAME}/new"]')
        open_link.click()
        time.sleep(15)  # Увеличиваем время ожидания

        # Переключение на iframe консоли
        print("🔄 Переключение на консоль...")
        driver.switch_to.frame(driver.find_element(By.ID, "id_console"))
        time.sleep(5)
        
        # Создание файла с данными JSON
        print("📝 Создание файла с данными луны...")
        body = driver.find_element(By.TAG_NAME, "body")
        actions = ActionChains(driver)
        actions.move_to_element(body).click()
        
        # Экранируем JSON для безопасной передачи
        json_escaped = MOON_JSON.replace("'", "\\'").replace('"', '\\"')
        actions.send_keys(f'echo \'{MOON_JSON}\' > moon_data_input.json')
        actions.send_keys(Keys.ENTER)
        actions.perform()
        time.sleep(2)
        
        # Выполнение основного скрипта
        print("⚡ Запуск pythonanywhere_starter.py...")
        actions = ActionChains(driver)
        actions.move_to_element(body).click()
        actions.send_keys('python3 pythonanywhere_starter.py')
        actions.send_keys(Keys.ENTER)
        actions.perform()
        
        # Увеличиваем время ожидания для выполнения скрипта
        print("⏳ Ожидание выполнения скрипта...")
        time.sleep(30)
        
        # Проверяем результат
        print("🔍 Проверка результата...")
        actions = ActionChains(driver)
        actions.move_to_element(body).click()
        actions.send_keys('ls -la *.json')
        actions.send_keys(Keys.ENTER)
        actions.perform()
        time.sleep(3)
        
        print("✅ Бот успешно запущен и выполнен!")
        
    except Exception as e:
        print(f"❌ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("🔚 Закрытие браузера...")
        driver.quit()

if __name__ == "__main__":
    run()
