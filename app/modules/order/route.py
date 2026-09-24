from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional
from app.core.db import get_db
from sqlalchemy.orm import Session
from app.utils.token_service import get_current_user
from .schema import CreateOrder, UpdateOrder, AssignBulkOrders, OrderStatus

from .service import (
    get_order_list,
    create_new_order,
    get_order_by_id,
    update_order,
    delete_order,
    assign_orders_bulk,
    get_orders_by_user,
)

router = APIRouter(prefix="/orders", tags=["Orders"])


def _require_admin(current_user: dict):
    if current_user.get("role") not in ("admin", "superadmin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )


@router.get("/list")
def order_list(
    page: Optional[int] = Query(None, ge=1),
    limit: Optional[int] = Query(None, ge=1, le=100),
    status_filter: Optional[OrderStatus] = Query(None, alias="status"),
    area: Optional[str] = Query(None, description="Filter by user area / location"),
    avenue: Optional[str] = Query(None, description="Filter by user avenue"),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_admin(current_user)
    return get_order_list(
        db,
        page=page,
        limit=limit,
        status_filter=status_filter,
        area=area,
        avenue=avenue,
    )


@router.post("/create")
def store_order(req: CreateOrder, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return create_new_order(req, current_user["id"], db)


@router.post("/assign-bulk")
def assign_bulk(req: AssignBulkOrders, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    _require_admin(current_user)
    return assign_orders_bulk(req.deliveryman_id, req.order_ids, current_user["id"], db)


@router.get("/my")
def my_orders(
    page: Optional[int] = Query(None, ge=1),
    limit: Optional[int] = Query(None, ge=1, le=100),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_orders_by_user(current_user["id"], db, page, limit)


@router.get("/by-user/{user_id}")
def orders_by_user(
    user_id: int,
    page: Optional[int] = Query(None, ge=1),
    limit: Optional[int] = Query(None, ge=1, le=100),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_admin(current_user)
    return get_orders_by_user(user_id, db, page, limit)


@router.get("/{id}")
def order_by_id(id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return get_order_by_id(id, db)


@router.put("/{id}")
def order_update(id: int, req: UpdateOrder, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return update_order(id, req, current_user["id"], db)


@router.delete("/{id}")
def order_delete(id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return delete_order(id, db)
