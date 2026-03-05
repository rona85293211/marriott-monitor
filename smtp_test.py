import os
import requests

API_KEY = os.environ["RESEND_API_KEY"]

HOTEL_URL = "https://www.marriott.com.cn/reservation/availability.mi?propertyCode=ZQZEL&checkInDate=2026-03-07&checkOutDate=2026-03-08&roomCount=1&numAdultsPerRoom=1"

response = requests.get(HOTEL_URL)

html = response.text.lower()

available = True

if "sold out" in html or "没有可用客房" in html or "no availability" in html:
    available = False

if available:
    payload = {
        "from": "onboarding@resend.dev",
        "to": ["85293211@qq.com"],
        "subject": "万豪酒店放房提醒",
        "text": "你监控的万豪酒店可能有房了，请尽快查看。"
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    requests.post(
        "https://api.resend.com/emails",
        json=payload,
        headers=headers
    )

    print("发现房间，已发送邮件")

else:
    print("暂时没有房间")
