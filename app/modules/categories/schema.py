from pydantic import BaseModel, Field
from typing import Optional


class CreateCategory(BaseModel):
    name: str = Field(default='Liqued Milk', max_length=100)
    image: Optional[str] = Field(default=None)
    icon: Optional[str] = Field(default=None)
    status: Optional[bool] = True


class UpdateCategory(BaseModel):
    name: Optional[str] = Field(default=None, max_length=100)
    image: Optional[str] = Field(default=None)
    icon: Optional[str] = Field(default=None)
    status: Optional[bool] = None