
import sqlite3

connection = sqlite3.connect(":memory:")

try:

    connection.execute(
        """
        CREATE TABLE test_people (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER
        )
        """
    )

    # 最初に2件のテストデータを登録
    with connection:

        connection.execute(
            "INSERT INTO test_people (name, age) VALUES (?, ?)",
            ("テスト太郎", 30)
        )

        connection.execute(
            "INSERT INTO test_people (name, age) VALUES (?, ?)",
            ("テスト花子", 25)
        )

    print("=== 初期データ ===")

    people = connection.execute(
        "SELECT * FROM test_people ORDER BY id"
    ).fetchall()

    print(people)
    print()

    # 実験A：存在するIDを更新
    print("=== 実験A：存在するIDをUPDATE ===")

    with connection:

        cursor = connection.execute(
            "UPDATE test_people SET age = ? WHERE id = ?",
            (31, 1)
        )

        print("更新件数:", cursor.rowcount)

    print()

    # 実験B：存在しないIDを更新
    print("=== 実験B：存在しないIDをUPDATE ===")

    with connection:

        cursor = connection.execute(
            "UPDATE test_people SET age = ? WHERE id = ?",
            (40, 99999)
        )

        print("更新件数:", cursor.rowcount)

    print()

    # 実験C：存在するIDを削除
    print("=== 実験C：存在するIDをDELETE ===")

    with connection:

        cursor = connection.execute(
            "DELETE FROM test_people WHERE id = ?",
            (2,)
        )

        print("削除件数:", cursor.rowcount)

    print()

    # 実験D：存在しないIDを削除
    print("=== 実験D：存在しないIDをDELETE ===")

    with connection:

        cursor = connection.execute(
            "DELETE FROM test_people WHERE id = ?",
            (99999,)
        )

        print("削除件数:", cursor.rowcount)

    print()

    # 最終結果
    print("=== 最終データ ===")

    people = connection.execute(
        "SELECT * FROM test_people ORDER BY id"
    ).fetchall()

    print(people)
    print("登録件数:", len(people))

finally:

    connection.close()

    print()
    print("データベース接続を閉じました")
