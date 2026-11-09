
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


def show_result_message(result):

    if result == "success":
        print("更新しました")

    elif result == "not_found":
        print("対象の人物が見つかりません")

    elif result == "db_error":
        print("データベースエラーが発生しました")

    else:
        print("不明な処理結果です")


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

    print("=== 実験A：正常な更新 ===")

    result = update_person(connection, 1, 31)
    print("戻り値:", result)
    show_result_message(result)
    print()

    print("=== 実験B：存在しないID ===")

    result = update_person(connection, 99999, 40)
    print("戻り値:", result)
    show_result_message(result)
    print()

    print("=== 実験C：データベースエラー ===")

    result = update_person(connection, 1, None)
    print("戻り値:", result)
    show_result_message(result)
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

print()
print("=== 実験D：不明な戻り値 ===")

show_result_message("unknown")