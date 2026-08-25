from app.core.db import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response
from .schema import RegisterSchema, RegisteredOtpVerified


from .service import (
    user_register,
    user_registered_otp_verified
)

router = APIRouter(prefix='/auth', tags=["Auth"])

@router.post('/register')
def register(req: RegisterSchema, db: Session = Depends(get_db)):
    return user_register(req, db)

@router.post('/registerd/otp-verified')
def register_otp_verified(req: RegisteredOtpVerified, res: Response, db: Session = Depends(get_db)):
    token = user_registered_otp_verified(req, db)

    res.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite='lax',
        max_age= 365 * 24 * 60 * 60,
        path='/'
    )

    return {
        "success": True,
        "status_code": 200,
        "token": token
    }