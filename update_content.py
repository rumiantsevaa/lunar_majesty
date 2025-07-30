import json
import re
from datetime import datetime

# Читаем JSON данные
with open('./artifacts/moon_data_processed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Извлекаем данные
moon_today_data = data['moon_today']['moon_today']
moon_today = f"{moon_today_data['current_time']}\n🌙 Phase: {moon_today_data['moon_phase_tonight']}\nNew Moon: {moon_today_data['new_moon']}\nFirst Quarter: {moon_today_data['first_quarter']}"

moon_dream = data['moon_dream']['moon_dream']['time_translated']

inspiration_data = data['inspiration']['inspiration']
inspiration = f"{inspiration_data['content']}\n\n— {inspiration_data['author']}"

# Создаем JavaScript контент
js_content = f'''const cards = [
  {{
    title: "Moon today",
    content: {json.dumps(moon_today)}
  }},
  {{
    title: "Moon Phase Dream Dictionary", 
    content: {json.dumps(moon_dream)}
  }},
  {{
    title: "Daily inspiration",
    content: {json.dumps(inspiration)}
  }}
];

let currentIndex = 0;

function updateCard() {{
  const titleElement = document.getElementById("card-title");
  const contentElement = document.getElementById("card-content");
  
  if (titleElement && contentElement && cards[currentIndex]) {{
    titleElement.textContent = cards[currentIndex].title;
    contentElement.innerHTML = cards[currentIndex].content.replace(/\\n/g, '<br>');
    
    const card = document.getElementById("carousel-card");
    card.style.opacity = '0.7';
    setTimeout(() => {{
      card.style.opacity = '1';
    }}, 200);
  }}
}}

function nextCard() {{
  currentIndex = (currentIndex + 1) % cards.length;
  updateCard();
}}

function prevCard() {{
  currentIndex = (currentIndex - 1 + cards.length) % cards.length;
  updateCard();
}}

document.addEventListener('DOMContentLoaded', function() {{
  updateCard();
  
  document.addEventListener('keydown', function(event) {{
    if (event.key === 'ArrowLeft') {{
      prevCard();
    }} else if (event.key === 'ArrowRight') {{
      nextCard();
    }}
  }});
}});'''

# Записываем JavaScript файл
with open('js/lunar_majesty.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

# Обновляем HTML с timestamp
timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
with open('index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

html_content = re.sub(r'<title>Lunar Majesty.*?</title>', f'<title>Lunar Majesty - Updated {timestamp}</title>', html_content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ Files updated successfully")
