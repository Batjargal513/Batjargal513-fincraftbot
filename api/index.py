from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
import os
import requests

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "fincraft2024")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

SYSTEM_PROMPT = """Та Актив Финкрафт ХХК-ийн Facebook Messenger чатботын туслах юм.
Та зөвхөн Актив Финкрафтын мэдээллийг ашиглан хариулна.
You also speak English if the user writes in English.

=== ACTIVE FINCRAFT INFO ===

COMPANY: Актив Финкрафт ХХК / Active Fincraft LLC
Tagline: Ensure Your Resource With Expert Care
Website: www.afc.mn | Email: info@afc.mn
Phone: (+976) 94-119733, (+976) 99-740716
Address: Соёмбо Тауэр, А блок, 14 давхар, #141, Сүхбаатар дүүрэг, 1-р хороо, Сөүлийн гудамж, Улаанбаатар

SERVICES:
1. Хөрөнгө оруулалтын судалгаа, шинжилгээ — Мэдээлэлд суурилсан шийдвэр гаргалт, стратегийн зөвлөмж, цаг хэмнэлт
2. Төсөл, ТЭЗҮ боловсруулах — Санал болгож буй төслийн цар хүрээ, зорилго, боломжит байдлыг нарийвчлан судлаж баримт бичгийг мэргэжлийн түвшинд бэлтгэх
3. Зах зээлийн болон салбарын судалгаа — Тодорхой зах зээл эсвэл салбарын чиг хандлага, боломж, тулгарч буй сорилтыг гүнзгийрүүлэн судлах
4. Захиалгат ажил, бусад үйлчилгээ — Харилцагчийн эрэлт хэрэгцээнд тулгуурласан захиалгат үйлчилгээ

=== COURSES ===

1. CFA LEVEL 1 БҮТЭН СУРГАЛТ
Зориулалт: CFA level I шалгалт өгөхөөр зорьж, санхүүгийн зах зээлд сонирхогч, хөрөнгийн зах зээлд ажилладаг болон сонирхогч, сурах эрмэлзэлтэй иргэд
Хугацаа: 5 сар, 240+ цаг
Төлбөр: ₮2,900,000
Хуваарь: Даваа & Лхагва 18:30-21:00, Бямба 10:00-14:00
Онцлог:
- "CFA Level 1" шалгалтанд бэлтгэх бүтэн сургалтын хөтөлбөр
- Ажлын бус цагаар, амралтын өдрүүдэд сургалтад хамрагдах
- Сургалтын төлбөрийн уян хатан нөхцөл
- Давтлага, тест ажиллах
Бүртгэл: https://forms.gle/e835MRyQvCdU3wBx5

2. CFA LEVEL 1 ХЭСЭГЧИЛСЭН СУРГАЛТ
Зориулалт: Ажиллаж ажлын бус цагаар сурч хөгжин өөрийн бүтээмжээ өгсөх, ур чадвараа нэмэгдүүлэх хүсч буй хүн бүрд
Хугацаа: 11 долоо хоног, 120+ цаг
Төлбөр: ₮1,600,000
Хуваарь: Даваа & Лхагва 18:30-21:00, Бямба 10:00-14:00
Онцлог:
- Мэргэжлийн гүн мэдлэгтэй болох
- Карьерын боломж нэмэгдэх
- Өндөр цалин ба тогтвортой байдал
- Олон улсад ажиллах боломж
- Шинжилгээний болон удирдлагын ур чадвар
Бүртгэл: https://forms.gle/e835MRyQvCdU3wBx5

3. ХБҮЦ СУРГАЛТ (Хөрөнгөөр Баталгаажсан Үнэт Цаас)
Хугацаа: 2 өдөр, 12 цаг
Төлбөр: ₮800,000
Давтамж: Улиралд 1 удаа
Бүртгэл: https://forms.gle/J7mFBeWSpGzw16UL6

=== TEACHERS ===

1. Б.ЖҮГДЭРРАГЧАА — CFA
Одоогийн албан тушаал: Актив Финкрафт ХХК Гүйцэтгэх захирал (2024-одоо)
Боловсрол:
- CFA program, CFA institute (2016-2021)
- МУИС — ЭЗС эдийн засагч (2000-2004)
Ажлын туршлага:
- Инвескор Ассет Менежмент УЦК ХХК Портфолио менежер (2022-2024)
- Макс импэкс ХХК, Төлөвлөлт, Санхүү Удирдлагын албаны дарга (2009-2018)
- Анод банк Байгууллагын Банкны газар, Ахлах эдийн засагч (2004-2009)
Мэргэжлийн холбооны гишүүнчлэл:
- CFA institute — Итгэмжлэгдсэн санхүүгийн шинжээч
- Монгол Улсын үнэт цаасны зах зээлд мэргэшлийн ажил, үйлчилгээ явуулах эрх, МУЦАЭХ (2022-одоо)

2. Д.ЭНХЦАЦРАЛ — CFA
Одоогийн албан тушаал: Титан Си Ар Эй ЗМС ХХК Гүйцэтгэх захирал (2021-одоо)
Боловсрол:
- CFA program, CFA institute (2016-2024)
- Мэргэшсэн кэуч, ICF итгэмжлэгдсэн сургалт
- Бизнес шинжээч мастер, Boston University (2018-2022)
Ажлын туршлага:
- Sumitomo-NEX PTE. LTD — Санхүү хариуцсан захирал, Сингапур (2020-2022)
- I-Cash Microfinance Ltd., SUMITOMO CORPORATION, Мьянмар (2019-2020)
- ACCION International — Судлаач, АНУ (2019)
- Мобиком ХХК — Корпорацын төлөвлөлтийн газрын захирал (2007-2018)
Мэргэжлийн холбооны гишүүнчлэл:
- CFA institute — Итгэмжлэгдсэн санхүүгийн шинжээч
- Mongolian Society of Financial analyst-ийн Удирдах зөвлөлийн гишүүн

3. С.БОЛОР-ЭРДЭНЭ — CFA
Одоогийн албан тушаал: Биржийн Бус Зах Зээлийн Бүртгэлийн хорооны гишүүн (2025-одоо)
Боловсрол:
- CFA Program (2017-2022)
- Санхүүгийн удирдлагын магистр, Macquarie Graduate School of Management (2007-2009)
- Бизнесийн удирдлагын бакалавр, Санхүү Эдийн Засгийн Дээд Сургууль (1996-2000)
Ажлын туршлага:
- Титан Си Ар Эй ЗМС ХХК-ийн Бизнес хөгжил хариуцсан захирал (2025)
- Стора Централ ХХК-ийн Үйл ажиллагаа хариуцсан захирал (2022-2024)
- Эн Экс Ти ХХК-ийн Үүсгэн байгуулагч, Гүйцэтгэх захирал (2016-2020)
- Их Монгол Группийн Бизнес хөгжил хариуцсан захирал орлогч (2001-2013)
Мэргэжлийн холбооны гишүүнчлэл:
- Монгол Улсын үнэт цаасны зах зээлд мэргэшлийн ажил үйлчилгээ явуулах эрх, МУЦАЭХ (2022-одоо)
- Олон улсын итгэмжлэгдсэн санхүүгийн шинжээч, CFA Institute (2022-одоо)

=== PAYMENT & POLICIES ===
- Суудал баталгаажуулахад хамгийн багадаа ₮800,000 төлнө
- Үлдэгдлийг 1 сарын хугацаанд төлнө
- Эрүүл мэндийн хүндэтгэн үзэх шалтгаанаас бусад тохиолдолд төлбөр буцаахгүй
- Дараагийн сургалт руу хойшлуулбал +10% нэмэлт төлбөр
- Нэг анги 15 хүнээр хязгаарлагдана
- Шалгалтанд тэнцэнэ гэсэн баталгаа байхгүй
- Дахин өгөх бол 50% хөнгөлөлттэй
- Онлайн ганцаарчилсан сургалт: 99021010

RULES:
- Reply in same language as user (Mongolian or English)
- Use emojis naturally
- Be warm and helpful
- For unknown questions suggest calling 94-119733
- Share registration links when relevant
"""

WELCOME = {
    "text": "Сайн байна уу! 👋 Актив Финкрафтад тавтай морилно уу! 💼\n\nБид санхүүгийн мэргэжилтнүүдийг бэлтгэдэг, CFA болон ХБҮЦ сургалт явуулдаг мэргэжлийн байгууллага юм.\n\nТа юуны талаар мэдэхийг хүсч байна вэ?",
    "quick_replies": [
        {"content_type": "text", "title": "📚 Сургалтууд", "payload": "TRAININGS"},
        {"content_type": "text", "title": "💰 Төлбөр", "payload": "PRICING"},
        {"content_type": "text", "title": "👨‍🏫 Багш нар", "payload": "TEACHERS"},
        {"content_type": "text", "title": "📅 Хуваарь", "payload": "SCHEDULE"},
        {"content_type": "text", "title": "📍 Байршил", "payload": "LOCATION"},
    ]
}

TOPICS = {
    "TRAININGS": "📚 Манай сургалтууд:\n\nБид 3 төрлийн сургалт явуулдаг:\n\n1️⃣ CFA Level 1 — Бүтэн сургалт\n🕐 5 сар, 240+ цаг | Сар бүр элсэлт\nCFA шалгалтанд бүрэн бэлтгэх хөтөлбөр. Давтлага, тест ажиллах боломжтой.\n\n2️⃣ CFA Level 1 — Хэсэгчилсэн сургалт\n🕐 11 долоо хоног, 120+ цаг | Сар бүр элсэлт\nАжиллаж байгаа хүмүүст зориулсан, карьер болон ур чадвараа хөгжүүлэх.\n\n3️⃣ ХБҮЦ сургалт\n🕐 2 өдөр, 12 цаг | Улиралд 1 удаа\nХөрөнгөөр баталгаажсан үнэт цаасны мэргэжлийн сургалт.\n\nДэлгэрэнгүй мэдэхийг хүсэх сургалтаа сонгоно уу 👇",
    "CFA_FULL": "🎓 CFA Level 1 — Бүтэн сургалт\n\n📌 Зориулалт:\nCFA шалгалт өгөхөөр зорьж буй, санхүүгийн зах зээлд сонирхогч болон ажилладаг иргэд\n\n⏱ Хугацаа: 5 сар, 240+ цаг\n📅 Хуваарь: Да, Лха 18:30-21:00 | Бямба 10:00-14:00\n👥 Анги: Хамгийн ихдээ 15 хүн\n🗓 Элсэлт: Сар бүр\n\n✅ Онцлог:\n• Бүтэн сургалтын хөтөлбөр\n• Ажлын бус цагаар сурах боломж\n• Давтлага, тест ажиллах\n• Уян хатан төлбөрийн нөхцөл\n\n📝 Бүртгүүлэх:\nhttps://forms.gle/e835MRyQvCdU3wBx5",
    "CFA_PARTIAL": "🎓 CFA Level 1 — Хэсэгчилсэн сургалт\n\n📌 Зориулалт:\nАжиллаж байгаа, ур чадвар болон карьераа хөгжүүлэх хүсэлтэй хүн бүрд\n\n⏱ Хугацаа: 11 долоо хоног, 120+ цаг\n📅 Хуваарь: Да, Лха 18:30-21:00 | Бямба 10:00-14:00\n👥 Анги: Хамгийн ихдээ 15 хүн\n🗓 Элсэлт: Сар бүр\n\n✅ Сургалт дуусгасны дараа:\n• Мэргэжлийн гүн мэдлэгтэй болно\n• Карьерын боломж нэмэгдэнэ\n• Өндөр цалин, тогтвортой байдал\n• Олон улсад ажиллах боломж\n• Шинжилгээний болон удирдлагын ур чадвар\n\n📝 Бүртгүүлэх:\nhttps://forms.gle/e835MRyQvCdU3wBx5",
    "HBUTS": "📊 ХБҮЦ сургалт\n(Хөрөнгөөр Баталгаажсан Үнэт Цаас)\n\n⏱ Хугацаа: 2 өдөр, 12 цаг\n🗓 Давтамж: Улиралд 1 удаа\n\nХөрөнгөөр баталгаажсан үнэт цаасны чиглэлээр мэргэжлийн мэдлэг эзэмших сургалт.\n\n📝 Бүртгүүлэх:\nhttps://forms.gle/J7mFBeWSpGzw16UL6",
    "PRICING": "💰 Сургалтын төлбөр:\n\n• CFA Бүтэн сургалт → ₮2,900,000\n• CFA Хэсэгчилсэн → ₮1,600,000\n• ХБҮЦ сургалт → ₮800,000\n\n💳 Төлбөрийн нөхцөл:\n• Суудал баталгаажуулахад ₮800,000 урьдчилгаа\n• Үлдэгдлийг 1 сарын хугацаанд төлнө\n• Хойшлуулбал +10% нэмэлт төлбөр\n• Эрүүл мэндийн шалтгаанаас бусад тохиолдолд буцаахгүй\n\n📞 Дэлгэрэнгүй: 94-119733",
    "TEACHERS": "👨‍🏫 Манай багш нар — Бүгд CFA эзэмшигч!\n\n1️⃣ Б.Жүгдэррагчаа — CFA\nГүйцэтгэх захирал | 20+ жилийн туршлага\nМУИС эдийн засагч, CFA (2016-2021)\nИнвескор Ассет Менежмент, Анод банк зэрэг байгууллагуудад ажилласан\n\n2️⃣ Д.Энхцацрал — CFA\nBoston University MBA | Сингапур, АНУ-д ажилласан\nCFA (2016-2024), ICF мэргэшсэн коуч\nSumitomo, ACCION International зэрэг олон улсын байгууллагуудад ажилласан\n\n3️⃣ С.Болор-Эрдэнэ — CFA\nMacquarie Graduate School магистр\nCFA (2017-2022) | 25+ жилийн туршлага\nБиржийн Бус Зах Зээлийн Бүртгэлийн хорооны гишүүн\n\nДэлгэрэнгүй мэдэхийг хүсэх багшаа сонгоно уу 👇",
    "TEACHER_1": "👤 Б.Жүгдэррагчаа — CFA\n\n🏢 Одоо: Актив Финкрафт ХХК Гүйцэтгэх захирал (2024-одоо)\n\n🎓 Боловсрол:\n• CFA program, CFA institute (2016-2021)\n• МУИС — ЭЗС эдийн засагч (2000-2004)\n\n💼 Ажлын туршлага:\n• Инвескор Ассет Менежмент УЦК — Портфолио менежер (2022-2024)\n• Макс импэкс ХХК — Санхүү Удирдлагын албаны дарга (2009-2018)\n• Анод банк — Ахлах эдийн засагч (2004-2009)\n\n🏅 Мэргэжлийн эрх:\n• CFA Institute итгэмжлэгдсэн санхүүгийн шинжээч\n• МУЦАЭХ мэргэшлийн эрх (2022-одоо)",
    "TEACHER_2": "👤 Д.Энхцацрал — CFA\n\n🏢 Одоо: Титан Си Ар Эй ЗМС ХХК Гүйцэтгэх захирал (2021-одоо)\n\n🎓 Боловсрол:\n• CFA program, CFA institute (2016-2024)\n• Бизнес шинжээч мастер, Boston University (2018-2022)\n• ICF итгэмжлэгдсэн мэргэшсэн коуч\n\n💼 Ажлын туршлага:\n• Sumitomo-NEX PTE. LTD — Санхүү захирал, Сингапур (2020-2022)\n• ACCION International — Судлаач, АНУ (2019)\n• Мобиком ХХК — Корпорацын захирал (2007-2018)\n\n🏅 Мэргэжлийн эрх:\n• CFA Institute итгэмжлэгдсэн санхүүгийн шинжээч\n• Mongolian Society of Financial Analysts — Удирдах зөвлөлийн гишүүн",
    "TEACHER_3": "👤 С.Болор-Эрдэнэ — CFA\n\n🏢 Одоо: Биржийн Бус Зах Зээлийн Бүртгэлийн хорооны гишүүн (2025-одоо)\n\n🎓 Боловсрол:\n• CFA Program (2017-2022)\n• Санхүүгийн удирдлагын магистр, Macquarie Graduate School (2007-2009)\n• Бизнесийн удирдлагын бакалавр, СЭЗДС (1996-2000)\n\n💼 Ажлын туршлага:\n• Титан Си Ар Эй ЗМС ХХК — Бизнес хөгжил захирал (2025)\n• Стора Централ ХХК — Үйл ажиллагаа захирал (2022-2024)\n• Эн Экс Ти ХХК — Үүсгэн байгуулагч, Гүйцэтгэх захирал (2016-2020)\n• Их Монгол Групп — Бизнес хөгжил захирал орлогч (2001-2013)\n\n🏅 Мэргэжлийн эрх:\n• CFA Institute олон улсын итгэмжлэл (2022-одоо)\n• МУЦАЭХ мэргэшлийн эрх (2022-одоо)",
    "SCHEDULE": "📅 Хичээлийн хуваарь:\n\n📌 Даваа гараг: 18:30 – 21:00\n📌 Лхагва гараг: 18:30 – 21:00\n📌 Бямба гараг: 10:00 – 14:00\n\n✅ Сар бүр шинэ элсэлт авдаг тул та хүссэн үедээ бүртгүүлж болно!\n\n💻 Ганцаарчилсан онлайн сургалт авах бол:\n📞 99021010",
    "LOCATION": "📍 Байршил:\n\nСоёмбо Тауэр, А блок, 14 давхар, #141\nСүхбаатар дүүрэг, 1-р хороо, Сөүлийн гудамж\nУлаанбаатар хот\n\n📞 Утас: 94-119733, 99-740716\n📧 Имэйл: info@afc.mn\n🌐 Вэбсайт: www.afc.mn",
    "ASK_AI": "🤖 Та асуултаа бичнэ үү, би хариулах болно! 💬",
}

TRAINING_MENU = {
    "text": "Аль сургалтын талаар дэлгэрэнгүй мэдэхийг хүсч байна вэ? 👇",
    "quick_replies": [
        {"content_type": "text", "title": "CFA Бүтэн", "payload": "CFA_FULL"},
        {"content_type": "text", "title": "CFA Хэсэгчилсэн", "payload": "CFA_PARTIAL"},
        {"content_type": "text", "title": "ХБҮЦ", "payload": "HBUTS"},
    ]
}

TEACHER_MENU = {
    "text": "Аль багшийн талаар дэлгэрэнгүй мэдэхийг хүсч байна вэ? 👇",
    "quick_replies": [
        {"content_type": "text", "title": "Б.Жүгдэррагчаа", "payload": "TEACHER_1"},
        {"content_type": "text", "title": "Д.Энхцацрал", "payload": "TEACHER_2"},
        {"content_type": "text", "title": "С.Болор-Эрдэнэ", "payload": "TEACHER_3"},
    ]
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
                "max_tokens": 400,
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

    if payload == "TRAININGS":
        send_msg(sender_id, {"text": TOPICS["TRAININGS"]})
        send_msg(sender_id, TRAINING_MENU)
        return

    if payload == "TEACHERS":
        send_msg(sender_id, {"text": TOPICS["TEACHERS"]})
        send_msg(sender_id, TEACHER_MENU)
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
