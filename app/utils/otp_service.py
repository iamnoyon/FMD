import os
import secrets
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

from app.modules.otp.model import OTP

load_dotenv()

from pwdlib import PasswordHash
pwd_context = PasswordHash.recommended()

#####################
def generate_otp() -> str:
    return f"{secrets.randbelow(100000):05d}"


def hash_otp(password: str) -> str:
    return pwd_context.hash(password)


def get_otp_expire_time() -> str:
    expireIn = os.getenv('OTP_EXPIRE_TIME')
    return datetime.now(timezone.utc) + timedelta(minutes=expireIn)


def verify_otp(otp, hash_otp) -> bool:
    return pwd_context.verify(otp, hash_otp)


def create_otp_record(phone):
    
    plan_otp = generate_otp()
    hashed_otp = hash_otp(plan_otp)
    expire_time = get_otp_expire_time()

    # Create new OTP
    new_otp_record = OTP(
        phone = phone,
        otp_hash = hashed_otp,
        verified = False,
        expire_at = expire_time
    )
    return (new_otp_record, plan_otp)