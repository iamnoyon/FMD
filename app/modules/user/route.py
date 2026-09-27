from fastapi import APIRouter, Depends, Query
from app.core.db import get_db
from sqlalchemy.orm import Session
from app.utils.token_service import get_current_user

from .schema import CreateUser
from .service import create_new_user, get_deliveryman_by_area


router = APIRouter(prefix='/user', tags=['User'])


@router.post('/create', description='Create a new user (admin)')
def create_user(
    req: CreateUser,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_new_user(req, db, current_user)


@router.get('/deliveryman', description='Get deliverymen by area')
def get_deliveryman(
    area: str = Query(..., min_length=1, description='Area name, e.g. mirpurdosh'),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_deliveryman_by_area(area, db)