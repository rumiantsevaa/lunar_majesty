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
            element = driver.find_element(by, value)
            element.click()
            return True
        except:
            time.sleep(0.5)
    return False

def wait_and_type(driver, by, value, text, timeout=10):
    for _ in range(timeout * 2):
        try:
            el = driver.find_element(by, value)
            el.clear()
            el.send_keys(text)
            return True
        except:
            time.sleep(0.5)
    return False

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
    options.add_argument("--window-size=1920,1080")  # Добавляем фиксированный размер окна

    print("🌐 Запуск Chrome...")
    driver = uc.Chrome(options=options)
    
    try:
        # 1. Логин в PythonAnywhere
        print("🔐 Выполняется вход в PythonAnywhere...")
        driver.get("https://www.pythonanywhere.com/login/")
        wait_and_type(driver, By.ID, "id_auth-username", USERNAME)
        wait_and_type(driver, By.ID, "id_auth-password", PASSWORD)
        wait_and_click(driver, By.ID, "id_next")
        time.sleep(3)
        print("✅ Вход выполнен")

        # 2. Редактирование moon_data.json
        print("📝 Открытие файла moon_data.json для редактирования...")
        driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/files/home/{USERNAME}/moon_data.json?edit")
        time.sleep(5)
        
        # Фокус на странице
        driver.execute_script("document.body.click()")
        time.sleep(1)
        
        # Выделить всё и удалить
        print("📋 Очистка редактора...")
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
        ActionChains(driver).send_keys(Keys.DELETE).perform()
        time.sleep(1)
        
        # Вставка новых данных
        print("📋 Вставка данных JSON...")
        ActionChains(driver).send_keys(MOON_JSON).perform()
        time.sleep(2)
        
        # Сохранение файла
        print("💾 Сохранение файла...")
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('s').key_up(Keys.CONTROL).perform()
        time.sleep(3)
        print("✅ Файл moon_data.json сохранен")

        # 3. Работа с консолью (упрощенный вариант)
        print("🖥️ Открытие консоли напрямую...")
        driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/consoles/bash//home/{USERNAME}/new")
        time.sleep(15)  # Долгая загрузка консоли

        # Ввод команды через JavaScript
        print("⚡ Ввод команды через JavaScript...")
        driver.execute_script("""
            term_.io.sendString('python3 pythonanywhere_starter.py\\n');
        """)
        time.sleep(20)
        print("✅ Команда выполнена")

        # 4. Получение обработанных данных
        print("📖 Открытие обработанного файла...")
        driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/files/home/{USERNAME}/moon_data_processed.json?edit")
        time.sleep(5)
        
        # Получение содержимого через JavaScript
        print("📋 Получение данных через JavaScript...")
        processed_content = driver.execute_script("""
            try {
                return ace.edit(document.querySelector('.ace_editor')).getValue();
            } catch(e) {
                return document.querySelector('.ace_content').innerText;
            }
        """)
        
        if not processed_content:
            raise Exception("Не удалось получить содержимое файла")

        # 5. Сохранение результата
        print("💾 Сохранение результата...")
        with open('moon_data_processed.json', 'w', encoding='utf-8') as f:
            f.write(processed_content)
        
        print(f"✅ Файл moon_data_processed.json создан ({len(processed_content)} символов)")
        print(f"📝 Предварительный просмотр: {processed_content[:200]}...")
        
    except Exception as e:
        print(f"❌ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("🔚 Закрытие браузера...")
        driver.quit()

if __name__ == "__main__":
    run()
