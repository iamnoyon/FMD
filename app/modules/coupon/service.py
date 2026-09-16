from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .model import Coupon
from .schema import CreateCoupon, UpdateCoupon, ApplyCoupon
from app.modules.product.model import Product
from datetime import datetime


def get_coupon_list(db: Session):
    try:
        coupons = db.query(Coupon).filter(Coupon.status == True).all()
        return {
            "success": True,
            "message": "Coupons retrieved successfully!",
            "data": coupons
        }
    except Exception:
        db.rollback()
        raise


def create_new_coupon(req: CreateCoupon, created_by: int, db: Session):
    try:
        new_coupon = Coupon(
            code=req.code,
            discount_amount=req.discount_amount,
            expire_at=req.expire_at,
            max_usage=req.max_usage,
            createdBy=created_by,
        )

        db.add(new_coupon)
        db.commit()
        db.refresh(new_coupon)

    except Exception:
        db.rollback()
        raise

    return {
        "success": True,
        "message": "Coupon is created successfully!",
        "data": new_coupon
    }


def get_coupon_by_id(id: int, db: Session):
    coupon = db.query(Coupon).filter(Coupon.id == id).first()

    if not coupon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coupon not found"
        )

    return {
        "success": True,
        "message": "Coupon retrieved by id",
        "data": coupon
    }


def update_coupon(id: int, req: UpdateCoupon, updated_by: int, db: Session):
    coupon = db.query(Coupon).filter(Coupon.id == id).first()

    if not coupon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coupon not found"
        )

    try:
        if req.code is not None:
            coupon.code = req.code
        if req.discount_amount is not None:
            coupon.discount_amount = req.discount_amount
        if req.expire_at is not None:
            coupon.expire_at = req.expire_at
        if req.max_usage is not None:
            coupon.max_usage = req.max_usage
        if req.status is not None:
            coupon.status = req.status

        coupon.updatedBy = updated_by

        db.commit()
        db.refresh(coupon)

    except Exception:
        db.rollback()
        raise

    return {
        "success": True,
        "message": "Coupon updated successfully!",
        "data": coupon
    }


def delete_coupon(id: int, db: Session):
    coupon = db.query(Coupon).filter(Coupon.id == id).first()

    if not coupon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coupon not found"
        )

    try:
        db.delete(coupon)
        db.commit()

    except Exception:
        db.rollback()
        raise

    return {
        "success": True,
        "message": "Coupon deleted successfully!",
    }


def apply_coupon(req: ApplyCoupon, db: Session):
    try:
        coupon = db.query(Coupon).filter(
            Coupon.code == req.coupon_code,
            Coupon.status == True
        ).first()

        if not coupon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Coupon not found"
            )

        if coupon.expire_at < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Coupon has expired"
            )

        if coupon.used_count >= coupon.max_usage:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Coupon usage limit reached"
            )

        items = []
        total = 0

        for item in req.products:
            product = db.query(Product).filter(Product.id == item.id).first()

            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with id {item.id} not found"
                )

            subtotal = product.price * item.quantity
            total += subtotal

            items.append({
                "product_id": product.id,
                "product_name": product.name,
                "product_price": product.price,
                "quantity": item.quantity,
                "subtotal": subtotal,
            })

        discount = min(coupon.discount_amount, total)
        final_price = total - discount

        coupon.used_count += 1
        db.commit()

        return {
            "success": True,
            "message": "Coupon applied successfully!",
            "data": {
                "coupon_id": coupon.id,
                "coupon_code": coupon.code,
                "items": items,
                "total": total,
                "final_price": final_price,
            }
        }

    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise
