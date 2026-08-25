from app.core.db import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response
from .schema import (
    RegisterSchema,
    RegisteredOtpVerified,
    ResendOTP,
    LoginSchema
)

from .service import (
    user_register,
    user_registered_otp_verified,
    resend_otp,
    user_login
)

router = APIRouter(prefix='/auth', tags=["Auth"])

@router.post('/register', description='New user registration')
def register(req: RegisterSchema, db: Session = Depends(get_db)):
    return user_register(req, db)

@router.post('/registerd/otp-verified', description='Registered user OTP verification')
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


@router.post('/resend-otp', description='Send OTP if user is already register. Use it in login and other')
def resend(req: ResendOTP, db: Session = Depends(get_db)):
    return resend_otp(req, db)


@router.post('/login', description='User login')
def login(req: LoginSchema, res: Response, db: Session = Depends(get_db)):
    token = user_login(req, db)

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


