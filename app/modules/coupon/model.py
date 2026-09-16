from app.core.db import Base
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column


class Coupon(Base):
    __tablename__ = 'coupons'

    id: Mapped[int] = mapped_column(autoincrement=True, index=True, primary_key=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    discount_amount: Mapped[float] = mapped_column(Float, nullable=False)
    expire_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    max_usage: Mapped[int] = mapped_column(Integer, nullable=False)
    used_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    status: Mapped[bool] = mapped_column(Boolean, default=True)
    createdAt: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=datetime.utcnow)
    createdBy: Mapped[int] = mapped_column(nullable=True)

    updatedAt: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    updatedBy: Mapped[int] = mapped_column(nullable=True)
