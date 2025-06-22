import sqlite3
from datetime import datetime

def create_database():
    conn = sqlite3.connect('genshin.db')
    c = conn.cursor()
    
    # Таблица заметок
    c.execute(''' CREATE TABLE IF NOT EXISTS notes ( id INTEGER PRIMARY KEY, title TEXT, content TEXT, date_created TEXT, type TEXT DEFAULT 'note' ) ''')
    
    # Таблица персонажей
    c.execute(''' CREATE TABLE IF NOT EXISTS characters ( id INTEGER PRIMARY KEY, name TEXT UNIQUE, info TEXT ) ''')
    
    conn.commit()
    conn.close()

def save_note(title, content, note_type="note"):
    conn = sqlite3.connect('genshin.db')
    c = conn.cursor()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO notes (title, content, date_created, type) VALUES (?, ?, ?, ?)",
              (title, content, current_time, note_type))
    conn.commit()
    conn.close()

def get_all_notes():
    conn = sqlite3.connect('genshin.db')
    c = conn.cursor()
    c.execute("SELECT * FROM notes ORDER BY date_created DESC")
    return c.fetchall()

# Инициализация базы данных
create_database()