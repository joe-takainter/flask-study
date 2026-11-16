
import sqlite3
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


def insert_person(connection, name, age, hobby):

    try:

        with connection:

            connection.execute(
                """
                INSERT INTO people (name, age, hobby)
                VALUES (?, ?, ?)
                """,
                (name, age, hobby)
            )

        logging.info("登録に成功しました")

        return "success"

    except sqlite3.Error as e:

        logging.exception("登録エラー: %s", e)

        return "db_error"


connection = sqlite3.connect(":memory:")

try:

    result = insert_person(
        connection, "テスト太郎", 30, "読書"
    )

    print("処理結果:", result)

finally:

    connection.close()
