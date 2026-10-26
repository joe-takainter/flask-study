
import sqlite3

connection = sqlite3.connect(":memory:")

try:

    connection.execute(
        """
        CREATE TABLE test_people (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
        """
    )

    with connection:

        connection.execute(
            "INSERT INTO test_people (name) VALUES (?)",
            ("テスト太郎",)
        )

    print("with文を正常に終了しました")

    people = connection.execute(
        "SELECT * FROM test_people"
    ).fetchall()

    print("登録結果:", people)

finally:

    connection.close()

    print("データベース接続を閉じました")
