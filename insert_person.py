import sqlite3


connection = sqlite3.connect("people.db")

cursor = connection.cursor()


cursor.execute(
    """
    INSERT INTO people (name, age, hobby)
    VALUES (?, ?, ?)
    """,
    ("Takeshi", 30, "ボウリング")
)


connection.commit()

connection.close()


print("1名登録しました。")