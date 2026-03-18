from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
import os
import requests

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "fincraft2024")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

SYSTEM_PROMPT = """Та Актив Финкрафт ХХК-ийн Facebook Messenger чатботын туслах юм.
Та зөвхөн Актив Финкрафтын мэдээллийг ашиглан хариулна. Хэрэв мэдэхгүй бол "94-119733 дугаарт залгана уу" гэж хэлнэ.
You also speak English if the user writes in English.

COMPANY: Актив Финкрафт ХХК / Active Fincraft LLC
Website: www.afc.mn | Email: info@afc.mn
Phone: (+976) 94-119733, (+976) 99-740716
Address: Соёмбо Тауэр, А блок, 14 давхар, #141, Улаанбаатар

TRAININGS:
1. CFA Level 1 бүтэн - 5 сар, 240+ цаг - 2,900,000 tugrug | Register: https://forms.gle/e835MRyQvCdU3wBx5
2. CFA Level 1 хэсэгчилсэн - 11 долоо хоног, 120+ цаг - 1,600,000 tugrug | Register: https://forms.gle/e835MRyQvCdU3wBx5
3. ХБҮЦ сургалт - 2 өдөр, 12 цаг - 800,000 tugrug | Register: https://forms.gle/J7mFBeWSpGzw16UL6

SCHEDULE: Даваа & Лхагва 18:30-21:00, Бямба 10:00-14:00
PAYMENT: Min deposit 800,000 tugrug, rest within 1 month. No refunds except medical.
CLASS SIZE: Max 15 students
ONLINE: Individual sessions - call 99021010
POSTPONE: +10% fee
PASS GUARANTEE: No guarantee. Retake = 50% discount.
TEACHERS: Б.Жүгдэррагчаа CFA, Д.Энхцацрал CFA, С.Болор-Эрдэнэ CFA

RULES:
- Short replies max 3-4 sentences
- Use emojis
- Reply in same language as user
- Share registration links when relevant
- Unknown questions: suggest calling 94-119733
"""

WELCOME = {
    "text": "Сайн байна уу! 👋 Актив Финкрафтад тавтай морилно уу! 💼\n\nТа юуны талаар мэдэхийг хүсч байна вэ?",
    "quick_replies": [
        {"content_type": "text", "title": "📚 Сургалтууд", "payload": "TRAININGS"},
        {"content_type": "text", "title": "💰 Төлбөр", "payload": "PRICING"},
        {"content_type": "text", "title": "📅 Хуваарь", "payload": "SCHEDULE"},
        {"content_type": "text", "title": "📍 Байршил", "payload": "LOCATION"},
        {"content_type": "text", "title": "🤖 Асуулт асуух", "payload": "ASK_AI"},
    ]
}

TOPICS = {
    "TRAININGS": "📚 Манай сургалтууд:\n\n1️⃣ CFA Level 1 Бүтэн (5 сар, 240+ цаг) - 2,900,000 tugrug\n2️⃣ CFA Level 1 Хэсэгчилсэн (11 долоо хоног) - 1,600,000 tugrug\n3️⃣ ХБҮЦ (2 өдөр, 12 цаг) - 800,000 tugrug\n\nДэлгэрэнгүй мэдэхийг хүсвэл асуугаарай! 😊",
    "PRICING": "💰 Төлбөр:\n\n• CFA Бүтэн - 2,900,000 tugrug\n• CFA Хэсэгчилсэн - 1,600,000 tugrug\n• ХБҮЦ - 800,000 tugrug\n\n💳 Суудал баталгаажуулахад 800,000 tugrug урьдчилгаа төлнө. Үлдэгдлийг 1 сарын хугацаанд төлж болно 😊",
    "SCHEDULE": "📅 Хуваарь:\n\n📌 Даваа: 18:30-21:00\n📌 Лхагва: 18:30-21:00\n📌 Бямба: 10:00-14:00\n\n✅ Сар бүр шинэ элсэлт авдаг!",
    "LOCATION": "📍 Байршил:\n\nСоёмбо Тауэр, А блок, 14 давхар, #141\nСүхбаатар дүүрэг, 1-р хороо, Сөүлийн гудамж\n\n📞 94-119733, 99-740716\n🌐 www.afc.mn",
    "ASK_AI": "🤖 Та асуултаа бичнэ үү, би хариулах болно! 💬",
}

FOLLOW_UP = {
    "text": "Өөр зүйл мэдэхийг хүсч байна уу? 👇",
    "quick_replies": [
        {"content_type": "text", "title": "📚 Сургалтууд", "payload": "TRAININGS"},
        {"content_type": "text", "title": "💰 Төлбөр", "payload": "PRICING"},
        {"content_type": "text", "title": "📋 Үндсэн цэс", "payload": "MENU"},
    ]
}


def send_msg(recipient_id, message_data):
    if not PAGE_ACCESS_TOKEN:
        return
    try:
        requests.post(
            f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}",
            json={"recipient": {"id": recipient_id}, "message": message_data, "messaging_type": "RESPONSE"},
            timeout=5
        )
    except Exception:
        pass


def send_typing(recipient_id):
    if not PAGE_ACCESS_TOKEN:
        return
    try:
        requests.post(
            f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}",
            json={"recipient": {"id": recipient_id}, "sender_action": "typing_on"},
            timeout=3
        )
    except Exception:
        pass


def ask_groq(question):
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": question}
                ],
                "max_tokens": 250,
                "temperature": 0.5
            },
            timeout=10
        )
        return r.json()["choices"][0]["message"]["content"]
    except Exception:
        return "Уучлаарай, одоогоор асуудал гарлаа 😅 94-119733 дугаарт залгана уу!"


def handle_message(sender_id, message):
    text = message.get("text", "").strip()
    quick_reply = message.get("quick_reply", {})
    payload = quick_reply.get("payload", "") if quick_reply else ""

    send_typing(sender_id)

    greetings = ["hi", "hello", "hey", "start", "menu", "help",
                 "сайн", "сайн байна", "байна уу", "мэнд", ""]

    if payload == "MENU" or text.lower() in greetings:
        send_msg(sender_id, WELCOME)
        return

    if payload in TOPICS:
        send_msg(sender_id, {"text": TOPICS[payload]})
        send_msg(sender_id, FOLLOW_UP)
        return

    ai_reply = ask_groq(text)
    send_msg(sender_id, {"text": ai_reply})
    send_msg(sender_id, FOLLOW_UP)


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            mode = params.get("hub.mode", [None])[0]
            token = params.get("hub.verify_token", [None])[0]
            challenge = params.get("hub.challenge", [None])[0]

            if mode == "subscribe" and token == VERIFY_TOKEN:
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(challenge.encode())
            else:
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(b"FinancraftBot is running!")
        except Exception:
            self.send_response(500)
            self.end_headers()

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            data = json.loads(body)
            if data.get("object") == "page":
                for entry in data.get("entry", []):
                    for event in entry.get("messaging", []):
                        sender_id = event["sender"]["id"]
                        if "message" in event:
                            handle_message(sender_id, event["message"])
        except Exception:
            pass
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')

    def log_message(self, format, *args):
        pass
