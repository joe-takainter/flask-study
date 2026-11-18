
import sqlite3
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


def delete_person(connection, person_id):

    try:
        with connection:
            cursor = connection.execute(
                "DELETE FROM people WHERE id = ?",
                (person_id,)
            )

            deleted_count = cursor.rowcount

        if deleted_count > 0:
            logging.info("削除に成功しました")
            return "success"
        else:
            logging.warning("対象の人物が見つかりません")
            return "not_found"

    except sqlite3.Error as e:
        logging.exception("削除エラー: %s", e)
        return "db_error"


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

        connection.execute(
            """
            INSERT INTO people (name, age, hobby)
            VALUES (?, ?, ?)
            """,
            ("テスト太郎", 30, "読書")
        )

    print("===== テスト1：削除成功 =====", flush=True)
    result = delete_person(connection, 1)
    print("処理結果:", result, flush=True)

    print()

    print("===== テスト2：対象なし =====", flush=True)
    result = delete_person(connection, 999)
    print("処理結果:", result, flush=True)

    print()

    print("===== テスト3：DBエラー =====", flush=True)

    with connection:
        connection.execute("DROP TABLE people")

    result = delete_person(connection, 1)
    print("処理結果:", result, flush=True)

finally:
    connection.close()
