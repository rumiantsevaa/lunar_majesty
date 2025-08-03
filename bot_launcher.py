import os
import time
import json
import shutil
import traceback
from functools import wraps
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, WebDriverException

USERNAME = os.getenv("PA_USERNAME")
PASSWORD = os.getenv("PA_PASSWORD")
MOON_JSON = os.getenv("MOON_JSON")

DOWNLOAD_DIR = os.path.abspath("downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def retry_on_failure(max_retries=3, delay=5):
    """Decorator for retry logic with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    print(f"🔄 Attempt {attempt + 1}/{max_retries} for {func.__name__}")
                    result = func(*args, **kwargs)
                    if attempt > 0:
                        print(f"✅ Success on attempt {attempt + 1}")
                    return result
                except Exception as e:
                    last_exception = e
                    wait_time = delay * (2 ** attempt)
                    print(f"❌ Attempt {attempt + 1} failed: {str(e)}")
                    if attempt < max_retries - 1:
                        print(f"⏳ Waiting {wait_time}s before retry...")
                        time.sleep(wait_time)
                        # Recreate driver for next attempt if it's a WebDriver issue
                        if isinstance(e, (TimeoutException, WebDriverException)):
                            print("🔄 Recreating driver for next attempt...")
                            if 'driver' in kwargs:
                                try:
                                    kwargs['driver'].quit()
                                except:
                                    pass
                                kwargs['driver'] = create_robust_driver()
                    else:
                        print(f"💥 All {max_retries} attempts failed")
            
            raise last_exception
        return wrapper
    return decorator

def create_robust_driver():
    """Create Chrome driver with robust settings"""
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
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-web-security")
    
    driver = uc.Chrome(options=options)
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(10)
    return driver

def wait_and_click(driver, by, value, timeout=10):
    """Wait for element and click it with retries"""
    for _ in range(timeout * 2):
        try:
            element = driver.find_element(by, value)
            element.click()
            return True
        except:
            time.sleep(0.5)
    raise Exception(f"Could not click element {by}={value}")

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
    raise Exception(f"Could not type into element {by}={value}")

def wait_for_file(filename, timeout=30):
    """Wait for file to appear and finish downloading"""
    print(f"⏳ Waiting up to {timeout}s for file: {filename}")
    for i in range(timeout * 2):
        if os.path.exists(filename) and not filename.endswith(".crdownload"):
            if not any(fname.startswith(os.path.basename(filename)) and fname.endswith(".crdownload") 
                      for fname in os.listdir(DOWNLOAD_DIR)):
                print(f"✅ File found after {i*0.5}s")
                return True
        time.sleep(0.5)
    raise Exception(f"File {filename} didn't download in {timeout}s")

@retry_on_failure(max_retries=3, delay=5)
def login_to_pythonanywhere(driver):
    """Login to PythonAnywhere with retry logic"""
    print("🔐 Logging into PythonAnywhere...")
    driver.get("https://www.pythonanywhere.com/login/")
    wait_and_type(driver, By.ID, "id_auth-username", USERNAME)
    wait_and_type(driver, By.ID, "id_auth-password", PASSWORD)
    wait_and_click(driver, By.ID, "id_next")
    time.sleep(5)
    
    # Verify login success
    if "login" in driver.current_url.lower():
        raise Exception("Login failed - still on login page")
    
    print("✅ Login successful")

@retry_on_failure(max_retries=3, delay=5)  
def upload_json_data(driver):
    """Upload JSON data to remote file with retry logic"""
    print("📝 Opening moon_data.json for editing...")
    driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/files/home/{USERNAME}/moon_data.json?edit")
    time.sleep(8)
    
    active_element = driver.switch_to.active_element
    
    print("📋 Clearing editor...")
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
    time.sleep(1)
    active_element.send_keys(Keys.DELETE)
    time.sleep(1)
    
    print("📋 Inserting JSON data...")
    # Insert data in smaller chunks to avoid timeouts
    chunk_size = 50
    for i in range(0, len(MOON_JSON), chunk_size):
        chunk = MOON_JSON[i:i+chunk_size]
        active_element.send_keys(chunk)
        time.sleep(0.05)
    
    time.sleep(2)
    
    print("💾 Saving file...")
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('s').key_up(Keys.CONTROL).perform()
    time.sleep(5)
    
    print("✅ File moon_data.json saved")

@retry_on_failure(max_retries=3, delay=5)
def process_data_in_console(driver):
    """Process data in console with retry logic"""
    print("🖥️ Opening console...")
    driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/consoles/")
    time.sleep(5)

    # Close old consoles
    close_buttons = driver.find_elements(By.CSS_SELECTOR, 'span.glyphicon-remove')
    for btn in close_buttons:
        try:
            btn.click()
            time.sleep(1)
        except:
            pass

    driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/files/home/{USERNAME}")
    time.sleep(3)

    print("🚪 Starting new bash console...")
    open_link = driver.find_element(By.CSS_SELECTOR, f'a[href="/user/{USERNAME}/consoles/bash//home/{USERNAME}/new"]')
    open_link.click()
    time.sleep(15)

    print("📺 Switching to console iframe...")
    driver.switch_to.frame(driver.find_element(By.ID, "id_console"))
    time.sleep(8)

    console_body = driver.find_element(By.TAG_NAME, "body")
    actions = ActionChains(driver)
    actions.move_to_element(console_body).click()
    actions.send_keys('python3 pythonanywhere_starter.py')
    actions.send_keys(Keys.ENTER)
    actions.perform()
    print("✅ Processing command sent")
    time.sleep(25)  # Increased wait time

    driver.switch_to.default_content()

@retry_on_failure(max_retries=3, delay=5)
def download_processed_file(driver):
    """Download processed file with retry logic"""
    print("📖 Opening files page...")
    driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/files/home/{USERNAME}")
    time.sleep(8)

    print("⬇️ Clicking download link...")
    download_link = driver.find_element(By.CSS_SELECTOR, 'a.download_link[href$="moon_data_processed.json"]')
    download_link.click()

    local_filename = os.path.join(DOWNLOAD_DIR, "moon_data_processed.json")
    wait_for_file(local_filename, timeout=30)

    print("📋 Reading downloaded file...")
    with open(local_filename, "r", encoding="utf-8") as f:
        processed_content = f.read()

    if len(processed_content) < 100:  # Sanity check
        raise Exception("Downloaded file seems too small")

    print(f"✅ File read ({len(processed_content)} characters)")
    print(f"📝 Preview: {processed_content[:200]}...")

    dest_path = os.path.join(os.getcwd(), "moon_data_processed.json")
    shutil.copy(local_filename, dest_path)
    print(f"✅ File copied to: {dest_path}")

def run():
    print("🚀 Starting robust PythonAnywhere bot...")
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

    driver = None
    try:
        driver = create_robust_driver()
        
        # Each operation has its own retry logic
        login_to_pythonanywhere(driver)
        upload_json_data(driver)
        process_data_in_console(driver)
        download_processed_file(driver)
        
        print("🎉 All operations completed successfully!")
        
    except Exception as e:
        print(f"💥 Fatal error after all retries: {e}")
        traceback.print_exc()
        raise
    finally:
        if driver:
            print("🔚 Closing browser...")
            try:
                driver.quit()
            except:
                pass

if __name__ == "__main__":
    run()
