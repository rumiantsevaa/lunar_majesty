import json
import re
from googletrans import Translator

def process_moon_data():
    with open('moon_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    moon_today = data['moon_today']['moon_today']
    for key in ['current_time', 'first_quarter', 'new_moon']:
        if key in moon_today:
            # Cut off the time, leaving only the date
            moon_today[key] = moon_today[key].split(' at ')[0]

    moon_dream = data['moon_dream']['moon_dream']
    # Leave only weekday and dream_interpretation, delete the rest
    keys_to_keep = ['weekday', 'dream_interpretation']
    moon_dream_processed = {k: moon_dream[k] for k in keys_to_keep if k in moon_dream}

    if 'dream_interpretation' in moon_dream_processed:
        text = moon_dream_processed['dream_interpretation']
        # Find the last occurrence of "день" and trim everything before it
        match = re.search(r'день', text)
        if match:
            start_pos = match.end()
            moon_dream_processed['dream_interpretation'] = text[start_pos:].strip()

        translator = Translator()
        try:
            translated = translator.translate(moon_dream_processed['dream_interpretation'], dest='en').text
            moon_dream_processed['dream_interpretation_translated'] = translated
        except Exception as e:
            print(f"Translation error: {e}")
            moon_dream_processed['dream_interpretation_translated'] = "Translation failed"

    inspiration = data['inspiration']['inspiration']
    inspiration_processed = {
        'content': inspiration['content'],
        'author': inspiration['author']
    }

    result = {
        'moon_today': {'moon_today': moon_today},
        'moon_dream': {'moon_dream': moon_dream_processed},
        'inspiration': {'inspiration': inspiration_processed}
    }

    with open('moon_data_processed.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=2)

    print("Processing complete. Result saved in moon_data_processed.json")

if __name__ == "__main__":
    process_moon_data()
