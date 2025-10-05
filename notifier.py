# notifier.py
import smtplib, os
from email.mime.text import MIMEText
import os

def send_email(subject: str, body: str) -> None:
    sender = os.environ.get("GMAIL_SENDER")        # 例: yourname@gmail.com
    recipient = os.environ.get("GMAIL_RECIPIENT")  # 例: notify-destination@gmail.com
    password = os.environ.get("GMAIL_APP_PASSWORD")
    if not (sender and recipient and password):
        raise RuntimeError("Email環境変数(GMAIL_SENDER/GMAIL_RECIPIENT/GMAIL_APP_PASSWORD)が未設定です。")

    msg = MIMEText(body, _charset="utf-8")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)
