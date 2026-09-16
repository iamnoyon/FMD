from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CreateCoupon(BaseModel):
    code: str = Field(max_length=50)
    discount_amount: float = Field(gt=0)
    expire_at: datetime
    max_usage: int = Field(gt=0)


class UpdateCoupon(BaseModel):
    code: Optional[str] = Field(default=None, max_length=50)
    discount_amount: Optional[float] = Field(default=None, gt=0)
    expire_at: Optional[datetime] = None
    max_usage: Optional[int] = Field(default=None, gt=0)
    status: Optional[bool] = None


class CouponProductItem(BaseModel):
    id: int
    quantity: int = Field(gt=0)


class ApplyCoupon(BaseModel):
    coupon_code: str = Field(max_length=50)
    products: List[CouponProductItem]
