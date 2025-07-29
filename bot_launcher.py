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
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
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

def wait_for_element(driver, by, value, timeout=10):
    for _ in range(timeout * 2):
        try:
            return driver.find_element(by, value)
        except:
            time.sleep(0.5)
    raise Exception(f"Element not found: {value}")

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
        
        # Переключение на iframe редактора
        print("🔄 Поиск iframe редактора...")
        iframe = wait_for_element(driver, By.ID, "id_file_editor_iframe")
        driver.switch_to.frame(iframe)
        time.sleep(3)
        
        # Находим текстовый редактор
        print("🔍 Поиск текстового редактора...")
        editor = wait_for_element(driver, By.CSS_SELECTOR, "textarea.ace_text-input")
        
        # Вставка данных
        print("📋 Вставка данных JSON...")
        actions = ActionChains(driver)
        actions.move_to_element(editor).click().perform()
        time.sleep(1)
        
        # Ctrl+A (выделить всё) и удалить
        actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
        actions.send_keys(Keys.DELETE).perform()
        time.sleep(1)
        
        # Вставка новых данных
        editor.send_keys(MOON_JSON)
        time.sleep(2)
        
        # Ctrl+S (сохранить)
        actions.key_down(Keys.CONTROL).send_keys('s').key_up(Keys.CONTROL).perform()
        time.sleep(3)
        driver.switch_to.default_content()
        print("✅ Файл moon_data.json сохранен")

        # 3. Работа с консолью
        print("🖥️ Подготовка консоли...")
        driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/consoles/")
        time.sleep(3)
        
        # Закрытие старых консолей
        close_buttons = driver.find_elements(By.CSS_SELECTOR, 'span.glyphicon-remove')
        for btn in close_buttons:
            try:
                btn.click()
                time.sleep(1)
            except:
                pass

        # Открытие новой консоли
        print("🆕 Создание новой bash консоли...")
        driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/files/home/{USERNAME}")
        time.sleep(2)
        open_link = driver.find_element(By.CSS_SELECTOR, f'a[href="/user/{USERNAME}/consoles/bash//home/{USERNAME}/new"]')
        open_link.click()
        time.sleep(15)  # Долгая загрузка консоли

        # Выполнение команды
        print("⚡ Запуск обработчика данных...")
        driver.switch_to.frame(driver.find_element(By.ID, "id_console"))
        time.sleep(5)
        
        body = driver.find_element(By.TAG_NAME, "body")
        actions = ActionChains(driver)
        actions.move_to_element(body).click().perform()
        time.sleep(1)
        
        # Ввод команды с несколькими попытками
        for attempt in range(3):
            try:
                body.send_keys(Keys.CONTROL + 'a')
                body.send_keys(Keys.DELETE)
                time.sleep(1)
                body.send_keys('python3 pythonanywhere_starter.py')
                time.sleep(1)
                body.send_keys(Keys.ENTER)
                time.sleep(1)
                break
            except:
                time.sleep(2)
        
        print("⏳ Ожидание обработки данных (20 секунд)...")
        time.sleep(20)
        driver.switch_to.default_content()
        print("✅ Скрипт выполнен")

        # 4. Получение обработанных данных
        print("📖 Открытие обработанного файла...")
        driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/files/home/{USERNAME}/moon_data_processed.json?edit")
        time.sleep(5)
        
        # Переключение на iframe редактора
        iframe = wait_for_element(driver, By.ID, "id_file_editor_iframe")
        driver.switch_to.frame(iframe)
        time.sleep(3)
        
        # Получение содержимого через Ace Editor
        print("📋 Получение обработанных данных...")
        processed_content = driver.execute_script("""
            try {
                var editor = ace.edit(document.querySelector('.ace_editor'));
                return editor.getValue();
            } catch(e) {
                return '';
            }
        """)
        
        if not processed_content:
            # Альтернативный способ через textarea
            editor = driver.find_element(By.CSS_SELECTOR, "textarea.ace_text-input")
            processed_content = editor.get_attribute('value')
        
        driver.switch_to.default_content()
        
        if not processed_content:
            raise Exception("Не удалось получить содержимое обработанного файла")

        # 5. Сохранение результата для GitHub Actions
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
