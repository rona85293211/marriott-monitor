import os
import json
import requests
from datetime import datetime, timezone

# ====== 你要监控的参数（按需改）======
PROPERTY_CODE = "ZQZEL"                 # 酒店code（你这个是崇礼 Element）
CHECKIN_DATE = "2026-03-09"            # 入住日期 YYYY-MM-DD
CHECKOUT_DATE = "2026-03-10"           # 退房日期 YYYY-MM-DD
ROOM_COUNT = "1"
ADULTS_PER_ROOM = "1"
CHILDREN_COUNT = "0"

# ====== Resend 配置（从 GitHub Secrets 读取）======
RESEND_API_KEY = os.environ["RESEND_API_KEY"]
MAIL_TO = os.environ["MAIL_TO"]         # 你的QQ邮箱（或任何邮箱）
MAIL_FROM = os.environ.get("MAIL_FROM", "onboarding@resend.dev")  # testing模式用这个

STATE_FILE = "state.json"

BASE_URL = "https://www.marriott.com.cn/reservation/availability.mi"
QUERY_URL = (
    f"{BASE_URL}"
    f"?propertyCode={PROPERTY_CODE}"
    f"&checkInDate={CHECKIN_DATE}"
    f"&checkOutDate={CHECKOUT_DATE}"
    f"&roomCount={ROOM_COUNT}"
    f"&numAdultsPerRoom={ADULTS_PER_ROOM}"
    f"&childrenCount={CHILDREN_COUNT}"
    f"&useRewardsPoints=false"
    f"&showErrors=true"
    f"&useRequestCriteria=true"
    f"&isSearch=true"
)

NO_ROOM_MARKERS = [
    "没有可用客房",
    "无可用客房",
    "已售完",
    "sold out",
    "no availability",
    "no rooms available",
]

YES_ROOM_MARKERS = [
    "查看房价",
    "选择客房",
    "view rates",
    "select room",
]


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_state():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"last_status": "UNKNOWN"}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def detect_availability(html: str) -> bool:
    h = html.lower()

    # 明确无房文案
    if any(m.lower() in h for m in NO_ROOM_MARKERS):
        return False

    # 明确有房按钮/文案（更强信号）
    if any(m.lower() in h for m in YES_ROOM_MARKERS):
        return True

    # 兜底：既没看到无房，也没看到明显有房，就当无房（保守，减少误报）
    return False


def send_email_resend(subject: str, text: str):
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "from": MAIL_FROM,
        "to": [MAIL_TO],
        "subject": subject,
        "text": text,
    }
    r = requests.post(url, json=payload, headers=headers, timeout=30)
    print("[resend]", r.status_code, r.text)
    r.raise_for_status()


def main():
    state = load_state()
    last_status = state.get("last_status", "UNKNOWN")

    print("[info] checking:", QUERY_URL)
    resp = requests.get(
        QUERY_URL,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        },
        timeout=45,
    )
    resp.raise_for_status()

    available = detect_availability(resp.text)
    status = "AVAILABLE" if available else "NO_AVAIL"

    print("[check]", {"time_utc": utc_now(), "status": status, "last": last_status})

    # 只在“无房 -> 有房”时提醒一次
    if last_status in ("UNKNOWN", "NO_AVAIL") and status == "AVAILABLE":
        subject = f"万豪放房提醒：{PROPERTY_CODE} {CHECKIN_DATE}→{CHECKOUT_DATE}"
        text = (
            f"检测到可能放房！\n\n"
            f"酒店：{PROPERTY_CODE}\n"
            f"日期：{CHECKIN_DATE} → {CHECKOUT_DATE}\n"
            f"人数：{ROOM_COUNT}间 / 每间{ADULTS_PER_ROOM}成人 / {CHILDREN_COUNT}儿童\n\n"
            f"打开查看：{QUERY_URL}\n\n"
            f"(UTC) {utc_now()}\n"
        )
        send_email_resend(subject, text)
        print("[notify] sent")

    # 保存本次状态
    state.update({"last_status": status, "last_checked_utc": utc_now()})
    save_state(state)


if __name__ == "__main__":
    main()
