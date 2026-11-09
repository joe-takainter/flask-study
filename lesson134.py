
from flask import (
    Flask,
    flash,
    redirect,
    render_template_string,
    request,
    url_for
)


app = Flask(__name__)

app.secret_key = "lesson133-local-test-key"


def show_result_message(result):

    if result == "success":
        flash("更新しました", "success")

    elif result == "not_found":
        flash("対象の人物が見つかりません", "warning")

    elif result == "db_error":
        flash("データベースエラーが発生しました", "danger")

    else:
        flash("不明な処理結果です", "warning")



HTML = """
<!doctype html>
<html lang="ja">
<head>
    <meta charset="utf-8">
    <title>第134回 flash色分け練習</title>

    <style>
        body {
            font-family: sans-serif;
            margin: 30px;
        }

        .message {
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 6px;
            border: 1px solid;
        }

        .success {
            background-color: #d4edda;
            color: #155724;
            border-color: #c3e6cb;
        }

        .warning {
            background-color: #fff3cd;
            color: #856404;
            border-color: #ffeeba;
        }

        .danger {
            background-color: #f8d7da;
            color: #721c24;
            border-color: #f5c6cb;
        }

        button {
            padding: 10px;
            margin: 5px;
            cursor: pointer;
        }
    </style>
</head>

<body>

    <h1>第134回 flash色分け練習</h1>

    {% with messages = get_flashed_messages(
        with_categories=true
    ) %}

        {% for category, message in messages %}

            <div class="message {{ category }}">
                {{ message }}
            </div>

        {% endfor %}

    {% endwith %}

    <form method="post" action="{{ url_for('test_result') }}">

        <button type="submit" name="result" value="success">
            正常更新
        </button>

        <button type="submit" name="result" value="not_found">
            対象なし
        </button>

        <button type="submit" name="result" value="db_error">
            DBエラー
        </button>

        <button type="submit" name="result" value="unknown">
            不明な結果
        </button>

    </form>

</body>
</html>
"""



@app.route("/")
def index():

    return render_template_string(HTML)


@app.route("/test", methods=["POST"])
def test_result():

    result = request.form.get("result", "")

    show_result_message(result)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=5001)