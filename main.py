import requests
import os
from datetime import datetime
import pytz

BOT_TOKEN = "8985690731:AAGaZRKBdUJIu7ExSHoJEAWQ8xrj1eLCYlM"
CHAT_ID = "-1004458187017"

API_TOKEN = "توکن_AlanChand"

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

r = requests.get(
    "https://api.alanchand.com/?type=currencies",
    headers=headers,
    timeout=20
)

data = r.json()

usd = data["usd"]["sell"]
eur = data["eur"]["sell"]

# اگر API تتر هم داخل currencies باشد
try:
    usdt = data["usdt"]["sell"]
except:
    usdt = "وجود ندارد"

iran = pytz.timezone("Asia/Tehran")

now = datetime.now(iran)

message = f"""
📊 قیمت لحظه‌ای بازار

💵 دلار آمریکا: {usd:,}

💶 یورو: {eur:,}

💲 تتر: {usdt}

🕒 {now.strftime("%Y-%m-%d %H:%M")}
"""

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)
