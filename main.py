import requests

BOT_TOKEN = "8985690731:AAGbeHG5hHxjpKoSGBrfCGtN35jGQgCI9as"
CHAT_ID = "-1004458187017"

message = """📊 تست ربات

✅ اگر این پیام را می‌بینی یعنی ربات درست کار می‌کند.
"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(url, data={
    "chat_id": CHAT_ID,
    "text": message
})
