from bs4 import BeautifulSoup
import requests


def moon_today_description():
    url = "https://www.timeanddate.com/moon/phases/ukraine/kyiv"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    data = {}

    rows = soup.select("table.table--left tr")
    for row in rows:
        header = row.select_one("th")
        value = row.select_one("td")
        if header and value:
            key = header.get_text(strip=True)
            val = value.get_text(strip=True)
            data[key] = val

    print("🌕 Moon Today:")
    print(f"Current Time: {data.get('Current Time:')}")
    print(f"Moon Phase Tonight: {data.get('Moon Phase Tonight:')}")
    print(f"First Quarter: {data.get('First Quarter:')}")
    print(f"New Moon: {data.get('New Moon:')}")
    print()


def moon_dream_dictionary():
    url = "https://rivendel.ru/dream_lenta.php"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    green_img = soup.find("img", {"src": "greensn.gif"})
    if not green_img:
        print("🌙 Moon Dream Dictionary: элемент с иконкой greensn.gif не найден.")
        return

    dream_td = green_img.find_next("td", {"width": "100%"})
    if dream_td:
        print("🌙 Moon Dream Dictionary:")
        print(dream_td.get_text(strip=True, separator="\n"))
    else:
        print("🌙 Moon Dream Dictionary: текст после иконки не найден.")
    print()


def day_inspiration():
    url = "https://www.greatday.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    box = soup.select_one("div#messageBox")
    if not box:
        print("☀️ Daily Inspiration: блок messageBox не найден.")
        return

    date = box.find("h3").text.strip()
    title = box.find("h1").text.strip()
    paragraphs = box.select("p.maintext")
    content = "\n\n".join(p.text.strip() for p in paragraphs[:-1])
    author = paragraphs[-1].text.strip()

    print("☀️ Daily Inspiration:")
    print(f"{date} — {title}")
    print(content)
    print(author)
    print()


if __name__ == "__main__":
    moon_today_description()
    moon_dream_dictionary()
    day_inspiration()
