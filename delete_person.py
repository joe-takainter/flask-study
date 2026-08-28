import sqlite3


person_id = input("削除する人のID：").strip()


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
    print("削除する人")
    print("--------------------")
    print("名前：", row["name"])
    print("年齢：", row["age"])
    print("趣味：", row["hobby"])
    print("--------------------")

    print()

    answer = input(
    "本当に削除しますか？（y/n）："
    ).strip()

    print("入力された内容：", repr(answer))

    if answer.lower() == "y":

        cursor.execute(
            "DELETE FROM people WHERE id = ?",
            (person_id,)
        )

        connection.commit()

        print("削除しました。")

    else:

        print("削除を中止しました。")

else:

    print("そのIDの人は登録されていません。")


connection.close()