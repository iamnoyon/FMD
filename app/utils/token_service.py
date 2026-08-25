from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import Cookie, Depends, HTTPException, status

SECRET_KEY = 'JWT_SECRET'
ALGORITHM = 'HS256'
TOKEN_EXPIRE_TIME = 365 #1 year

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
