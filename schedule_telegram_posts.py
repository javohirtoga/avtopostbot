import datetime
import json
import time
import requests

# Configuration
BOT_TOKEN = "2115813430:AAGutGn817sAejVIDRKNfK3YT9JUArJYM9Y"
CHANNEL_ID = "@hushtam"
ADMIN_LINK = "@javohir_baxodirov"
ROUTE_NAME = "Beshariq - Qo'qon - Dangara"

# Use Tashkent timezone (UTC+5) for scheduled_date timestamps
TASHKENT_TZ = datetime.timezone(datetime.timedelta(hours=5))

# Message schedule times for each day
SCHEDULE_TIMES = ["07:30", "11:30", "14:30", "17:30", "21:00"]

# Delay between scheduling requests to avoid Telegram rate limits
REQUEST_DELAY_SECONDS = 2

# Message templates for automatic generation
POST_TEMPLATES = {
    "morning": [
        "🌇 {day} tongi: {route} yo'nalishida yo'l vaziyati yaxshi. Ishga o'tish yoki sayohat uchun @hushtam bilan ishonchli yo'lni tanlang.",
        "☀️ Ertalabki salom! {route} yo'nalishidagi marshrutlarimiz qulay va xavfsiz. Hozir ham band qilish mumkin.",
        "🌤️ {route} safaringiz uchun ob-havo ma'lumotlari yangilandi. Ishga borish uchun ishonchli transport bizda mavjud."
    ],
    "cargo": [
        "📦 {route} bo'ylab yuk va parcel yetkazib berish xizmati. Sizning paketlaringizni Toshkentga ishonchli yetkazamiz.",
        "🚚 Yukingiz bormi? {route} yo'nalishida tez, xavfsiz va arzon Cargo xizmatini tanlang.",
        "📬 Tezkor parcel xizmatimiz bilan {route} bo'ylab yuklarni qat'iy muddatda yetkazamiz. Kanalga yozing."
    ],
    "comfort": [
        "🛋️ {route} yo'lovchilari uchun qulaylik va xavfsizlik birinchi o'rinda. Toza transport, yaxshi havoni chiqarish va xushmuomala haydovchilar.",
        "🚍 Komfortli sayohat: keng o'rindiqlar, konditsioner va qat'iy sanitariya qoidalari. {route} yo'nalishida ishonchli safar.",
        "😌 Safaringiz davomida qulaylikni his qiling. {route} yo'lda har bir yo'lovchi uchun eng yaxshi xizmat."
    ],
    "booking": [
        "📲 Ertangi {route} safariga joy band qilishni boshlang. Oldindan buyurtma qiling, eng yaxshi o'rinlarni qo'lga kiriting.",
        "🕒 Ertangi yo'lovchilik uchun joylar cheklanadi. {route} yo'nalishida hozir buyurtma qiling va o'zingizga mos vaqtni tanlang.",
        "📅 {route} bo'ylab sayohat uchun joyni oldindan band qilib qo'ying. Ish va shaxsiy safarlarni ishonchli rejalashtiring."
    ],
    "driver": [
        "💼 Haydovchilar uchun daromad imkoniyati: @hushtam kanali orqali yangi yo'lovchilarni toping va sherik bo'ling.",
        "📈 {route} yo'nalishida haydovchilar uchun qo'shimcha ishlash rejasi. Kanalimiz orqali hamkorlik boshlang.",
        "🎯 Haydovchi do'stlaringizga ayting: @javohir_baxodirov bilan aloqaga chiqing, {route} yo'lda ko'proq daromad toping."
    ]
}

DAYS_OF_WEEK = [
    "Dushanba",
    "Seshanba",
    "Chorshanba",
    "Payshanba",
    "Juma",
    "Shanba",
    "Yakshanba",
]

TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# Inline keyboard markup with admin contact and channel button
REPLY_MARKUP = {
    "inline_keyboard": [
        [
            {"text": "📞 Admin bilan bog'lanish", "url": f"https://t.me/{ADMIN_LINK.lstrip('@')}"},
            {"text": "🔔 Kanalga o'tish", "url": "https://t.me/hushtam"}
        ]
    ]
}


def get_next_monday(start_date: datetime.date) -> datetime.date:
    days_ahead = (0 - start_date.weekday()) % 7
    return start_date + datetime.timedelta(days=days_ahead)


def build_schedule_dates() -> list[datetime.datetime]:
    today = datetime.datetime.now(tz=TASHKENT_TZ).date()
    first_monday = get_next_monday(today)
    schedule_dates = []

    for day_offset in range(7):
        current_date = first_monday + datetime.timedelta(days=day_offset)
        for schedule_time in SCHEDULE_TIMES:
            hour, minute = map(int, schedule_time.split(':'))
            schedule_dates.append(
                datetime.datetime(
                    year=current_date.year,
                    month=current_date.month,
                    day=current_date.day,
                    hour=hour,
                    minute=minute,
                    tzinfo=TASHKENT_TZ,
                )
            )

    return schedule_dates


def generate_daily_posts() -> list[str]:
    posts = []
    slot_keys = ["morning", "cargo", "comfort", "booking", "driver"]

    for day_name in DAYS_OF_WEEK:
        for slot_key in slot_keys:
            templates = POST_TEMPLATES[slot_key]
            index = (DAYS_OF_WEEK.index(day_name) + slot_keys.index(slot_key)) % len(templates)
            text = templates[index].format(day=day_name, route=ROUTE_NAME)
            posts.append(text)

    return posts


def send_scheduled_message(text: str, scheduled_datetime: datetime.datetime) -> None:
    timestamp = int(scheduled_datetime.timestamp())
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
        "scheduled_date": timestamp,
        "reply_markup": REPLY_MARKUP,
    }

    while True:
        try:
            response = requests.post(TELEGRAM_API_URL, json=payload, timeout=15)
            response_data = response.json()
        except requests.RequestException as exc:
            print(f"HTTP request failed for {scheduled_datetime.isoformat()}: {exc}")
            return
        except ValueError:
            print(f"Invalid JSON response for {scheduled_datetime.isoformat()}: {response.text}")
            return

        if response.status_code == 429 or response_data.get("error_code") == 429:
            retry_after = response_data.get("parameters", {}).get("retry_after", REQUEST_DELAY_SECONDS)
            wait_seconds = max(int(retry_after) + 1, REQUEST_DELAY_SECONDS)
            print(
                f"Telegram rate limit hit. Kutish {wait_seconds} soniya..."
            )
            time.sleep(wait_seconds)
            continue

        if response.status_code != 200 or not response_data.get("ok", False):
            print(f"Failed to schedule message for {scheduled_datetime.isoformat()}")
            print(json.dumps(response_data, ensure_ascii=False, indent=2))
            return

        message_id = response_data["result"]["message_id"]
        print(
            f"Scheduled message {message_id} for {scheduled_datetime.strftime('%Y-%m-%d %H:%M')} Tashkent"
        )
        return


if __name__ == "__main__":
    scheduled_datetimes = build_schedule_dates()
    post_texts = generate_daily_posts()

    for scheduled_datetime, text in zip(scheduled_datetimes, post_texts):
        print(f"Rejalashtirish: {scheduled_datetime.strftime('%Y-%m-%d %H:%M')} | {text[:40]}...")
        send_scheduled_message(text, scheduled_datetime)
        time.sleep(REQUEST_DELAY_SECONDS)

    print("\nBarcha 35 ta post Telegramning schudle bo'limiga rejalashtirildi.")

# Requirements:
# pip install requests
