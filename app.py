from flask import Flask, render_template

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)