import os
import re

import requests
from dotenv import load_dotenv

from ..consumer import start_consuming

load_dotenv()


def format_phone(phone: str) -> str:
    cleaned = re.sub(r"[^\d]", "", phone)
    if cleaned.startswith("880"):
        return cleaned
    cleaned = re.sub(r"^(?:00)?88", "", cleaned)
    return f"88{cleaned}"


def handle_sms_message(data):
    phone = format_phone(data["phone"])
    message = data["message"]

    SMS_URL = os.getenv("SMS_API_URL")
    SMS_API_KEY = os.getenv("SMS_API_KEY")

    if not SMS_URL or not SMS_API_KEY:
        return

    payload = {
        "api_key": SMS_API_KEY,
        "msg": message,
        "to": phone,
    }

    print(payload)

    # try:
    #     response = requests.request("POST", SMS_URL, data=payload, timeout=10)
    #     response.raise_for_status()
    #     print("SMS sent successfully. Response:", response.text)
    # except requests.RequestException:
    #     pass


if __name__ == "__main__":
    start_consuming("sms_consumer", handle_sms_message)
