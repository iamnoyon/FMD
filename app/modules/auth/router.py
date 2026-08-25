from app.core.db import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from .schema import RegisterSchema


from .service import user_register

router = APIRouter(prefix='/auth', tags=["Auth"])

@router.post('/register')
def register(req: RegisterSchema, db: Session = Depends(get_db)):
    return user_register(req, db)