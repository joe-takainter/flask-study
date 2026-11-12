def greet(name):
    return f"こんにちは、{name}さん！"


def main():
    name = input("お名前を入力してください：")
    message = greet(name)
    print(message)


if __name__ == "__main__":
    main()
