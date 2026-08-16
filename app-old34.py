from flask import Flask, render_template, request, redirect

app = Flask(__name__)


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

    return render_template("people.html", people=people)

@app.route("/add", methods=["GET", "POST"])
def add_person():

    error = ""

    if request.method == "POST":

        name = request.form["name"].strip()
        age = request.form["age"].strip()
        hobby = request.form["hobby"].strip()

        if name == "":
            error = "名前は必ず入力してください。"

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

                return redirect("/people")

    return render_template("add.html", error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)