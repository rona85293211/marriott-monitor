import os
import requests

API_KEY = os.environ["RESEND_API_KEY"]

url = "https://api.resend.com/emails"

payload = {
    "from": "onboarding@resend.dev",
    "to": ["85293211@qq.com"],   # 这里改成你的QQ邮箱
    "subject": "万豪监控邮件测试",
    "text": "如果你收到这封邮件，说明QQ邮箱接收成功。"
}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)
