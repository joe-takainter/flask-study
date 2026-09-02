from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3


app = Flask(__name__)

app.secret_key = "flask-study-secret"


def get_db_connection():

    connection = sqlite3.connect("people.db")

    connection.row_factory = sqlite3.Row

    return connection





@app.route("/")
def home():

    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/people")
def show_people():

    query = request.args.get("q", "").strip()

    sort = request.args.get("sort", "name")


    if sort == "age":

        order_column = "age"

    elif sort == "id":

        order_column = "id"

    else:

        order_column = "name"


    connection = get_db_connection()


    if query != "":

        search_word = "%" + query + "%"

        people = connection.execute(
            f"""
            SELECT * FROM people
            WHERE name LIKE ?
               OR hobby LIKE ?
            ORDER BY {order_column}
            """,
            (search_word, search_word)
        ).fetchall()

    else:

        people = connection.execute(
            f"""
            SELECT * FROM people
            ORDER BY {order_column}
            """
        ).fetchall()


    connection.close()

    count = len(people)


    return render_template(
        "people.html",
        people=people,
        query=query,
        count=count,
        sort=sort
    )

@app.route("/add", methods=["GET", "POST"])
def add_person():

    error = ""
    name = ""
    age = ""
    hobby = ""

    if request.method == "POST":

        name = request.form["name"].strip()
        age = request.form["age"].strip()
        hobby = request.form["hobby"].strip()

        if name == "":
            error = "名前は必ず入力してください。"

        elif age == "":
            error = "年齢は必ず入力してください。"

        elif not age.isdigit():
            error = "年齢は数字で入力してください。"

        elif int(age) < 0 or int(age) > 120:
            error = "年齢は0～120の範囲で入力してください。"

        else:

            connection = get_db_connection()

            person = connection.execute(
                "SELECT * FROM people WHERE name = ?",
                (name,)
            ).fetchone()

            if person:

                error = "同じ名前が登録されています。"

                connection.close()

            else:

                connection.execute(
                    """
                    INSERT INTO people (name, age, hobby)
                    VALUES (?, ?, ?)
                    """,
                    (name, age, hobby)
                )

                connection.commit()

                connection.close()

                flash("登録しました！")

                return redirect(url_for("show_people"))

    return render_template(
        "add.html",
        error=error,
        name=name,
        age=age,
        hobby=hobby
    )

@app.route("/delete/<int:person_id>", methods=["GET", "POST"])
def delete_person(person_id):

    connection = get_db_connection()

    person = connection.execute(
        "SELECT * FROM people WHERE id = ?",
        (person_id,)
    ).fetchone()


    if person is None:

        connection.close()

        flash("その人は登録されていません。")

        return redirect(url_for("show_people"))


    if request.method == "POST":

        connection.execute(
            "DELETE FROM people WHERE id = ?",
            (person_id,)
        )

        connection.commit()

        connection.close()

        flash("削除しました！")

        return redirect(url_for("show_people"))


    connection.close()

    return render_template(
        "delete_confirm.html",
        person=person
    )
@app.route("/edit/<int:person_id>", methods=["GET", "POST"])
def edit_person(person_id):

    connection = get_db_connection()

    person = connection.execute(
        "SELECT * FROM people WHERE id = ?",
        (person_id,)
    ).fetchone()


    if person is None:

        connection.close()

        flash("その人は登録されていません。")

        return redirect(url_for("show_people"))


    error = ""


    if request.method == "POST":

        name = request.form["name"].strip()
        age = request.form["age"].strip()
        hobby = request.form["hobby"].strip()


        if name == "":

            error = "名前は必ず入力してください。"


        elif age == "":

            error = "年齢は必ず入力してください。"


        elif not age.isdigit():

            error = "年齢は数字で入力してください。"


        elif int(age) < 0 or int(age) > 120:

            error = "年齢は0～120の範囲で入力してください。"


        else:

            duplicate = connection.execute(
                """
                SELECT * FROM people
                WHERE name = ? AND id != ?
                """,
                (name, person_id)
            ).fetchone()


            if duplicate:

                error = "同じ名前が登録されています。"


            else:

                connection.execute(
                    """
                    UPDATE people
                    SET name = ?, age = ?, hobby = ?
                    WHERE id = ?
                    """,
                    (name, age, hobby, person_id)
                )

                connection.commit()

                connection.close()

                flash("更新しました！")

                return redirect(url_for("show_people"))


        connection.close()

        return render_template(
            "edit.html",
            person={
                "id": person_id,
                "name": name,
                "age": age,
                "hobby": hobby
            },
            error=error
        )


    connection.close()

    return render_template(
        "edit.html",
        person=person,
        error=error
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)