import os
import requests

API_KEY = os.environ["RESEND_API_KEY"]

# 万豪查询链接
URL = "https://www.marriott.com.cn/reservation/availability.mi?propertyCode=ZQZEL&checkInDate=2026-03-07&checkOutDate=2026-03-08&roomCount=1&numAdultsPerRoom=1"

response = requests.get(URL)

html = response.text.lower()

# 判断是否有房
no_room_words = [
    "没有可用客房",
    "no availability",
    "sold out"
]

available = True

for w in no_room_words:
    if w in html:
        available = False

# 如果发现有房就发邮件
if available:

    payload = {
        "from": "onboarding@resend.dev",
        "to": ["85293211@qq.com"],
        "subject": "万豪酒店放房提醒",
        "text": "检测到酒店可能放房，请立即查看。"
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

    print("发现房间，已发送提醒")

else:
    print("当前没有房间")
