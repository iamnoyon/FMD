from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import random
import string
from .model import Order, OrderItem
from .schema import CreateOrder, UpdateOrder
from app.modules.product.model import Product
from app.modules.coupon.model import Coupon
from datetime import datetime


def generate_order_number():
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"ORD-{suffix}"


def get_order_list(db: Session):
    try:
        orders = db.query(Order).all()
        return {
            "success": True,
            "message": "Orders retrieved successfully!",
            "data": orders
        }
    except Exception:
        db.rollback()
        raise


def create_new_order(req: CreateOrder, created_by: int, db: Session):
    try:
        items = []
        total = 0

        for item in req.products:
            product = db.query(Product).filter(Product.id == item.id).first()

            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with id {item.id} not found"
                )

            if product.quantity < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for product '{product.name}'"
                )

            subtotal = product.price * item.quantity
            total += subtotal

            items.append({
                "product": product,
                "quantity": item.quantity,
                "price": product.price,
            })

        discount = 0
        coupon_code = None

        if req.coupon_code:
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

            discount = min(coupon.discount_amount, total)
            coupon.used_count += 1
            coupon_code = coupon.code

        final_price = total - discount
        order_number = generate_order_number()

        while db.query(Order).filter(Order.order_number == order_number).first():
            order_number = generate_order_number()

        new_order = Order(
            order_number=order_number,
            user_id=created_by,
            total_price=final_price,
            applied_coupon=coupon_code,
            payment_method=req.payment_method.value,
            createdBy=created_by,
        )

        db.add(new_order)
        db.flush()

        for item in items:
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=item["product"].id,
                quantity=item["quantity"],
                price=item["price"],
            )
            db.add(order_item)
            item["product"].quantity -= item["quantity"]

        db.commit()
        db.refresh(new_order)

    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise

    return {
        "success": True,
        "message": "Order is created successfully!",
        "data": new_order
    }


def get_order_by_id(id: int, db: Session):
    order = db.query(Order).filter(Order.id == id).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()

    return {
        "success": True,
        "message": "Order retrieved by id",
        "data": {
            "id": order.id,
            "order_number": order.order_number,
            "user_id": order.user_id,
            "total_price": order.total_price,
            "applied_coupon": order.applied_coupon,
            "status": order.status,
            "items": items,
            "createdAt": order.createdAt,
            "updatedAt": order.updatedAt,
        }
    }


def update_order(id: int, req: UpdateOrder, updated_by: int, db: Session):
    order = db.query(Order).filter(Order.id == id).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    try:
        if req.status is not None:
            order.status = req.status.value

        order.updatedBy = updated_by

        db.commit()
        db.refresh(order)

    except Exception:
        db.rollback()
        raise

    return {
        "success": True,
        "message": "Order updated successfully!",
        "data": order
    }


def delete_order(id: int, db: Session):
    order = db.query(Order).filter(Order.id == id).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    try:
        db.query(OrderItem).filter(OrderItem.order_id == order.id).delete()
        db.delete(order)
        db.commit()

    except Exception:
        db.rollback()
        raise

    return {
        "success": True,
        "message": "Order deleted successfully!",
    }
