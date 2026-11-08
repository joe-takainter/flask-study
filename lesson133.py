
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
    <title>第133回 flash練習</title>
</head>
<body>

    <h1>第133回 flash練習</h1>

    {% with messages = get_flashed_messages(
        with_categories=true
    ) %}

        {% for category, message in messages %}

            <p>
                カテゴリ：{{ category }}
                <br>
                メッセージ：{{ message }}
            </p>

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