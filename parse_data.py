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

    print("🌕 Moon Today:")
    print(f"Current Time: {data.get('Current Time:', '—')}")
    print(f"Moon Phase Tonight: {data.get('Moon Phase Tonight:', '—')}")
    print(f"First Quarter: {data.get('First Quarter:', '—')}")
    print(f"New Moon: {data.get('New Moon:', '—')}")
    print()


def moon_dream_dictionary(driver):

    driver.get("https://rivendel.ru/dream_lenta.php")
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Найдём тег <img src="greensn.gif">
    green_img = soup.find("img", {"src": "greensn.gif"})
    if not green_img:
        print("🌙 Галочка не найдена.")
        return

    # Переходим к <tr>, в котором находится галочка
    target_tr = green_img.find_parent("tr")
    current_tr = target_tr

    result = []

    # Следующий <tr> — день недели
    current_tr = current_tr.find_next_sibling("tr")
    tds = current_tr.find_all("td")
    if len(tds) == 2:
        date = tds[0].get_text(strip=True).replace("29 июля 2025", "").strip()  # уже будет внутри с img
        weekday = tds[1].get_text(strip=True)
        result.append(weekday)

    # Следующий <tr> — лунный день и фаза
    current_tr = current_tr.find_next_sibling("tr")
    tds = current_tr.find_all("td")
    for td in tds:
        result.append(td.get_text(strip=True))

    # Следующий <tr> — время и знак
    current_tr = current_tr.find_next_sibling("tr")
    tds = current_tr.find_all("td")
    for td in tds:
        alt = td.find("img")["alt"] if td.find("img") else ""
        if alt:
            result.append(alt)
        else:
            result.append(td.get_text(strip=True))

    # Следующий <tr> — толкование
    current_tr = current_tr.find_next_sibling("tr")
    full_text = current_tr.get_text(separator="\n", strip=True)
    result.append(full_text)

    # Вывод
    print("🌙 Moon Dream Dictionary:")
    for item in result:
        print(item)



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
