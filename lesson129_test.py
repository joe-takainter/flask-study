
import sqlite3

from app import update_person

connection = sqlite3.connect(":memory:")

try:

    connection.execute(
        """
        CREATE TABLE people (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            hobby TEXT
        )
        """
    )

    with connection:

        connection.execute(
            """
            INSERT INTO people (name, age, hobby)
            VALUES (?, ?, ?)
            """,
            ("テスト太郎", 30, "読書")
        )

    print("=== 存在するIDを更新 ===")

    result = update_person(
        connection, 1, "テスト太郎", 31, "音楽"
    )

    print("更新結果:", result)

    print()

    print("=== 存在しないIDを更新 ===")

    result = update_person(
        connection, 99999, "存在しない人物", 40, "映画"
    )

    print("更新結果:", result)

    print()

    print("=== 最終データ ===")

    people = connection.execute(
        "SELECT * FROM people ORDER BY id"
    ).fetchall()

    print(people)

finally:

    connection.close()
    print("データベース接続を閉じました")
