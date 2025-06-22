import sqlite3
from datetime import datetime

def create_database():
    conn = sqlite3.connect('genshin.db')
    c = conn.cursor()
    
    # Таблица заметок
    c.execute(''' CREATE TABLE IF NOT EXISTS notes (
                 id INTEGER PRIMARY KEY,
                 title TEXT,
                 content TEXT,
                 date_created TEXT,
                 type TEXT DEFAULT 'note') ''')
    
    # Таблица персонажей
    c.execute(''' CREATE TABLE IF NOT EXISTS characters (
                 id INTEGER PRIMARY KEY,
                 name TEXT UNIQUE,
                 description TEXT,
                 rarity TEXT,
                 element TEXT,
                 birthday TEXT,
                 constellation TEXT,
                 region TEXT,
                 type_weapon TEXT,
                 recommended_artifacts TEXT,
                 recommended_weapon TEXT) ''')
    
    # Таблица для пунктов списка
    c.execute(''' CREATE TABLE IF NOT EXISTS list_items (
                 id INTEGER PRIMARY KEY,
                 parent_note_id INTEGER,
                 text TEXT,
                 completed BOOLEAN DEFAULT FALSE,
                 FOREIGN KEY(parent_note_id) REFERENCES notes(id)) ''')
    
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

def get_all_characters():
    conn = sqlite3.connect('genshin.db')
    c = conn.cursor()
    c.execute("SELECT * FROM characters")
    results = c.fetchall()
    conn.close()
    return results

# Функции для работы с элементами списка
def mark_completed(item_id, completed):
    conn = sqlite3.connect('genshin.db')
    c = conn.cursor()
    c.execute("UPDATE list_items SET completed=? WHERE id=?", (completed, item_id))
    conn.commit()
    conn.close()

def get_list_items(note_id):
    conn = sqlite3.connect('genshin.db')
    c = conn.cursor()
    c.execute("SELECT id, text, completed FROM list_items WHERE parent_note_id=?", (note_id,))
    results = c.fetchall()
    conn.close()
    return results

def insert_list_item(parent_note_id, text):
    conn = sqlite3.connect('genshin.db')
    c = conn.cursor()
    c.execute("INSERT INTO list_items (parent_note_id, text) VALUES (?, ?)", (parent_note_id, text))
    conn.commit()
    conn.close()

# Функция для удаления заметки
def delete_note(note_id):
    conn = sqlite3.connect('genshin.db')
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()

# Функция для добавления нового персонажа
def insert_character(name, description, rarity, element, birthday, constellation, region, type_weapon, recommended_artifacts, recommended_weapon):
    conn = sqlite3.connect('genshin.db')
    c = conn.cursor()
    c.execute("INSERT INTO characters (name, description, rarity, element, birthday, constellation, region, type_weapon, recommended_artifacts, recommended_weapon) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (name, description, rarity, element, birthday, constellation, region, type_weapon, recommended_artifacts, recommended_weapon))
    conn.commit()
    conn.close()

# Инициализация базы данных
create_database()
