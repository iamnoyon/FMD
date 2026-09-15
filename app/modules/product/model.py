from app.core.db import Base
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, Float, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(autoincrement=True, index=True, primary_key=True)
    categoryId: Mapped[int] = mapped_column(Integer, ForeignKey('categories.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    weight_type: Mapped[str] = mapped_column(String(10), nullable=False)  # ml, liter, gm, kg
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    image: Mapped[str] = mapped_column(nullable=True)

    status: Mapped[bool] = mapped_column(Boolean, default=True)
    createdAt: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=datetime.utcnow)
    createdBy: Mapped[int] = mapped_column(nullable=True)

    updatedAt: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    updatedBy: Mapped[int] = mapped_column(nullable=True)
