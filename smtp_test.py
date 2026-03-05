
import smtplib
from email.message import EmailMessage

# ====== 在这里填写你的邮箱信息 ======

SMTP_HOST = "smtp.office365.com"      # 例如: smtp.gmail.com / smtp.qq.com
SMTP_PORT = 587                   # Gmail/QQ 通常是 587
SMTP_USER = "rona8529@outlook.com"
SMTP_PASS = "121211Rona"   # Gmail App Password 或 QQ 授权码

MAIL_TO = "85293211@qq.com"    # 收件邮箱


# ====== 邮件内容 ======

msg = EmailMessage()
msg["Subject"] = "SMTP Test Email"
msg["From"] = SMTP_USER
msg["To"] = MAIL_TO
msg.set_content("如果你收到这封邮件，说明SMTP配置成功。")


# ====== 发送邮件 ======

try:
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

    print("邮件发送成功！")

except Exception as e:
    print("邮件发送失败：")
    print(e)
