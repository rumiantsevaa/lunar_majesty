import os
import time
import json
import shutil
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

USERNAME = os.getenv("PA_USERNAME")
PASSWORD = os.getenv("PA_PASSWORD")
MOON_JSON = os.getenv("MOON_JSON")

DOWNLOAD_DIR = os.path.abspath("downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

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

def wait_for_file(filename, timeout=15):
    """Ждём появления файла и завершения скачивания (.crdownload)"""
    for _ in range(timeout * 2):
        if os.path.exists(filename) and not filename.endswith(".crdownload"):
            # Проверяем, что файл не временный (не загружается)
            if not any(fname.startswith(filename) and fname.endswith(".crdownload") for fname in os.listdir(DOWNLOAD_DIR)):
                return True
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
    # Настройки скачивания, чтобы не появлялся диалог
    prefs = {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }
    options.add_experimental_option("prefs", prefs)

    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
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
        
        # Находим активный элемент (редактор уже в фокусе)
        active_element = driver.switch_to.active_element
        
        # Выделить всё и удалить
        print("📋 Очистка редактора...")
        ActionChains(driver)\
            .key_down(Keys.CONTROL)\
            .send_keys('a')\
            .key_up(Keys.CONTROL)\
            .perform()
        time.sleep(1)
        active_element.send_keys(Keys.DELETE)
        time.sleep(1)
        
        # Вставка новых данных
        print("📋 Вставка данных JSON...")
        for chunk in [MOON_JSON[i:i+100] for i in range(0, len(MOON_JSON), 100)]:
            active_element.send_keys(chunk)
            time.sleep(0.1)
        time.sleep(2)
        
        # Сохранение файла
        print("💾 Сохранение файла...")
        ActionChains(driver)\
            .key_down(Keys.CONTROL)\
            .send_keys('s')\
            .key_up(Keys.CONTROL)\
            .perform()
        time.sleep(3)
        print("✅ Файл moon_data.json сохранен")

        # 3. Работа с консолью (устойчивый метод)
        print("🖥️ Открытие консоли...")
        driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/consoles/")
        time.sleep(3)

        # Закрыть старые консоли
        close_buttons = driver.find_elements(By.CSS_SELECTOR, 'span.glyphicon-remove')
        for btn in close_buttons:
            try:
                btn.click()
                time.sleep(1)
            except:
                pass

        # Вернуться в файловый менеджер
        driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/files/home/{USERNAME}")
        time.sleep(2)

        # Клик по ссылке на запуск консоли
        print("🚪 Запуск новой bash-консоли...")
        open_link = driver.find_element(By.CSS_SELECTOR, f'a[href="/user/{USERNAME}/consoles/bash//home/{USERNAME}/new"]')
        open_link.click()
        time.sleep(10)

        # Переключение на iframe консоли
        print("📺 Переключение на iframe консоли...")
        driver.switch_to.frame(driver.find_element(By.ID, "id_console"))
        time.sleep(5)

        # Ввод команды
        console_body = driver.find_element(By.TAG_NAME, "body")
        actions = ActionChains(driver)
        actions.move_to_element(console_body).click()
        actions.send_keys('python3 pythonanywhere_starter.py')
        actions.send_keys(Keys.ENTER)
        actions.perform()
        print("✅ Команда отправлена")
        time.sleep(20)

        # Возврат в основной контекст
        driver.switch_to.default_content()

        # 4. Получение обработанных данных через скачивание
        print("📖 Открытие страницы файлов для скачивания обработанного файла...")
        driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/files/home/{USERNAME}")
        time.sleep(5)

        print("⬇️ Кликаем по ссылке скачивания moon_data_processed.json")
        download_link = driver.find_element(By.CSS_SELECTOR, 'a.download_link[href$="moon_data_processed.json"]')
        download_link.click()

        # Ждём появления файла в папке загрузок
        local_filename = os.path.join(DOWNLOAD_DIR, "moon_data_processed.json")
        print(f"⏳ Ждём скачивания файла: {local_filename} ...")
        if not wait_for_file(local_filename):
            raise Exception("Файл moon_data_processed.json не скачался за отведённое время")

        # Читаем скачанный файл
        print("📋 Читаем скачанный файл...")
        with open(local_filename, "r", encoding="utf-8") as f:
            processed_content = f.read()

        print(f"✅ Файл moon_data_processed.json прочитан ({len(processed_content)} символов)")
        print(f"📝 Предварительный просмотр: {processed_content[:200]}...")

        # Перемещаем файл в рабочую директорию, чтобы GitHub Actions его увидел
        dest_path = os.path.join(os.getcwd(), "moon_data_processed.json")
        shutil.copy(local_filename, dest_path)
        print(f"✅ Файл скопирован в рабочую директорию: {dest_path}")
        
    except Exception as e:
        print(f"❌ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("🔚 Закрытие браузера...")
        driver.quit()

if __name__ == "__main__":
    run()
