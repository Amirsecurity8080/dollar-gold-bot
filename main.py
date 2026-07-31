import os
import sys
import requests
from datetime import datetime
import pytz

# ---------------------------------------------------------------------------
# فقط توکن ربات تلگرام و آیدی کانال لازمه. CoinGecko کاملاً رایگان و بدون
# کلیده و از هر جای دنیا (از جمله GitHub Actions) در دسترسه.
# ---------------------------------------------------------------------------
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

# نمادهایی که می‌خوای قیمتشون رو بگیری: (نماد نمایشی، coingecko id)
COINS = [
    ("💲 تتر", "tether"),
    ("₿ بیت‌کوین", "bitcoin"),
    ("Ξ اتریوم", "ethereum"),
]


def send_telegram_message(text: str) -> None:
    """پیام رو به کانال تلگرام ارسال می‌کند."""
    try:
        resp = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": text},
            timeout=20,
        )
        print("Telegram Status:", resp.status_code)
        print(resp.text)
    except Exception as telegram_err:
        print("Telegram Error:", telegram_err)


def main() -> None:
    missing = [n for n, v in {"BOT_TOKEN": BOT_TOKEN, "CHAT_ID": CHAT_ID}.items() if not v]
    if missing:
        print(f"ERROR: متغیرهای محیطی زیر تنظیم نشده‌اند: {', '.join(missing)}")
        sys.exit(1)

    try:
        ids = ",".join(cid for _, cid in COINS)
        r = requests.get(
            COINGECKO_URL,
            params={"ids": ids, "vs_currencies": "usd"},
            timeout=20,
        )
        r.raise_for_status()
        data = r.json()

        lines = []
        for label, cid in COINS:
            price = data.get(cid, {}).get("usd")
            if price is None:
                lines.append(f"{label}: نامشخص")
            else:
                lines.append(f"{label}: ${price:,.4f}" if price < 1 else f"{label}: ${price:,.2f}")

        iran = pytz.timezone("Asia/Tehran")
        now = datetime.now(iran)

        message = (
            "📊 قیمت لحظه‌ای ارزهای دیجیتال (منبع: CoinGecko)\n\n"
            + "\n".join(lines)
            + f"\n\n🕒 {now.strftime('%Y-%m-%d %H:%M')}"
        )

        send_telegram_message(message)

    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else "?"
        body = e.response.text[:300] if e.response is not None else ""
        error_text = f"❌ خطا در دریافت قیمت (HTTP {status}):\n{body}"
        print("ERROR:", error_text)
        send_telegram_message(error_text)

    except Exception as e:
        error_text = f"❌ ERROR:\n{str(e)}"
        print("ERROR:", str(e))
        send_telegram_message(error_text)


if __name__ == "__main__":
    main()
