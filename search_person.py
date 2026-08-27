import sqlite3


person_id = input("検索するID：").strip()


connection = sqlite3.connect("people.db")

connection.row_factory = sqlite3.Row

cursor = connection.cursor()


cursor.execute(
    "SELECT * FROM people WHERE id = ?",
    (person_id,)
)


row = cursor.fetchone()


if row:

    print("ID：", row["id"])
    print("名前：", row["name"])
    print("年齢：", row["age"])
    print("趣味：", row["hobby"])

else:

    print("そのIDの人は登録されていません。")


connection.close()