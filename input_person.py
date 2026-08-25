import sqlite3


while True:

    name = input("名前：").strip()

    if name != "":

        break

    print("名前は必ず入力してください。")
while True:

    age = input("年齢：").strip()

    if age.isdigit():

        break

    print("年齢は数字で入力してください。")
hobby = input("趣味：").strip()


connection = sqlite3.connect("people.db")

cursor = connection.cursor()


cursor.execute(
    """
    INSERT INTO people (name, age, hobby)
    VALUES (?, ?, ?)
    """,
    (name, age, hobby)
)


connection.commit()

connection.close()


print("1名登録しました。")