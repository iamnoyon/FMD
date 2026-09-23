from typing import Optional
from fastapi import APIRouter, Depends, Query
from app.core.db import get_db
from sqlalchemy.orm import Session
from app.utils.token_service import get_current_user
from .schema import CreateCategory, UpdateCategory

from .service import (
    get_category_list,
    create_new_category,
    get_category_by_id,
    update_category_by_id,
    delete_category_by_id
)

router = APIRouter(prefix='/categories', tags=['Categories'])

@router.get('/list')
def category_list(
    page: Optional[int] = Query(None, ge=1),
    limit: Optional[int] = Query(None, ge=1),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_category_list(db, page=page, limit=limit)


@router.post('/create')
def store_category(req: CreateCategory, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return create_new_category(req, db)


@router.get('/{id}')
def category_by_id(id, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_category_by_id(id, db);

@router.put('/{id}')
def update_category(id, req: UpdateCategory, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return update_category_by_id(id, req, db);


@router.delete('/{id}')
def delete_category(id, db: Session = Depends(get_db)):
    return delete_category_by_id(id, db);