import os
import time
import json
import shutil
import subprocess
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service

def clear_uc_cache():
    """Clear undetected_chromedriver cache to force local driver"""
    try:
        cache_dirs = [
            os.path.expanduser("~/.undetected_chromedriver"),
            "/tmp/.com.google.Chrome",
            "/tmp/undetected_chromedriver"
        ]
        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir, ignore_errors=True)
                print(f"🧹 Cleared cache: {cache_dir}")
    except Exception as e:
        print(f"⚠️ Cache clear warning: {e}")

USERNAME = os.getenv("PA_USERNAME")
PASSWORD = os.getenv("PA_PASSWORD")
MOON_JSON = os.getenv("MOON_JSON")

DOWNLOAD_DIR = os.path.abspath("downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def wait_and_click(driver, by, value, timeout=10):
    """Wait for element and click it with retries"""
    for _ in range(timeout * 2):
        try:
            element = driver.find_element(by, value)
            element.click()
            return True
        except:
            time.sleep(0.5)
    return False

def wait_and_type(driver, by, value, text, timeout=10):
    """Wait for input field and type text with retries"""
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
    """Wait for file to appear and finish downloading (check for .crdownload)"""
    for _ in range(timeout * 2):
        if os.path.exists(filename) and not filename.endswith(".crdownload"):
            if not any(fname.startswith(filename) and fname.endswith(".crdownload") for fname in os.listdir(DOWNLOAD_DIR)):
                return True
        time.sleep(0.5)
    return False

def run():
    print("🚀 Initialization...")
    print(f"📋 Username: {USERNAME}")
    print(f"🌙 Moon data available: {'Yes' if MOON_JSON else 'No'}")
    
    if not USERNAME or not PASSWORD:
        print("❌ ERROR: PA_USERNAME or PA_PASSWORD not set")
        return
    
    if not MOON_JSON:
        print("❌ ERROR: MOON_JSON data not found")
        return
    
    try:
        moon_data = json.loads(MOON_JSON)
        print(f"✅ Moon data loaded: {len(moon_data)} sections")
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing ERROR: {e}")
        return

    clear_uc_cache()

    subprocess.run(['pkill', '-9', '-f', 'chrome'], capture_output=True)
    subprocess.run(['pkill', '-9', '-f', 'google-chrome'], capture_output=True)

    chromedriver_path = os.path.abspath("./matching_chrome_driver/chromedriver")
    if not os.path.exists(chromedriver_path):
        raise FileNotFoundError(f"ChromeDriver not found at {chromedriver_path}")
    
    try:
        result = subprocess.run([chromedriver_path, '--version'], capture_output=True, text=True)
        chromedriver_version = result.stdout.strip()
        chromedriver_major = chromedriver_version.split()[1].split('.')[0]
        print(f"🔍 ChromeDriver version: {chromedriver_version}")
        
        result = subprocess.run(['google-chrome', '--version'], capture_output=True, text=True)
        chrome_version = result.stdout.strip()
        chrome_major = chrome_version.split()[-1].split('.')[0]
        print(f"🔍 Chrome version: {chrome_version}")
        print(f"🔍 ChromeDriver major: {chromedriver_major}, Chrome major: {chrome_major}")
        
        if chromedriver_major != chrome_major:
            print(f"⚠️ Version mismatch detected!")
            subprocess.run(['pkill', '-f', 'chrome'], capture_output=True)
            subprocess.run(['pkill', '-f', 'google-chrome'], capture_output=True)
            time.sleep(2)
    except Exception as e:
        print(f"⚠️ Version check failed: {e}")

    options = uc.ChromeOptions()
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
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--disable-extensions")

    print("🌐 Starting Chrome...")
    print(f"🔧 Using ChromeDriver: {chromedriver_path}")
    
    try:
        driver = uc.Chrome(
            options=options,
            driver_executable_path=chromedriver_path,
            version_main=139,
        )
        print("✅ undetected_chromedriver created successfully")
        print("📡 Connected browser version:", driver.capabilities.get("browserVersion", "unknown"))
    except Exception as e:
        print(f"❌ Failed to create driver with undetected_chromedriver: {e}")
        print("🔄 Trying fallback method with regular Selenium...")
        try:
            from selenium import webdriver
            service = Service(executable_path=chromedriver_path)
            driver = webdriver.Chrome(service=service, options=options)
            print("✅ Regular Selenium driver created successfully")
        except Exception as e2:
            print(f"❌ Regular Selenium also failed: {e2}")
            raise Exception("Could not create Chrome driver with any method")

    try:
        print(f"✅ Chrome started successfully")

        print("🔐 Logging into PythonAnywhere...")
        driver.get("https://www.pythonanywhere.com/login/")
        wait_and_type(driver, By.ID, "id_auth-username", USERNAME)
        wait_and_type(driver, By.ID, "id_auth-password", PASSWORD)
        wait_and_click(driver, By.ID, "id_next")
        time.sleep(3)
        print("✅ Login successful")

        print("📝 Opening moon_data.json for editing...")
        driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/files/home/{USERNAME}/moon_data.json?edit")
        time.sleep(5)

        active_element = driver.switch_to.active_element
        print("📋 Clearing editor...")
        ActionChains(driver)\
            .key_down(Keys.CONTROL)\
            .send_keys('a')\
            .key_up(Keys.CONTROL)\
            .perform()
        time.sleep(1)
        active_element.send_keys(Keys.DELETE)
        time.sleep(1)

        print("📋 Inserting JSON data...")
        for chunk in [MOON_JSON[i:i+100] for i in range(0, len(MOON_JSON), 100)]:
            active_element.send_keys(chunk)
            time.sleep(0.1)
        time.sleep(2)

        print("💾 Saving file...")
        ActionChains(driver)\
            .key_down(Keys.CONTROL)\
            .send_keys('s')\
            .key_up(Keys.CONTROL)\
            .perform()
        time.sleep(3)
        print("✅ File moon_data.json saved")

        print("🖥️ Opening console...")
        driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/consoles/")
        time.sleep(3)

        close_buttons = driver.find_elements(By.CSS_SELECTOR, 'span.glyphicon-remove')
        for btn in close_buttons:
            try:
                btn.click()
                time.sleep(1)
            except:
                pass

        driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/files/home/{USERNAME}")
        time.sleep(2)

        print("🚪 Starting new bash console...")
        open_link = driver.find_element(By.CSS_SELECTOR, f'a[href="/user/{USERNAME}/consoles/bash//home/{USERNAME}/new"]')
        open_link.click()
        time.sleep(10)

        print("📺 Переключение на iframe консоли...")
        driver.switch_to.frame(driver.find_element(By.ID, "id_console"))
        time.sleep(5)

        console_body = driver.find_element(By.TAG_NAME, "body")
        actions = ActionChains(driver)
        actions.move_to_element(console_body).click()
        actions.send_keys('python3 pythonanywhere_starter.py')
        actions.send_keys(Keys.ENTER)
        actions.perform()
        print("✅ Command to process transfered data sent")
        time.sleep(20)

        driver.switch_to.default_content()

        print("📖 Opening files page to download processed file...")
        driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/files/home/{USERNAME}")
        time.sleep(5)

        print("⬇️ Clicking download link for moon_data_processed.json")
        download_link = driver.find_element(By.CSS_SELECTOR, 'a.download_link[href$="moon_data_processed.json"]')
        download_link.click()

        local_filename = os.path.join(DOWNLOAD_DIR, "moon_data_processed.json")
        print(f"⏳ Waiting for file download: {local_filename} ...")
        if not wait_for_file(local_filename):
            raise Exception("File moon_data_processed.json didn't download in time")

        print("📋 Reading downloaded file...")
        with open(local_filename, "r", encoding="utf-8") as f:
            processed_content = f.read()

        print(f"✅ File moon_data_processed.json read ({len(processed_content)} characters)")
        print(f"📝 Preview: {processed_content[:200]}...")

        dest_path = os.path.join(os.getcwd(), "moon_data_processed.json")
        shutil.copy(local_filename, dest_path)
        print(f"✅ File copied to working directory: {dest_path}")

    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("🔚 Closing browser...")
        driver.quit()
        clear_uc_cache()

if __name__ == "__main__":
    run()
