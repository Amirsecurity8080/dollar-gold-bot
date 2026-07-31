import os
import sys
import requests
from datetime import datetime
import pytz

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

NOBITEX_STATS_URL = "https://api.nobitex.ir/market/stats"

# نمادهایی که می‌خوای قیمتشون رو بگیری: (نماد نمایشی، srcCurrency، dstCurrency)
SYMBOLS = [
    ("💲 تتر", "usdt", "rls"),
    ("₿ بیت‌کوین", "btc", "rls"),
    ("Ξ اتریوم", "eth", "rls"),
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


def get_price(src: str, dst: str) -> float | None:
    """قیمت لحظه‌ای یک جفت ارز رو از نوبیتکس می‌گیرد. مقدار خروجی به ریال است."""
    resp = requests.post(
        NOBITEX_STATS_URL,
        json={"srcCurrency": src, "dstCurrency": dst},
        timeout=20,
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") != "ok":
        raise RuntimeError(f"پاسخ نامعتبر از نوبیتکس: {data}")

    key = f"{src}-{dst}"
    stats = data.get("stats", {}).get(key)
    if not stats:
        return None
    return float(stats["latest"])


def main() -> None:
    missing = [n for n, v in {"BOT_TOKEN": BOT_TOKEN, "CHAT_ID": CHAT_ID}.items() if not v]
    if missing:
        print(f"ERROR: متغیرهای محیطی زیر تنظیم نشده‌اند: {', '.join(missing)}")
        sys.exit(1)

    try:
        lines = []
        for label, src, dst in SYMBOLS:
            price_rls = get_price(src, dst)
            if price_rls is None:
                lines.append(f"{label}: نامشخص")
                continue
            # نوبیتکس قیمت رو به ریال می‌ده؛ برای نمایش به تومان تقسیم بر ۱۰ می‌کنیم
            price_toman = price_rls / 10
            lines.append(f"{label}: {price_toman:,.0f} تومان")

        iran = pytz.timezone("Asia/Tehran")
        now = datetime.now(iran)

        message = (
            "📊 قیمت لحظه‌ای بازار (منبع: نوبیتکس)\n\n"
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
