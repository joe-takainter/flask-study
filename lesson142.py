

import sqlite3

from lesson141 import update_person, delete_person


def main():
    connection = sqlite3.connect(":memory:")

    try:
        with connection:
            connection.execute(
                """
                CREATE TABLE people (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    age INTEGER,
                    hobby TEXT
                )
                """
            )

        print("===== テスト1：存在しないIDの更新 =====", flush=True)

        result = update_person(
            connection, 999, "テスト花子", 25, "旅行"
        )

        print("更新結果:", result, flush=True)

        print()

        print("===== テスト2：存在しないIDの削除 =====", flush=True)

        result = delete_person(connection, 999)

        print("削除結果:", result, flush=True)

        print()

        print("===== テスト3：データベースエラー =====", flush=True)

        with connection:
            connection.execute("DROP TABLE people")

        result = delete_person(connection, 1)

        print("削除結果:", result, flush=True)

    finally:
        connection.close()


if __name__ == "__main__":
    main()
