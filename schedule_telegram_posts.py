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

# 35 post texts, each 2-4 sentences, ready for scheduling
POST_TEXTS = [
    "Assalomu alaykum! Beshariq - Qo'qon - Dangara yo'nalishida ertalabki yo'l holati yaxshi. Ishga borish uchun ishonchli va qulay transportimiz mavjud. @hushtam kanalida joyni oldindan band qiling.",
    "Qo'chayotgan yuklaringiz bormi? Bizning cargo xizmati bilan yuklaringizni vaqtida va ishonchli yetkazamiz. Sizga har doim eng yaxshi narx va hizmat taklif qilamiz.",
    "Safaringizni qulay qilish bizning vazifamiz. avtobuslarimizda toza o'rindiqlar va konditsioner mavjud. Yo'lovchilarimizning xavfsizligi birinchi o'rinda.",
    "Ertangi yo'lga joy band qilish vaqti keldi. Hozir buyurtma berib, o'zingizga yoqqan o'rinni tanlang. @javohir_baxodirov orqali tezkor aloqaga chiqing.",
    "Haydovchilar uchun yangi imkoniyatlar ochildi. Kanalimizda sherik bo'lib, yanada ko'proq yo'lovchi va daromad oling. Beshariq - Qo'qon yo'lida birga ishlash qulay.",
    "Seshanba tongi ob-havo ma'lumotlari: yo'lda shamol va bulutlar bor. Bizning avtobuslar yo'lga tayyor va sizni Toshkentga xavfsiz yetkazadi.",
    "Kichik yoki katta yukni yetkazib berish kerakmi? Beshariq - Qo'qon - Dangara yo'nalishida cargo xizmatimiz mavjud. Paketlaringizni xatosiz va tez yetkazamiz.",
    "Yo'lovchilar uchun qulayliklarimizni sinab ko'ring. Toza transport, xushmuomala haydovchilar va qulay o'rindiqlar sizni kutmoqda. Har safar ishonchli xizmat kafolatlanadi.",
    "Ertangi safaringizni endi rejalashtiring. Joylar cheklangan emas, ammo eng yaxshi o'rinlar tez tugaydi. Kanalimiz orqali buyurtma bering.",
    "Haydovchi bo'lmaysizmi? Siz ham @hushtam bilan ishlashni boshlang. Har kuni yangi yo'lovchi va barqaror daromad uchun imkoniyat mavjud.",
    "Chorshanba tongida yo'l holati yaxshi. Beshariq - Dangara yo'nalishida yo'l davomiyligi optimallashtirilgan. Sizga eng ishonchli safarni taqdim etamiz.",
    "Toshkentga yuk yetkazish kerak bo'lsa, bizning cargo xizmati eng yaxshi tanlov. Paketlaringizni xavfsiz tarzda yetkazamiz. Sizga tez va halol hizmat taklif qilamiz.",
    "Yo'lovchilar uchun qulay muhit yaratganmiz. Konditsioner, toza salon va yo'lda tinchligiimizni his qiling. Har safar siz uchun eng yaxshi sharoit.",
    "Ertangi sayohatingiz uchun joyni endi band qiling. Eng yaxshi vaqt va o'rinlarni ushlang. @javohir_baxodirov bilan tezkor aloqada bo'ling.",
    "Haydovchilar uchun qo'shimcha daromad yo'li: kanalimiz bilan hamkorlik qiling. Yo'lovchilarni jalb qiling va transportingizni samarali ishlating. Birgalikda biznesni rivojlantiramiz.",
    "Payshanba tongi bahorona kayfiyat bilan boshlanadi. Beshariq - Qo'qon - Dangara yo'lida transportimiz tayyor. Sizga yoqimli va ishonchli safar kafolatlaymiz.",
    "Parcel va cargo xizmatimiz har doim faol. Toshkentga yuklarni tez va ishonchli yetkazamiz. Siz bandlikda bo'lsangiz ham, jo'natishni bizga topshiring.",
    "Safaringizda komfort muhim. Bizning servisimiz yo'lovchilarga qulaylik beradi. Salonga kirganingizda hammasi tartibli va toza bo'ladi.",
    "Ertangi yo'l uchun joyni oldindan band qiling. Ayni vaqtda eng yaxshi vaqtlar mavjud. Kanalimizdagi xabarlar orqali tez orada joy oling.",
    "Haydovchilarga tavsiya: siz ham daromadingizni oshiring. Beshariq yo'lovchilari bilan ishlash vaqti keldi. Taxi biznesini kengaytiring.",
    "Juma kuni yo'l holati yaxshi. Beshariq - Tashkent yo'nalishida yo'lda tinchlik va barqarorlik kuzatilmoqda. Sizning sayohatingiz uchun barcha sharoitlar tayyor.",
    "Cargo va parcel buyurtmalari uchun eng yaxshi vaqt. Yuklaringiz xavfsiz qo'lda va tez yetkaziladi. Bizga ishonch bildiring.",
    "Yo'lovchilar uchun muhitni yanada yaxshiladik. Konditsioner, toza o'rindiqlar va yaxshi xizmat sizni kutadi. Yo'l davomida dam oling.",
    "Ertangi safar uchun joylarni hozir band qiling. To'liq qulaylik bilan o'z rejangizni tuzing. @hushtam yordam beradi.",
    "Haydovchilar uchun yangi hamkorlik taklifi. Siz ham bu kanal orqali mijozlar topishingiz mumkin. Ishingizga barqarorlik kiritiladi.",
    "Shanba ertalabida yo'lga chiqish juda qulay. Beshariq - Qo'qon yo'nalishida avtotransportlar tayyor. Sizni xavfsiz va tez yetkazamiz.",
    "Parcel va cargo buyurtmalarini kechiktirmang. Paketlaringizni Toshkentga ishonchli yetkazishimiz mumkin. Har bir buyurtma ustuvor hisoblanadi.",
    "Sayohat paytidagi qulayliklarni his qiling. Bizning transportimiz yo'lovchilar uchun eng yaxshi shartlarni taqdim etadi. Har safar sizni xursand qilishga harakat qilamiz.",
    "Ertangi safar uchun joylaringizni hozirroq olishni maslahat beramiz. Bunday imkoniyatlar har kuni bo'lmasligi mumkin. Kanalimizda yangiliklarni kuzatib boring.",
    "Haydovchilar uchun imkoniyatlar kengaymoqda. Beshariq - Dangara yo'nalishida yo'lovchilar ko'p. Siz ham daromadingizni oshirishni boshlang.",
    "Yakshanba kuni sayohat uchun tinch dam olish kuni. Yo'lga chiqqaningizda hammasi tinch va shinam bo'ladi. Sizni ishonchli transport kutmoqda.",
    "Cargo va parcel xizmatimiz hafta oxirida ham ishlaydi. Yuklaringizni vaqtida yetkazib beramiz. Halol va tez xizmat bizning afzalliklarimizdan.",
    "Yo'lovchilar uchun juda qulay sharoit yaratamiz. Beshariqdan Tashkentga bo'lgan yo'nalishda saloon har doim toza bo'ladi. Siz dam olishingiz uchun hammasi tayyor.",
    "Ertangi sayohatni oxirgi daqiqada qoldirmang. Joylaringizni endi band qiling va yaxshi o'rinni tanlang. Kanalimizdagi xabarlar sizni qo'llab-quvvatlaydi.",
    "Haydovchilar uchun daromadni barqaror qilish mumkin. Yo'lovchilarni ko'proq jalb qilganda, daromadingiz ortadi. @javohir_baxodirov bilan bog'lanib, hamkorlikni boshlang."
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
            print(f"Telegram rate limit hit. Kutish {wait_seconds} soniya...")
            time.sleep(wait_seconds)
            continue

        if response.status_code != 200 or not response_data.get("ok", False):
            print(f"Failed to schedule message for {scheduled_datetime.isoformat()}")
            print(json.dumps(response_data, ensure_ascii=False, indent=2))
            return

        message_id = response_data["result"]["message_id"]
        print(f"Scheduled message {message_id} for {scheduled_datetime.strftime('%Y-%m-%d %H:%M')} Tashkent")
        return


if __name__ == "__main__":
    scheduled_datetimes = build_schedule_dates()

    if len(scheduled_datetimes) != len(POST_TEXTS):
        raise SystemExit("Scheduled times and post texts soni mos emas.")

    for scheduled_datetime, text in zip(scheduled_datetimes, POST_TEXTS):
        print(f"Rejalashtirish: {scheduled_datetime.strftime('%Y-%m-%d %H:%M')} | {text[:60]}...")
        send_scheduled_message(text, scheduled_datetime)
        time.sleep(REQUEST_DELAY_SECONDS)

    print("\nBarcha 35 ta post Telegramning schudle bo'limiga rejalashtirildi.")

# Requirements:
# pip install requests
