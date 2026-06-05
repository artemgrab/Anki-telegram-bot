import sqlite3

def init_db():
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            word TEXT,
            translation TEXT,
            example TEXT,
            audio_url TEXT,
            is_exported INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def word_exists(user_id, word):
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM flashcards WHERE user_id = ? AND word = ?', (user_id, word))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def add_word(user_id, word, translation, example, audio_url):
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO flashcards (user_id, word, translation, example, audio_url)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, word, translation, example, audio_url))
    conn.commit()
    conn.close()

def get_unexported_words(user_id):
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.execute('SELECT word, translation, example, audio_url FROM flashcards WHERE user_id = ? AND is_exported = 0', (user_id,))
    words = cursor.fetchall()
    conn.close()
    return words

def mark_as_exported(user_id):
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE flashcards SET is_exported = 1 WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()