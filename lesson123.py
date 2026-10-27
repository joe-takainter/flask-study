
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

    try:

        with connection:

            connection.execute(
                "INSERT INTO test_people (name) VALUES (?)",
                ("テスト太郎",)
            )

            print("1件目のINSERTが成功しました")

            connection.execute(
                "INSERT INTO test_people (name) VALUES (?)",
                (None,)
            )

            print("2件目のINSERTが成功しました")

    except sqlite3.IntegrityError as error:

        print("エラーが発生しました")
        print("エラー内容:", error)
        print("ロールバックが実行されました")

    people = connection.execute(
        "SELECT * FROM test_people"
    ).fetchall()

    print("登録結果:", people)
    print("登録件数:", len(people))

finally:

    connection.close()

    print("データベース接続を閉じました")
