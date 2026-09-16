from fastapi import APIRouter, Depends
from app.core.db import get_db
from sqlalchemy.orm import Session
from app.utils.token_service import get_current_user
from .schema import CreateOrder, UpdateOrder

from .service import (
    get_order_list,
    create_new_order,
    get_order_by_id,
    update_order,
    delete_order,
)

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/list")
def order_list(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return get_order_list(db)


@router.post("/create")
def store_order(req: CreateOrder, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return create_new_order(req, current_user["id"], db)


@router.get("/{id}")
def order_by_id(id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return get_order_by_id(id, db)


@router.put("/{id}")
def order_update(id: int, req: UpdateOrder, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return update_order(id, req, current_user["id"], db)


@router.delete("/{id}")
def order_delete(id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return delete_order(id, db)
