import json
import sys
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def moon_today_description(driver):
    """Scrapes current moon phase data from timeanddate.com
    Returns structured data including:
    - Current time
    - Moon phase tonight
    - First quarter date
    - New moon date
    """
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
    """Extracts moon-related dream interpretation data from rivendel.ru
    Returns structured dream analysis including:
    - Weekday
    - Moon day and phase
    - Time and zodiac sign
    - Dream interpretation
    """
    driver.get("https://rivendel.ru/dream_lenta.php")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    green_img = soup.find("img", {"src": "greensn.gif"})
    if not green_img:
        return {"moon_dream": {"error": "Can't find the checkbox"}}

    target_tr = green_img.find_parent("tr")
    current_tr = target_tr
    result = []

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
            "time": time_zodiac[0] if len(time_zodiac) > 0 else "",
            "zodiac_sign": time_zodiac[1] if len(time_zodiac) > 1 else "",
            "interpretation": interpretation
        }
    }

def day_inspiration(driver):
    """Fetches daily inspiration quote from greatday.com
    Returns structured data including:
    - Date
    - Title
    - Content
    - Author
    """
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
    options.headless = True
    driver = uc.Chrome(options=options)

    try:
        # Execute all scraping functions and combine results
        data = {
            "moon_today": moon_today_description(driver),
            "moon_dream": moon_dream_dictionary(driver),
            "inspiration": day_inspiration(driver)
        }
        # Output combined data as pretty-printed JSON
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except Exception as e:
        # Handle any errors during execution
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    finally:
        # Ensure browser is closed even if errors occur
        driver.quit()
