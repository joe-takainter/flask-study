import sqlite3


connection = sqlite3.connect("people.db")

cursor = connection.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS people (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    hobby TEXT
)
""")


connection.commit()

connection.close()


print("データベースを作成しました。")