
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

    # 実験A：2件とも正常に登録する

    print("=== 実験A：COMMIT ===")

    with connection:

        connection.execute(
            "INSERT INTO test_people (name) VALUES (?)",
            ("テスト太郎",)
        )

        connection.execute(
            "INSERT INTO test_people (name) VALUES (?)",
            ("テスト花子",)
        )

    people = connection.execute(
        "SELECT * FROM test_people ORDER BY id"
    ).fetchall()

    print("登録結果:", people)
    print("登録件数:", len(people))

    # 実験B：2件目でエラーを発生させる

    print()
    print("=== 実験B：ROLLBACK ===")

    try:

        with connection:

            connection.execute(
                "INSERT INTO test_people (name) VALUES (?)",
                ("テスト次郎",)
            )

            print("1件目のINSERTが成功しました")

            connection.execute(
                "INSERT INTO test_people (name) VALUES (?)",
                (None,)
            )

    except sqlite3.IntegrityError as error:

        print("エラー内容:", error)
        print("ROLLBACKが実行されました")

    people = connection.execute(
        "SELECT * FROM test_people ORDER BY id"
    ).fetchall()

    print("登録結果:", people)
    print("登録件数:", len(people))

finally:

    connection.close()

    print()
    print("データベース接続を閉じました")
