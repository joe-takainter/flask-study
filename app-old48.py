from flask import Flask, render_template, request, redirect, flash
app = Flask(__name__)
app.secret_key = "flask-study-secret"


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

    people = load_people()

    query = request.args.get("q", "").strip()

    if query != "":

        filtered_people = []

        for person in people:

            if query.lower() in person["name"].lower():

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
            people = load_people()

            duplicate = False

            for person in people:
                if person["name"] == name:
                    duplicate = True
                    break

            if duplicate:
                error = "同じ名前が登録されています。"

            else:
                person = {
                    "name": name,
                    "age": age,
                    "hobby": hobby
                }

                people.append(person)

                save_people(people)

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
@app.route("/edit/<name>", methods=["GET", "POST"])
def edit_person(name):

    people = load_people()

    target = None

    for person in people:
        if person["name"] == name:
            target = person
            break

    if target is None:
        flash("その名前は登録されていません。")
        return redirect(url_for("show_people"))

    error = ""

    if request.method == "POST":

        new_name = request.form["name"].strip()
        new_age = request.form["age"].strip()
        new_hobby = request.form["hobby"].strip()

        if new_name == "":
            error = "名前は必ず入力してください。"

        elif new_age == "":
            error = "年齢は必ず入力してください。"

        elif not new_age.isdigit():
            error = "年齢は数字で入力してください。"

        elif int(new_age) < 0 or int(new_age) > 120:
            error = "年齢は0～120の範囲で入力してください。"

        else:

            duplicate = False

            for person in people:

                if person["name"] == new_name and person is not target:
                    duplicate = True
                    break

            if duplicate:
                error = "同じ名前が登録されています。"

            else:
                target["name"] = new_name
                target["age"] = new_age
                target["hobby"] = new_hobby

                save_people(people)

                flash("更新しました。")

                return redirect(url_for("show_people"))

        if error != "":
            target["name"] = new_name
            target["age"] = new_age
            target["hobby"] = new_hobby

    return render_template(
        "edit.html",
        person=target,
        error=error
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)