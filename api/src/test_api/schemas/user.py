from datetime import datetime
from pydantic import BaseModel

class UserBase(BaseModel):
    first_name: str
    last_name: str
    age: int
    date_of_birth: datetime

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
