from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def moon_today_description(driver):
    url = "https://www.timeanddate.com/moon/phases/ukraine/kyiv"
    driver.get(url)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table.table--inner-borders-rows"))
    )

    current_time = driver.find_element(By.ID, "smct").text
    moon_phase = driver.find_element(By.XPATH, "//th[contains(text(), 'Moon Phase Tonight:')]/following-sibling::td").text
    next_phase = driver.find_element(By.XPATH, "//th[contains(text(), 'First Quarter:')]/following-sibling::td").text
    prev_phase = driver.find_element(By.XPATH, "//th[contains(text(), 'New Moon:')]/following-sibling::td").text

    return {
        "current_time": current_time,
        "moon_phase_tonight": moon_phase,
        "next_phase": next_phase,
        "previous_phase": prev_phase,
    }


def moon_dream_dictionary(driver):
    url = "https://rivendel.ru/dream_lenta.php"
    driver.get(url)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "img[src='greensn.gif']"))
    )

    img = driver.find_element(By.CSS_SELECTOR, "img[src='greensn.gif']")
    dream_meaning = img.find_element(By.XPATH, "./following::td[1]").text
    return dream_meaning


def day_inspiration(driver):
    url = "https://www.greatday.com/"
    driver.get(url)
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "messageBox")))

    date = driver.find_element(By.CSS_SELECTOR, "#messageBox h3").text
    title = driver.find_element(By.CSS_SELECTOR, "#messageBox h1").text
    paragraphs = driver.find_elements(By.CSS_SELECTOR, "#messageBox p.maintext")

    main_texts = [p.text for p in paragraphs[:-1]]
    author = paragraphs[-1].text if paragraphs else ""

    return {
        "date": date,
        "title": title,
        "text": "\n".join(main_texts),
        "author": author,
    }


def main():
    driver = None
    try:
        driver = setup_driver()
        moon = moon_today_description(driver)
        dream = moon_dream_dictionary(driver)
        inspiration = day_inspiration(driver)

        print("=== Moon Today ===")
        print(f"Current Time: {moon['current_time']}")
        print(f"Moon Phase Tonight: {moon['moon_phase_tonight']}")
        print(f"Next Phase: {moon['next_phase']}")
        print(f"Previous Phase: {moon['previous_phase']}")
        print()

        print("=== Moon Phase Dream Dictionary ===")
        print(dream)
        print()

        print("=== Daily Inspiration ===")
        print(inspiration["date"])
        print(inspiration["title"])
        print(inspiration["text"])
        print(inspiration["author"])

    except Exception as e:
        print(f"Fatal error: {str(e)}")
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    main()

