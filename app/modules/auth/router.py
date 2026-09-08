from app.core.db import get_db
from sqlalchemy.orm import Session
from app.utils.token_service import get_current_user
from fastapi import APIRouter, Depends, Response, status
from .schema import (
    RegisterSchema,
    ResendOTP,
    LoginSchema,
    VerifyOTP
)
from .service import (
    user_register,
    resend_otp,
    user_login,
    otp_verify,
    get_user_details
)

router = APIRouter(prefix='/auth', tags=["Auth"])

@router.post('/register', description='New user registration')
def register(req: RegisterSchema, db: Session = Depends(get_db)):
    
    return user_register(req, db)


# if user already registerd then login with otp
@router.post('/login', description='After register otp verfied & login')
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
        "status_code": status.HTTP_200_OK,
        "token": token
    }


# if already registerd then resnd otp to the user for again login then call login api
@router.post('/resend-otp', description='OTP send to the registerd users')
def resend(req: ResendOTP, db: Session = Depends(get_db)):

    return resend_otp(req, db)


@router.post('/verify-otp', description='OTP verifying')
def otp_verificaiton(req: VerifyOTP, current_user = Depends(get_current_user), db: Session = Depends(get_db)):

    result =  otp_verify(req, db)
    if result:
        return {
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": "OTP verified"
        }

    return None


@router.post('/logout')
def logout(res: Response, current_user = Depends(get_current_user)):

    res.delete_cookie(
        key='access_token',
        path='/'
    )
    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": 'Logout done.'
    }


@router.get('/me', description='Get current user details')
def get_current_user_details(current_user = Depends(get_current_user), db: Session = Depends(get_db)):

    return get_user_details(current_user, db)