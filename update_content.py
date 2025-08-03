import json
import re
from datetime import datetime

print("🔍 Reading JSON data from artifacts...")
with open('./artifacts/moon_data_processed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("📊 JSON data loaded successfully")
print("🌙 Extracting moon data...")

moon_today_data = data['moon_today']['moon_today']
moon_today = f"{moon_today_data['current_time']}\n🌙 Phase: {moon_today_data['moon_phase_tonight']}\nNew Moon: {moon_today_data['new_moon']}\nFirst Quarter: {moon_today_data['first_quarter']}"

# var renamed to dream_interpretation_translated
moon_dream = data['moon_dream']['moon_dream']['dream_interpretation_translated']

inspiration_data = data['inspiration']['inspiration']
inspiration = f"{inspiration_data['content']}\n\n— {inspiration_data['author']}"

print(f"✅ Extracted data:")
print(f"  - Moon today: {moon_today_data['current_time']} - {moon_today_data['moon_phase_tonight']}")
print(f"  - Dream interpretation: {moon_dream[:50]}...")
print(f"  - Inspiration: {inspiration_data['content'][:50]}...")

print("📝 Creating JavaScript content...")

card_images = {
    "Moon today": "img/moon.avif",
    "Moon Phase Dream Dictionary": "img/Boho-Moon.avif", 
    "Daily inspiration": "img/Aesthetic-hands.avif"
}

js_content = f'''const cards = [
  {{
    title: "Moon today",
    content: {json.dumps(moon_today)},
    image: "img/moon.avif"
  }},
  {{
    title: "Moon Phase Dream Dictionary", 
    content: {json.dumps(moon_dream)},
    image: "img/Boho-Moon.avif"
  }},
  {{
    title: "Daily inspiration",
    content: {json.dumps(inspiration)},
    image: "img/Aesthetic-hands.avif"
  }}
];

let currentIndex = 0;

function updateCard() {{
  const titleElement = document.getElementById("card-title");
  const contentElement = document.getElementById("card-content");
  const imageElement = document.getElementById("card-image");
  
  if (titleElement && contentElement && cards[currentIndex]) {{
    titleElement.textContent = cards[currentIndex].title;
    contentElement.innerHTML = cards[currentIndex].content.replace(/\\n/g, '<br>');
    
    if (imageElement && cards[currentIndex].image) {{
      imageElement.src = cards[currentIndex].image;
      imageElement.alt = cards[currentIndex].title;
      imageElement.classList.remove('hidden');
      imageElement.onerror = function() {{
        this.classList.add('hidden');
      }};
    }}
    
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

print("💾 Writing JavaScript file...")
with open('js/lunar_majesty.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("✅ All files updated successfully with up-to-date lunar data!")
