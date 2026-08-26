import sqlite3


connection = sqlite3.connect("people.db")

cursor = connection.cursor()


cursor.execute("SELECT * FROM people")

rows = cursor.fetchall()


for row in rows:

    print("ID：", row[0])
    print("名前：", row[1])
    print("年齢：", row[2])
    print("趣味：", row[3])
    print("--------------------")


connection.close()