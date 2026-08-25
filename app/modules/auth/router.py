from app.core.db import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
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
def register_otp_verified(req: RegisteredOtpVerified, db: Session = Depends(get_db)):
    user_registered_otp_verified(req, db)