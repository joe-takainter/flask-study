from flask import Flask, render_template

app = Flask(__name__)


people = [
    {"name": "Takeshi", "age": "30", "hobby": "ボウリング"},
    {"name": "Yamada", "age": "25", "hobby": "野球"},
    {"name": "Suzuki", "age": "40", "hobby": "ゴルフ"}
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/people")
def show_people():
    return render_template("people.html", people=people)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)