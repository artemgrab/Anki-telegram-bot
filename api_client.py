import requests
from googletrans import Translator

translator = Translator()

def fetch_word_data(word):
    # Отримуємо англійські дані з Free Dictionary API
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    
    example = "Приклад не знайдено."
    audio_url = ""
    
    if response.status_code == 200:
        data = response.json()[0]
        try:
            # Шукаємо перший доступний приклад
            for meaning in data.get('meanings', []):
                for def_obj in meaning.get('definitions', []):
                    if 'example' in def_obj:
                        example = def_obj['example']
                        break
                if example != "Приклад не знайдено.": break
            
            # Шукаємо аудіо
            for phonetic in data.get('phonetics', []):
                if phonetic.get('audio'):
                    audio_url = phonetic['audio']
                    break
        except Exception as e:
            print(f"Помилка парсингу: {e}")

    # Отримуємо переклад
    try:
        translation = translator.translate(word, src='en', dest='uk').text
    except:
        translation = "Помилка перекладу"

    return {
        "word": word,
        "translation": translation,
        "example": example,
        "audio_url": audio_url
    }