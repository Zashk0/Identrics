import json
import sqlite3
from transform_data import transform_data
import os

def load_data(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_to_db(data):
    db_path = os.path.join(os.path.dirname(__file__), '..', 'spiders', 'articles.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            body TEXT,
            url TEXT UNIQUE,
            pub_datetime TEXT,
            author TEXT,
            images TEXT,
            ner TEXT,
            comments INTEGER DEFAULT 0
        )
    ''')

    for item in data:
        print("Saving item to DB:", item)  # Debug print
        cursor.execute('''
            INSERT OR IGNORE INTO articles (title, body, url, pub_datetime, author, images, ner, comments)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (item['title'], item['body'], item['url'], item['pub_datetime'], item['author'], json.dumps(item['images']), json.dumps(item['ner']), item.get('comments', 0)))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    raw_data_restofworld_path = os.path.join(os.path.dirname(__file__), '..', 'spiders', 'raw_data_restofworld.json')
    raw_data_capitalbrief_path = os.path.join(os.path.dirname(__file__), '..', 'spiders', 'raw_data_capitalbrief.json')

    print(f"Loading data from {raw_data_restofworld_path}")  # Debug print
    print(f"Loading data from {raw_data_capitalbrief_path}")  # Debug print

    raw_data_restofworld = load_data(raw_data_restofworld_path)
    raw_data_capitalbrief = load_data(raw_data_capitalbrief_path)

    if raw_data_restofworld:
        transformed_data_restofworld = transform_data(raw_data_restofworld)
        save_to_db(transformed_data_restofworld)

    if raw_data_capitalbrief:
        transformed_data_capitalbrief = transform_data(raw_data_capitalbrief)
        save_to_db(transformed_data_capitalbrief)
