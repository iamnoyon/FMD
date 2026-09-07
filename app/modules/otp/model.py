from app.core.db import Base
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column 

class OTP(Base):
    __tablename__ = 'otps'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    phone: Mapped[str] = mapped_column(nullable=False)
    otp_hash: Mapped[str] = mapped_column(nullable=False)
    verified: Mapped[bool] = mapped_column(nullable=False, default=False)
    expire_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)