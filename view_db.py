import os
import sqlite3

def view_articles():
    # Adjust the path to the database file
    db_path = os.path.join(os.path.dirname(__file__), 'etl_news_project', 'spiders', 'articles.db')
    print(f"Database path: {db_path}")  # Debug print

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute a query to retrieve all rows from the articles table
    cursor.execute("SELECT * FROM articles")
    rows = cursor.fetchall()

    # Print the retrieved rows
    for row in rows:
        print(row)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    view_articles()
