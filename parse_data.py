import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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

    print("🌕 Moon Today:")
    print(f"Current Time: {data.get('Current Time:', '—')}")
    print(f"Moon Phase Tonight: {data.get('Moon Phase Tonight:', '—')}")
    print(f"First Quarter: {data.get('First Quarter:', '—')}")
    print(f"New Moon: {data.get('New Moon:', '—')}")
    print()


def moon_dream_dictionary(driver):
    driver.get("https://rivendel.ru/dream_lenta.php")
    try:
        all_tds = driver.find_elements(By.TAG_NAME, "td")

        target_index = None
        for i, td in enumerate(all_tds):
            if td.find_elements(By.XPATH, ".//img[@src='greensn.gif']"):
                target_index = i
                break

        if target_index is not None:
            following_tds = all_tds[target_index + 1 : target_index + 5]
            print("🌙 Moon Dream Dictionary:")
            for td in following_tds:
                print(td.text.strip())
        else:
            print("🌙 Moon Dream Dictionary: галочка не найдена.")
    except Exception as e:
        print("🌙 Moon Dream Dictionary: ошибка.")
        print(str(e))
    print()



def day_inspiration(driver):
    driver.get("https://www.greatday.com/")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "messageBox"))
        )
        box = driver.find_element(By.ID, "messageBox")
        date = box.find_element(By.TAG_NAME, "h3").text.strip()
        title = box.find_element(By.TAG_NAME, "h1").text.strip()
        paragraphs = box.find_elements(By.CSS_SELECTOR, "p.maintext")
        content = "\n\n".join(p.text.strip() for p in paragraphs[:-1])
        author = paragraphs[-1].text.strip()

        print("☀️ Daily Inspiration:")
        print(f"{date} — {title}")
        print(content)
        print(author)
    except:
        print("☀️ Daily Inspiration: не удалось получить данные.")
    print()


if __name__ == "__main__":
    options = uc.ChromeOptions()
    options.headless = True
    driver = uc.Chrome(options=options)

    try:
        moon_today_description(driver)
        moon_dream_dictionary(driver)
        day_inspiration(driver)
    finally:
        driver.quit()
