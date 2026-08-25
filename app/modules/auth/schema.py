from pydantic import BaseModel, Field

class RegisterSchema(BaseModel):
    name: str = Field(default='Mr. John', max_length=20)
    phone: str = Field(default='01889010237', max_length=11, min_length=11)
    area: str = Field(default='mirpurdosh')
    avenue: str = Field(default='A')
    road: str = Field(default='10')
    house: str = Field(default='1240')
    flat: str = Field(default='B10')


class RegisteredOtpVerified(BaseModel):
    phone: str = Field(default='01889010239')
    otp: str = Field(default='12345')


class ResendOTP(BaseModel):
    phone: str = Field(default='01889010237')


class LoginSchema(BaseModel):
    phone: str = Field(default='01889010237')
    otp: str = Field(default='12345')