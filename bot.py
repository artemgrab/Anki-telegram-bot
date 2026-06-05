import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from dotenv import load_dotenv

from database import init_db, add_word, get_unexported_words, mark_as_exported, word_exists 
from api_client import fetch_word_data
from anki_export import generate_deck

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Токен бота не знайдено! Перевір файл .env.")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привіт! Відправляй мені слова англійською, а я буду збирати їх у колоду Anki.\nКоли будеш готовий, напиши /export.")

@dp.message(Command("export"))
async def cmd_export(message: types.Message):
    user_id = message.from_user.id
    words = get_unexported_words(user_id)
    
    if not words:
        await message.answer("У тебе немає нових слів для експорту.")
        return

    await message.answer(f"Генерую колоду з {len(words)} слів...")
    
    filename = f"anki_export_{user_id}.apkg"
    generate_deck(words, filename)
    
    document = FSInputFile(filename)
    await bot.send_document(message.chat.id, document)
    
    mark_as_exported(user_id)
    os.remove(filename)

@dp.message()
async def process_word(message: types.Message):
    word = message.text.strip().lower()
    user_id = message.from_user.id
    
    if len(word.split()) > 3:
        await message.answer("Будь ласка, відправляй по одному слову або короткій фразі.")
        return

    # ПЕРЕВІРКА НА ДУБЛІКАТИ
    if word_exists(user_id, word):
        await message.answer(f"⚠️ Слово <b>{word}</b> вже є у твоєму словнику!", parse_mode="HTML")
        return

    await bot.send_chat_action(message.chat.id, 'typing')
    

    data = await fetch_word_data(word)    
    add_word(message.from_user.id, data['word'], data['translation'], data['example'], data['audio_url'])
    
    response_text = (
        f"✅ <b>{data['word']}</b> додано!\n"
        f"🇺🇦 <i>{data['translation']}</i>\n\n"
        f"Відправ /export, щоб завантажити колоду."
    )
    await message.answer(response_text, parse_mode="HTML")

async def main():
    init_db()
    print("Бот запущений...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())