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
        # Логин
        print("🔐 Выполняется вход в PythonAnywhere...")
        driver.get("https://www.pythonanywhere.com/login/")
        wait_and_type(driver, By.ID, "id_auth-username", USERNAME)
        wait_and_type(driver, By.ID, "id_auth-password", PASSWORD)
        wait_and_click(driver, By.ID, "id_next")
        time.sleep(3)
        print("✅ Вход выполнен")

        # 1. Открытие файла moon_data.json для редактирования
        print("📝 Открытие файла moon_data.json для редактирования...")
        driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/files/home/{USERNAME}/moon_data.json?edit")
        time.sleep(5)
        
        # Отладочная информация о странице
        print(f"🔍 Текущий URL: {driver.current_url}")
        print(f"📄 Заголовок страницы: {driver.title}")
        
        # Проверим, есть ли сообщения об ошибках
        try:
            error_messages = driver.find_elements(By.CSS_SELECTOR, ".alert, .error, .message")
            for msg in error_messages:
                if msg.text.strip():
                    print(f"⚠️ Сообщение на странице: {msg.text.strip()}")
        except:
            pass

        # Поиск и переключение на iframe редактора
        print("🔄 Поиск iframe редактора...")
        time.sleep(5)
        
        # Проверим все доступные iframe
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"📝 Найдено {len(iframes)} iframe на странице")
        
        editor_frame = None
        # Попробуем разные возможные ID/селекторы для iframe
        possible_selectors = [
            (By.ID, "id_file_editor_iframe"),
            (By.ID, "file_editor_iframe"),
            (By.ID, "editor_iframe"),
            (By.CSS_SELECTOR, "iframe[src*='editor']"),
            (By.CSS_SELECTOR, "iframe")
        ]
        
        for by, selector in possible_selectors:
            try:
                editor_frame = driver.find_element(by, selector)
                print(f"✅ Найден iframe с селектором: {selector}")
                break
            except:
                continue
        
        if not editor_frame and iframes:
            # Если не нашли по селекторам, возьмем первый iframe
            editor_frame = iframes[0]
            print("📝 Используем первый доступный iframe")
        
        if not editor_frame:
            raise Exception("Не найден iframe редактора")
            
        driver.switch_to.frame(editor_frame)
        time.sleep(5)

        # Поиск текстового редактора
        print("📋 Поиск текстового редактора...")
        
        # Попробуем разные селекторы для редактора
        editor_selectors = [
            ".ace_text-input",
            ".ace_editor textarea",
            "textarea",
            ".CodeMirror textarea",
            "#id_content"
        ]
        
        editor = None
        for selector in editor_selectors:
            try:
                editor = driver.find_element(By.CSS_SELECTOR, selector)
                print(f"✅ Найден редактор: {selector}")
                break
            except:
                continue
        
        if not editor:
            # Попробуем найти любой input или textarea
            try:
                editor = driver.find_element(By.TAG_NAME, "textarea")
                print("✅ Найден textarea редактор")
            except:
                raise Exception("Не найден текстовый редактор")

        # Очистка содержимого и вставка новых данных
        print("📋 Очистка и вставка данных JSON...")
        
        # Кликаем на редактор и фокусируемся
        actions = ActionChains(driver)
        actions.move_to_element(editor).click()
        actions.perform()
        time.sleep(1)
        
        # Выделяем все содержимое и заменяем
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL)  # Ctrl+A
        actions.send_keys(Keys.DELETE)  # Удаляем выделенное
        actions.send_keys(MOON_JSON)  # Вставляем новые данные
        actions.perform()
        time.sleep(3)

        # Сохранение файла
        print("💾 Сохранение файла (Ctrl+S)...")
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).send_keys('s').key_up(Keys.CONTROL)  # Ctrl+S
        actions.perform()
        time.sleep(3)

        # Возврат к основному окну
        driver.switch_to.default_content()
        print("✅ Файл moon_data.json сохранен")

        # 2. Открытие консоли для запуска скрипта
        print("🖥️ Открытие консоли для запуска скрипта...")
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
        time.sleep(15)

        # Переключение на консоль и выполнение скрипта
        print("⚡ Запуск обработчика данных...")
        driver.switch_to.frame(driver.find_element(By.ID, "id_console"))
        time.sleep(5)
        
        body = driver.find_element(By.TAG_NAME, "body")
        actions = ActionChains(driver)
        actions.move_to_element(body).click()
        actions.send_keys('python3 pythonanywhere_starter.py')
        actions.send_keys(Keys.ENTER)
        actions.perform()
        
        # Ждем выполнения скрипта
        print("⏳ Ожидание обработки данных (60 секунд)...")
        time.sleep(60)

        # Возврат к основному окну
        driver.switch_to.default_content()
        print("✅ Скрипт выполнен")

        # 3. Открытие обработанного файла и извлечение содержимого
        print("📖 Открытие обработанного файла moon_data_processed.json...")
        driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/files/home/{USERNAME}/moon_data_processed.json?edit")
        time.sleep(5)

        # Поиск и переключение на iframe редактора
        print("🔄 Поиск iframe редактора для чтения результата...")
        
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        editor_frame = None
        
        for by, selector in possible_selectors:
            try:
                editor_frame = driver.find_element(by, selector)
                break
            except:
                continue
        
        if not editor_frame and iframes:
            editor_frame = iframes[0]
        
        if not editor_frame:
            raise Exception("Не найден iframe редактора для чтения результата")
            
        driver.switch_to.frame(editor_frame)
        time.sleep(5)

        # Поиск редактора и получение содержимого
        print("📋 Получение обработанных данных...")
        
        # Попробуем получить содержимое разными способами
        processed_content = ""
        
        # Способ 1: Через JavaScript API Ace редактора
        try:
            processed_content = driver.execute_script("""
                try {
                    var editor = ace.edit(document.querySelector('.ace_editor'));
                    return editor.getValue();
                } catch(e) {
                    return '';
                }
            """)
            if processed_content:
                print("✅ Содержимое получено через Ace Editor API")
        except:
            pass
        
        # Способ 2: Через textarea
        if not processed_content:
            try:
                for selector in editor_selectors:
                    try:
                        editor_elem = driver.find_element(By.CSS_SELECTOR, selector)
                        processed_content = editor_elem.get_attribute('value') or editor_elem.text
                        if processed_content:
                            print(f"✅ Содержимое получено через {selector}")
                            break
                    except:
                        continue
            except:
                pass
        
        # Способ 3: Выделение и копирование
        if not processed_content:
            try:
                editor_elem = driver.find_element(By.CSS_SELECTOR, editor_selectors[0])
                actions = ActionChains(driver)
                actions.move_to_element(editor_elem).click()
                actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL)
                actions.perform()
                time.sleep(1)
                
                # Попробуем получить выделенный текст
                processed_content = driver.execute_script("return window.getSelection().toString();")
                if processed_content:
                    print("✅ Содержимое получено через выделение")
            except:
                pass

        if not processed_content:
            raise Exception("Не удалось получить содержимое обработанного файла")

        driver.switch_to.default_content()
        print(f"✅ Получено {len(processed_content)} символов обработанных данных")

        # 4. Сохранение результата в файл для GitHub Actions
        print("💾 Сохранение результата для GitHub Actions...")
        with open('moon_data_processed.json', 'w', encoding='utf-8') as f:
            f.write(processed_content)
        
        print("✅ Файл moon_data_processed.json создан для артефакта")
        
        # Также выводим первые 200 символов для проверки
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
