import os
import requests
from dotenv import load_dotenv

load_dotenv()

LINE_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
USER_ID = os.getenv("LINE_USER_ID")

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
    res = requests.post(url, headers=headers, json=data)
    print(res.status_code, res.text)

if __name__ == "__main__":
    quote, author = get_quote()
    japanese = translate(quote)
    message = f"🌟 今日の名言\n\n\"{quote}\"\n― {author}\n\n「{japanese}」\n\n今日も一日頑張ろう！✨"
    send_line(message)
    print("送信完了")