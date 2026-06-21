import os
import requests
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

LINE_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
USER_ID = os.getenv("LINE_USER_ID")

app = Flask(__name__)


def get_quote():
    res = requests.get("https://zenquotes.io/api/random")
    data = res.json()
    quote = data[0]["q"]
    author = data[0]["a"]
    return quote, author


def translate(text):
    url = "https://api.mymemory.translated.net/get"
    params = {"q": text, "langpair": "en|ja"}
    res = requests.get(url, params=params)
    return res.json()["responseData"]["translatedText"]


def send_line(message):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "to": USER_ID,
        "messages": [{"type": "text", "text": message}]
    }
    requests.post(url, headers=headers, json=data)


@app.route("/")
def index():
    return "名言Bot 動いてます！"


@app.route("/quote")
def quote():
    q, author = get_quote()
    japanese = translate(q)
    message = f"🌟 今日の名言\n\n\"{q}\"\n― {author}\n\n「{japanese}」\n\n今日も一日頑張ろう！✨"
    send_line(message)
    return "送信完了"


if __name__ == "__main__":
    app.run(port=5000)
