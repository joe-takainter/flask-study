
import sqlite3


def update_person(connection, person_id, new_age):

    try:

        with connection:

            cursor = connection.execute(
                """
                UPDATE test_people
                SET age = ?
                WHERE id = ?
                """,
                (new_age, person_id)
            )

            updated_count = cursor.rowcount

        if updated_count == 0:
            return "not_found"

        return "success"

    except sqlite3.Error:
        return "db_error"


connection = sqlite3.connect(":memory:")

try:

    connection.execute(
        """
        CREATE TABLE test_people (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
        """
    )

    with connection:

        connection.execute(
            """
            INSERT INTO test_people (name, age)
            VALUES (?, ?)
            """,
            ("テスト太郎", 30)
        )

    print("=== 初期データ ===")

    people = connection.execute(
        "SELECT * FROM test_people"
    ).fetchall()

    print(people)
    print()

    print("=== 実験A：正常に更新 ===")

    result = update_person(connection, 1, 31)
    print("処理結果:", result)
    print()

    print("=== 実験B：存在しないID ===")

    result = update_person(connection, 99999, 40)
    print("処理結果:", result)
    print()

    print("=== 実験C：データベースエラー ===")

    result = update_person(connection, 1, None)
    print("処理結果:", result)
    print()

    print("=== 最終データ ===")

    people = connection.execute(
        "SELECT * FROM test_people"
    ).fetchall()

    print(people)

finally:

    connection.close()

    print()
    print("データベース接続を閉じました")
