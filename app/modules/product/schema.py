from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class WeightType(str, Enum):
    ml = "ml"
    liter = "liter"
    gm = "gm"
    kg = "kg"


class CreateProduct(BaseModel):
    categoryId: int
    name: str = Field(max_length=200)
    description: Optional[str] = None
    weight: float = Field(gt=0)
    weight_type: WeightType
    quantity: int = Field(default=0, ge=0)
    price: float = Field(gt=0)
    image: Optional[str] = None


class UpdateProduct(BaseModel):
    categoryId: Optional[int] = None
    name: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = None
    weight: Optional[float] = Field(default=None, gt=0)
    weight_type: Optional[WeightType] = None
    quantity: Optional[int] = Field(default=None, ge=0)
    price: Optional[float] = Field(default=None, gt=0)
    image: Optional[str] = None
    status: Optional[bool] = None
