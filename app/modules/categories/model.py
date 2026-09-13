from app.core.db import Base
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

class Categories(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(autoincrement=True, index=True, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    image: Mapped[str] = mapped_column(nullable=True)
    icon: Mapped[str] = mapped_column(nullable=True)

    status: Mapped[bool] = mapped_column(Boolean, default=True)
    createdAt: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=datetime.utcnow)
    createdBy: Mapped[int] = mapped_column(nullable=True)

    updatedAt: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    updatedBy: Mapped[int] = mapped_column(nullable=True)