from enum import Enum
from app.core.db import Base
from datetime import datetime
from sqlalchemy import String, DateTime, ARRAY, String
from sqlalchemy.orm import Mapped, mapped_column

class Role(str, Enum):
    ADMIN = 'admin'
    SUPERADMIN = 'superadmin'
    CUSTOMER = 'customer'
    DELIVERYMAN = 'deliveryman'

class AreaEnum(str, Enum):
    MIRPURDOSH = 'mirpurdosh'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(autoincrement=True, index=True, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[Role] = mapped_column(nullable=False, default=Role.CUSTOMER)

    area: Mapped[AreaEnum] = mapped_column(nullable=False, default=AreaEnum.MIRPURDOSH)
    avenue: Mapped[str] = mapped_column(nullable=False)
    road: Mapped[str] = mapped_column(nullable=False)
    house: Mapped[str] = mapped_column(nullable=False)
    flat: Mapped[str] = mapped_column(nullable=False)

    verified: Mapped[bool] = mapped_column(nullable=False, default=False)
    permissions: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False, default=list)

    createdAt: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=datetime.utcnow)
    createdBy: Mapped[str] = mapped_column(nullable=False, default='system')

    updatedAt: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    updatedBy: Mapped[str] = mapped_column(nullable=True)