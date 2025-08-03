import json
import sys
import time
import traceback
from functools import wraps
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup

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
                    wait_time = delay * (2 ** attempt)  # Exponential backoff
                    print(f"❌ Attempt {attempt + 1} failed: {str(e)}")
                    if attempt < max_retries - 1:
                        print(f"⏳ Waiting {wait_time}s before retry...")
                        time.sleep(wait_time)
                    else:
                        print(f"💥 All {max_retries} attempts failed")
            
            # If all retries failed, raise the last exception
            raise last_exception
        return wrapper
    return decorator

@retry_on_failure(max_retries=3, delay=3)
def moon_today_description(driver):
    """Scrapes current moon phase data from timeanddate.com with retry logic"""
    try:
        print("🌙 Loading timeanddate.com...")
        driver.set_page_load_timeout(15)
        driver.get("https://www.timeanddate.com/moon/phases/ukraine/kyiv")
        
        # Wait for table to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.table--left tr"))
        )
        
        table_rows = driver.find_elements(By.CSS_SELECTOR, "table.table--left tr")
        
        data = {}
        for row in table_rows:
            try:
                key = row.find_element(By.TAG_NAME, "th").text.strip()
                value = row.find_element(By.TAG_NAME, "td").text.strip()
                data[key] = value
            except:
                continue
                
        if not data:
            raise Exception("No moon data found in table")
            
        return {
            "moon_today": {
                "current_time": data.get("Current Time:", "—"),
                "moon_phase_tonight": data.get("Moon Phase Tonight:", "—"),
                "first_quarter": data.get("First Quarter:", "—"),
                "new_moon": data.get("New Moon:", "—")
            }
        }
    except TimeoutException:
        raise Exception("Timeout loading moon phase data")
    except Exception as e:
        raise Exception(f"Failed to get moon data: {str(e)}")

@retry_on_failure(max_retries=3, delay=3)
def moon_dream_dictionary(driver):
    """Extracts moon-related dream interpretation data with retry logic"""
    try:
        print("🔮 Loading rivendel.ru...")
        driver.set_page_load_timeout(15)
        driver.get("https://rivendel.ru/dream_lenta.php")
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "img"))
        )
        
        soup = BeautifulSoup(driver.page_source, "html.parser")

        green_img = soup.find("img", {"src": "greensn.gif"})
        if not green_img:
            raise Exception("Can't find the green checkbox image")

        target_tr = green_img.find_parent("tr")
        current_tr = target_tr

        current_tr = current_tr.find_next_sibling("tr")
        tds = current_tr.find_all("td")
        weekday = ""
        if len(tds) == 2:
            weekday = tds[1].get_text(strip=True)

        current_tr = current_tr.find_next_sibling("tr")
        moon_day_phase = [td.get_text(strip=True) for td in current_tr.find_all("td")]

        current_tr = current_tr.find_next_sibling("tr")
        time_zodiac = []
        for td in current_tr.find_all("td"):
            alt = td.find("img")["alt"] if td.find("img") else ""
            if alt:
                time_zodiac.append(alt)
            else:
                time_zodiac.append(td.get_text(strip=True))

        current_tr = current_tr.find_next_sibling("tr")
        interpretation = current_tr.get_text(separator="\n", strip=True)

        return {
            "moon_dream": {
                "weekday": weekday,
                "moon_day": moon_day_phase[0] if len(moon_day_phase) > 0 else "",
                "moon_phase": moon_day_phase[1] if len(moon_day_phase) > 1 else "",
                "dream_interpretation": time_zodiac[0] if len(time_zodiac) > 0 else ""
            }
        }
    except TimeoutException:
        raise Exception("Timeout loading dream dictionary")
    except Exception as e:
        raise Exception(f"Failed to get dream data: {str(e)}")

@retry_on_failure(max_retries=3, delay=3)
def day_inspiration(driver):
    """Fetches daily inspiration quote with retry logic"""
    try:
        print("✨ Loading greatday.com...")
        driver.set_page_load_timeout(15)
        driver.get("https://www.greatday.com/")
        
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "messageBox"))
        )
        
        box = driver.find_element(By.ID, "messageBox")
        date = box.find_element(By.TAG_NAME, "h3").text.strip()
        title = box.find_element(By.TAG_NAME, "h1").text.strip()
        paragraphs = box.find_elements(By.CSS_SELECTOR, "p.maintext")
        
        if not paragraphs:
            raise Exception("No inspiration content found")
            
        content = "\n\n".join(p.text.strip() for p in paragraphs[:-1])
        author = paragraphs[-1].text.strip()

        return {
            "inspiration": {
                "date": date,
                "title": title,
                "content": content,
                "author": author
            }
        }
    except TimeoutException:
        raise Exception("Timeout loading inspiration")
    except Exception as e:
        raise Exception(f"Failed to get inspiration: {str(e)}")

def create_robust_driver():
    """Create Chrome driver with robust settings"""
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    driver = uc.Chrome(options=options)
    driver.set_page_load_timeout(20)
    driver.implicitly_wait(10)
    return driver

if __name__ == "__main__":
    driver = None
    try:
        print("🚀 Starting robust moon data parser...")
        driver = create_robust_driver()

        # Execute all scraping functions with individual retry logic
        print("📊 Collecting all moon data...")
        data = {}
        
        # Each function has its own retry mechanism
        data["moon_today"] = moon_today_description(driver)
        data["moon_dream"] = moon_dream_dictionary(driver)
        data["inspiration"] = day_inspiration(driver)
        
        print("✅ All data collected successfully!")
        print(json.dumps(data, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"💥 Fatal error after all retries: {str(e)}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)
    finally:
        if driver:
            print("🔚 Closing browser...")
            driver.quit()
