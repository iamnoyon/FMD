from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import random
import string
from .model import Order, OrderItem
from .schema import CreateOrder, UpdateOrder
from app.modules.product.model import Product
from app.modules.coupon.model import Coupon
from app.modules.user.model import User, Role
from datetime import datetime


def generate_order_number():
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"ORD-{suffix}"


def _validate_deliveryman(deliveryman_id: int, db: Session):
    user = db.query(User).filter(User.id == deliveryman_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {deliveryman_id} not found"
        )
    if user.role != Role.DELIVERYMAN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with id {deliveryman_id} is not a deliveryman"
        )
    return user


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
        subtotal = 0

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

            line_total = product.price * item.quantity
            subtotal += line_total

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

            discount = min(coupon.discount_amount, subtotal)
            coupon.used_count += 1
            coupon_code = coupon.code

        final_price = subtotal + req.delivery_fee - discount
        order_number = generate_order_number()

        while db.query(Order).filter(Order.order_number == order_number).first():
            order_number = generate_order_number()

        new_order = Order(
            order_number=order_number,
            user_id=created_by,
            subtotal=subtotal,
            delivery_fee=req.delivery_fee,
            total_price=final_price,
            discount_price=discount,
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
            "subtotal": order.subtotal,
            "delivery_fee": order.delivery_fee,
            "total_price": order.total_price,
            "discount_price": order.discount_price,
            "applied_coupon": order.applied_coupon,
            "deliveryman_id": order.deliveryman_id,
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


def assign_orders_bulk(deliveryman_id: int, order_ids: list, updated_by: int, db: Session):
    _validate_deliveryman(deliveryman_id, db)

    orders = db.query(Order).filter(Order.id.in_(order_ids)).all()
    found_ids = {o.id for o in orders}
    missing_ids = [oid for oid in order_ids if oid not in found_ids]

    if missing_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Orders not found: {missing_ids}"
        )

    try:
        for order in orders:
            order.deliveryman_id = deliveryman_id
            if order.status == 'pending':
                order.status = 'confirmed'
            order.updatedBy = updated_by

        db.commit()
    except Exception:
        db.rollback()
        raise

    return {
        "success": True,
        "message": f"Assigned {len(orders)} orders to deliveryman {deliveryman_id}",
        "data": {
            "deliveryman_id": deliveryman_id,
            "assigned_count": len(orders),
            "order_ids": list(found_ids),
        }
    }
