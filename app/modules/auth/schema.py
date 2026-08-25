from pydantic import BaseModel, Field

class RegisterSchema(BaseModel):
    name: str = Field(default='Mr. John', max_length=20)
    