import secrets
from datetime import datetime, timezone, timedelta

from pwdlib import PasswordHash
hash = PasswordHash.recommended()

def generate_otp() -> str:
    return f"{secrets.randbelow(100000):05d}"


def hash_otp(password: str) -> str:
    return hash(password)


def get_otp_expire_time() -> str:
    # 5 min
    expireIn = '5'
    return datetime.now(timezone.utc) + timedelta(minutes=expireIn)