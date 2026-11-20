
import sqlite3
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(message)s"
)


def insert_person(connection, name, age, hobby):
    try:
        with connection:
            cursor = connection.execute(
                """
                INSERT INTO people (name, age, hobby)
                VALUES (?, ?, ?)
                """,
                (name, age, hobby)
            )

        logging.info("登録に成功しました")
        return cursor.lastrowid

    except sqlite3.Error as e:
        logging.exception("登録エラー: %s", e)
        return None


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

        logging.warning("更新対象が見つかりません")
        return "not_found"

    except sqlite3.Error as e:
        logging.exception("更新エラー: %s", e)
        return "db_error"


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

        logging.warning("削除対象が見つかりません")
        return "not_found"

    except sqlite3.Error as e:
        logging.exception("削除エラー: %s", e)
        return "db_error"


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

        print("===== 1. 登録 =====", flush=True)
        person_id = insert_person(
            connection, "テスト太郎", 30, "読書"
        )
        print("登録ID:", person_id, flush=True)

        print("\n===== 2. 更新 =====", flush=True)
        result = update_person(
            connection, person_id, "テスト太郎", 31, "映画"
        )
        print("更新結果:", result, flush=True)

        print("\n===== 3. データ確認 =====", flush=True)
        rows = connection.execute(
            "SELECT * FROM people"
        ).fetchall()

        for row in rows:
            print(row, flush=True)

        print("\n===== 4. 削除 =====", flush=True)
        result = delete_person(connection, person_id)
        print("削除結果:", result, flush=True)

        print("\n===== 5. 削除後の確認 =====", flush=True)
        rows = connection.execute(
            "SELECT * FROM people"
        ).fetchall()
        print("登録件数:", len(rows), flush=True)

    finally:
        connection.close()


if __name__ == "__main__":
    main()


