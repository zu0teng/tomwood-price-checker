import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
from scraper import fetch_price
from notifier import send_email
from storage import load_history, save_history
from dotenv import load_dotenv

# === .env の読み込み ===
load_dotenv()

# === ログ設定（7日分ローテーション） ===
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# ファイル出力（毎日ローテーション、7日保持）
file_handler = TimedRotatingFileHandler(
    "run.log",
    when="midnight",    # 毎日0時に新しいログファイル
    interval=1,
    backupCount=7,      # 7日分を保持
    encoding="utf-8"
)

# フォーマット設定
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# ターミナルにも出力
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
# =========================================

urls = [
    "https://www.tomwoodproject.com/jp_ja/product/ice-huggie/",
    "https://www.tomwoodproject.com/jp_ja/product/robin-bracelet/"
]

def main():
    history = load_history()
    today = str(datetime.date.today())
    messages = []

    for url in urls:
        logging.info(f"取得開始: {url}")
        current_price = fetch_price(url)

        if current_price is None:
            logging.warning(f"価格取得に失敗しました: {url}")
            continue

        old_price = history.get(url, {}).get("price")

        if old_price is None:
            logging.info(f"初回記録: {url} → {current_price}円")
        elif current_price < old_price:
            logging.info(f"値下げ検出: {old_price}円 → {current_price}円 ({url})")
            messages.append(f"値下げ: {url}\n{old_price}円 → {current_price}円")
        else:
            logging.info(f"変化なし: {old_price}円 → {current_price}円")

        history[url] = {"date": today, "price": current_price}

    save_history(history)

    if messages:
        subject = "Tom Wood 値下げ通知"
        body = "\n\n".join(messages)
        try:
            send_email(subject, body)
            logging.info("メール送信完了。")
        except Exception as e:
            logging.error(f"メール送信失敗: {e}")
    else:
        logging.info("値下がりなし。メール送信スキップ。")

if __name__ == "__main__":
    logging.info("==== 実行開始 ====")
    main()
    logging.info("==== 実行終了 ====\n")
