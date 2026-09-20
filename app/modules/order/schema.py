from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class OrderStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    delivered = "delivered"


class PaymentMethod(str, Enum):
    cash_on_delivery = "cash_on_delivery"
    bkash = "bkash"
    nagad = "nagad"
    card = "card"


class OrderProductItem(BaseModel):
    id: int
    quantity: int = Field(gt=0)


class CreateOrder(BaseModel):
    products: List[OrderProductItem]
    coupon_code: Optional[str] = Field(default=None, max_length=50)
    payment_method: PaymentMethod


class UpdateOrder(BaseModel):
    status: Optional[OrderStatus] = None


class AssignBulkOrders(BaseModel):
    deliveryman_id: int
    order_ids: List[int] = Field(min_length=1)
