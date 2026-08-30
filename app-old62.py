from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3


app = Flask(__name__)

app.secret_key = "flask-study-secret"


def get_db_connection():

    connection = sqlite3.connect("people.db")

    connection.row_factory = sqlite3.Row

    return connection



def load_people():

    people = []

    try:
        file = open("people.txt", "r", encoding="utf-8")

    except FileNotFoundError:
        return []

    for line in file:

        line = line.strip()

        data = line.split(",")

        person = {}

        person["name"] = data[0]
        person["age"] = data[1]
        person["hobby"] = data[2]

        people.append(person)

    file.close()

    return people
def save_people(people):

    file = open("people.txt", "w", encoding="utf-8")

    for person in people:

        file.write(person["name"] + ",")
        file.write(person["age"] + ",")
        file.write(person["hobby"] + "\n")

    file.close()


@app.route("/")
def home():

    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/people")
def show_people():

    connection = get_db_connection()

    people = connection.execute(
        "SELECT * FROM people"
    ).fetchall()

    connection.close()

    query = request.args.get("q", "").strip()

    if query != "":

        filtered_people = []

        for person in people:

            if (
                query.lower() in person["name"].lower()
                or
                query.lower() in person["hobby"].lower()
            ):

                filtered_people.append(person)

        people = filtered_people

    count = len(people)

    return render_template(
        "people.html",
        people=people,
        query=query,
        count=count
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

@app.route("/delete/<name>", methods=["GET", "POST"])
def delete_person(name):

    people = load_people()

    target = None

    for person in people:

        if person["name"] == name:

            target = person

            break

    if target is None:

        flash("その名前は登録されていません。")

        return redirect(url_for("show_people"))

    if request.method == "POST":

        people.remove(target)

        save_people(people)

        flash("削除しました。")

        return redirect(url_for("show_people"))

    return render_template(
        "delete_confirm.html",
        person=target
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