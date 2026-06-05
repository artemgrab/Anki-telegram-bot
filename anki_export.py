import genanki
import random

def generate_deck(words_data, filename="my_new_words.apkg"):
    model_id = random.randrange(1 << 30, 1 << 31)
    deck_id = random.randrange(1 << 30, 1 << 31)

    my_model = genanki.Model(
      model_id,
      'Minimalist Bot Model',
      fields=[
        {'name': 'Word'},
        {'name': 'BackData'},
      ],
      templates=[
        {
          'name': 'Card 1',
          'qfmt': '<h2 style="text-align:center; font-family: sans-serif;">{{Word}}</h2>',
          'afmt': '{{FrontSide}}<hr id="answer"><div style="font-family: sans-serif; text-align:center;">{{BackData}}</div>',
        },
      ])

    my_deck = genanki.Deck(deck_id, 'Telegram English Vocabulary')

    for word, translation, example, audio in words_data:
        back_content = f"<b>Переклад:</b> {translation}<br><br><b>Приклад:</b> <i>{example}</i>"
        if audio:
            back_content += f"<br><br><a href='{audio}'>🎧 Слухати вимову</a>"

        note = genanki.Note(
            model=my_model,
            fields=[word, back_content]
        )
        my_deck.add_note(note)

    genanki.Package(my_deck).write_to_file(filename)
    return filename