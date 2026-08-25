import os
from dotenv import load_dotenv
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import Cookie, Depends, HTTPException, status

load_dotenv()

SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = os.getenv('JWT_ALGORITHM')
TOKEN_EXPIRE_TIME = int(os.getenv('JWT_TOKEN_EXPIRE'))

def create_token(user_id, phone, role, permissions):
    expire = datetime.now(timezone.utc) + timedelta(days=TOKEN_EXPIRE_TIME)

    paylaod = {
        "id": str(user_id),
        "phone": phone,
        "role": role,
        "permissions": permissions,
        "exp": expire
    }

    return jwt.encode(paylaod, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expire token."
        )


def get_current_user(
        access_token: str | None = Cookie(default=None) 
):
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthenticated!'
        )

    return verify_token(access_token)

