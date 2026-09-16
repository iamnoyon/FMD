from fastapi import APIRouter, Depends
from app.core.db import get_db
from sqlalchemy.orm import Session
from app.utils.token_service import get_current_user
from .schema import CreateCoupon, UpdateCoupon, ApplyCoupon

from .service import (
    get_coupon_list,
    create_new_coupon,
    get_coupon_by_id,
    update_coupon,
    delete_coupon,
    apply_coupon,
)

router = APIRouter(prefix="/coupons", tags=["Coupons"])


@router.get("/list")
def coupon_list(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return get_coupon_list(db)


@router.post("/create")
def store_coupon(req: CreateCoupon, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return create_new_coupon(req, current_user["id"], db)


@router.get("/{id}")
def coupon_by_id(id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return get_coupon_by_id(id, db)


@router.put("/{id}")
def coupon_update(id: int, req: UpdateCoupon, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return update_coupon(id, req, current_user["id"], db)


@router.delete("/{id}")
def coupon_delete(id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return delete_coupon(id, db)


@router.post("/apply")
def apply_coupon_to_product(req: ApplyCoupon, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return apply_coupon(req, db)
