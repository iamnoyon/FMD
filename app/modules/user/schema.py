from pydantic import BaseModel, Field
from typing import Optional
from app.modules.user.model import Role


class CreateUser(BaseModel):
    name: str = Field(default='Mr. John', max_length=20)
    phone: str = Field(default='01889010237', max_length=11, min_length=11)
    role: Role = Field(default=Role.CUSTOMER)
    area: str = Field(default='mirpurdosh')
    avenue: str = Field(default='A')
    road: str = Field(default='10')
    house: str = Field(default='1240')
    flat: str = Field(default='B10')


class UpdateUser(BaseModel):
    name: Optional[str] = Field(default=None, max_length=20)
    role: Optional[Role] = None
    area: Optional[str] = None
    avenue: Optional[str] = None
    road: Optional[str] = None
    house: Optional[str] = None
    flat: Optional[str] = None
    profile_image: Optional[str] = None