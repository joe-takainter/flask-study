
import sqlite3

from app import delete_person_from_db

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

        connection.execute(
            """
            INSERT INTO people (name, age, hobby)
            VALUES (?, ?, ?)
            """,
            ("テスト花子", 25, "映画")
        )

    print("=== 初期データ ===")

    people = connection.execute(
        "SELECT * FROM people ORDER BY id"
    ).fetchall()

    print(people)
    print()

    print("=== 存在するIDを削除 ===")

    result = delete_person_from_db(connection, 2)

    print("削除結果:", result)
    print()

    print("=== 存在しないIDを削除 ===")

    result = delete_person_from_db(connection, 99999)

    print("削除結果:", result)
    print()

    print("=== 最終データ ===")

    people = connection.execute(
        "SELECT * FROM people ORDER BY id"
    ).fetchall()

    print(people)
    print("登録件数:", len(people))

finally:

    connection.close()

    print()
    print("データベース接続を閉じました")
