
import sqlite3
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


def update_person(connection, person_id, name, age, hobby):

    try:

        with connection:

            cursor = connection.execute(
                """
                UPDATE people
                SET name = ?, age = ?, hobby = ?
                WHERE id = ?
                """,
                (name, age, hobby, person_id)
            )

            updated_count = cursor.rowcount

        if updated_count > 0:

            logging.info("更新に成功しました")

            return "success"

        else:

            logging.warning("対象の人物が見つかりません")

            return "not_found"

    except sqlite3.Error as e:

        logging.exception("更新エラー: %s", e)

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

    print("===== テスト1：更新成功 =====", flush=True)

    result = update_person(
        connection, 1, "テスト太郎", 31, "映画"
    )

    print("処理結果:", result, flush=True)

    print()

    print("===== テスト2：対象なし =====", flush=True)

    result = update_person(
        connection, 999, "テスト花子", 25, "旅行"
    )

    print("処理結果:", result, flush=True)

    print()

    print("===== テスト3：DBエラー =====", flush=True)

    with connection:

        connection.execute("DROP TABLE people")

    result = update_person(
        connection, 1, "テスト太郎", 32, "音楽"
    )

    print("処理結果:", result, flush=True)

finally:

    connection.close()
