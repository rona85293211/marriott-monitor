import os
import requests

API_KEY = os.environ["RESEND_API_KEY"]

url = "https://api.resend.com/emails"

payload = {
    "from": "onboarding@resend.dev",
    "to": ["85293211@qq.com"],
    "subject": "GitHub 邮件测试",
    "html": "<p>如果你收到这封邮件，说明 Resend 邮件系统正常。</p>"
}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

r = requests.post(url, json=payload, headers=headers)

print(r.text)
