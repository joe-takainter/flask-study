
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logging.debug("詳細な動作確認です")

logging.info("住所録アプリを起動しました")

logging.warning("対象の人物が見つかりません")

logging.error("データベースエラーが発生しました")

logging.critical("重大なエラーが発生しました")
