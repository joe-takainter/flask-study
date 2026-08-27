import sqlite3


person_id = input("変更する人のID：").strip()


connection = sqlite3.connect("people.db")

connection.row_factory = sqlite3.Row

cursor = connection.cursor()


cursor.execute(
    "SELECT * FROM people WHERE id = ?",
    (person_id,)
)

row = cursor.fetchone()


if row:

    print()
    print("現在の登録内容")
    print("--------------------")
    print("名前：", row["name"])
    print("年齢：", row["age"])
    print("趣味：", row["hobby"])
    print("--------------------")

    print()

    age = input("新しい年齢（変更しない場合はEnter）：").strip()

    if age == "":
        age = row["age"]


    hobby = input("新しい趣味（変更しない場合はEnter）：").strip()

    if hobby == "":
        hobby = row["hobby"]

    cursor.execute(
        """
        UPDATE people
        SET age = ?, hobby = ?
        WHERE id = ?
        """,
        (age, hobby, person_id)
    )

    connection.commit()

    print("更新しました。")

else:

    print("そのIDの人は登録されていません。")


connection.close()