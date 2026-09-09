def get_sms_payload(phone, otp):
    payload = {
        "phone": phone,
        "message": (
            f"FreshMilk: Your verification code is {otp}. "
            "It expires in 2 minutes. Please don't share this code with anyone."
        ),
    }

    return payload