import sqlite3


connection = sqlite3.connect("people.db")

cursor = connection.cursor()


cursor.execute("SELECT * FROM people")

rows = cursor.fetchall()


for row in rows:
    print(row)


connection.close()