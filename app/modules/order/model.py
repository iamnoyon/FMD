from app.core.db import Base
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, Float, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(autoincrement=True, index=True, primary_key=True)
    order_number: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    subtotal: Mapped[float] = mapped_column(Float, nullable=False)
    delivery_fee: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    coupon_value: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    total_price: Mapped[float] = mapped_column(Float, nullable=False)
    applied_coupon: Mapped[str] = mapped_column(String(50), nullable=True)
    payment_method: Mapped[str] = mapped_column(String(20), nullable=False)
    deliveryman_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default='pending')

    createdAt: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=datetime.utcnow)
    createdBy: Mapped[int] = mapped_column(nullable=True)

    updatedAt: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    updatedBy: Mapped[int] = mapped_column(nullable=True)


class OrderItem(Base):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(autoincrement=True, index=True, primary_key=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    createdAt: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=datetime.utcnow)
