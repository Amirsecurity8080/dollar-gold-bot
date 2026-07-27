import requests
from datetime import datetime
import pytz

BOT_TOKEN = "8985690731:AAGaZRKBdUJIu7ExSHoJEAWQ8xrj1eLCYlM"
CHAT_ID = "-1004458187017"

API_TOKEN = "توکن_AlanChand"

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

try:
    r = requests.get(
        "https://api.alanchand.com/?type=currencies",
        headers=headers,
        timeout=20
    )

    r.raise_for_status()

    data = r.json()

    usd = data["usd"]["sell"]
    eur = data["eur"]["sell"]

    if "usdt" in data:
        usdt = data["usdt"]["sell"]
    else:
        usdt = "وجود ندارد"

    iran = pytz.timezone("Asia/Tehran")
    now = datetime.now(iran)

    message = f"""
📊 قیمت لحظه‌ای بازار

💵 دلار: {usd:,}
💶 یورو: {eur:,}
💲 تتر: {usdt}

🕒 {now.strftime("%Y-%m-%d %H:%M")}
"""

    telegram = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message
        },
        timeout=20
    )

    print("Telegram Status:", telegram.status_code)
    print(telegram.text)

except Exception as e:
    print("ERROR:", str(e))

    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": f"❌ ERROR:\n{str(e)}"
            },
            timeout=20
        )
    except Exception as err:
        print("Telegram Error:", err)
