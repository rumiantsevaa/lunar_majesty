import json
import sys
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def moon_today_description(driver):
    driver.get("https://www.timeanddate.com/moon/phases/ukraine/kyiv")
    table_rows = driver.find_elements(By.CSS_SELECTOR, "table.table--left tr")
    data = {}
    for row in table_rows:
        try:
            key = row.find_element(By.TAG_NAME, "th").text.strip()
            value = row.find_element(By.TAG_NAME, "td").text.strip()
            data[key] = value
        except:
            continue
    return {
        "moon_today": {
            "current_time": data.get("Current Time:", "—"),
            "moon_phase_tonight": data.get("Moon Phase Tonight:", "—"),
            "first_quarter": data.get("First Quarter:", "—"),
            "new_moon": data.get("New Moon:", "—")
        }
    }

def moon_dream_dictionary(driver):
    driver.get("https://rivendel.ru/dream_lenta.php")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    green_img = soup.find("img", {"src": "greensn.gif"})
    if not green_img:
        return {"moon_dream": {"error": "Can't find the checkbox"}}
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

def day_inspiration(driver):
    driver.get("https://www.greatday.com/")
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "messageBox")))
        box = driver.find_element(By.ID, "messageBox")
        date = box.find_element(By.TAG_NAME, "h3").text.strip()
        title = box.find_element(By.TAG_NAME, "h1").text.strip()
        paragraphs = box.find_elements(By.CSS_SELECTOR, "p.maintext")
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
    except:
        return {"inspiration": {"error": "Can't get the requested data"}}

if __name__ == "__main__":
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-features=VizDisplayCompositor')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-plugins')
    options.add_argument('--disable-background-timer-throttling')
    options.add_argument('--disable-backgrounding-occluded-windows')
    options.add_argument('--disable-renderer-backgrounding')
    options.add_argument('--disable-features=TranslateUI')
    options.add_argument('--disable-ipc-flooding-protection')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36')
    if os.path.exists('/usr/bin/google-chrome-stable'):
        options.binary_location = '/usr/bin/google-chrome-stable'
    chromedriver_path = os.environ.get('CHROMEDRIVER_PATH', '/usr/local/bin/chromedriver')
    driver = None
    try:
        driver = uc.Chrome(
            options=options,
            driver_executable_path=chromedriver_path,
            version_main=139
        )
        driver.set_page_load_timeout(30)
        driver.implicitly_wait(10)
        moon_today_result = moon_today_description(driver)
        moon_dream_result = moon_dream_dictionary(driver)
        inspiration_result = day_inspiration(driver)
        data = {
            **moon_today_result,
            **moon_dream_result,
            **inspiration_result
        }
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except Exception as e:
        error_data = {
            "error": str(e),
            "moon_today": {"error": "Failed to scrape moon data"},
            "moon_dream": {"error": "Failed to scrape dream data"},
            "inspiration": {"error": "Failed to scrape inspiration data"}
        }
        print(json.dumps(error_data, ensure_ascii=False, indent=2))
        sys.exit(1)
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
