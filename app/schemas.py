
from pydantic import BaseModel, Field, validator, EmailStr

class CalcRequest(BaseModel):
    a: float = Field(...)
    b: float = Field(...)
    op: str = Field(..., description="add|sub|mul|div")
    @validator("op")
    def valid_op(cls, v):
        if v not in {"add", "sub", "mul", "div"}:
            raise ValueError("op must be one of add|sub|mul|div")
        return v

class CalcResponse(BaseModel):
    result: float

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    class Config:
        from_attributes = True
