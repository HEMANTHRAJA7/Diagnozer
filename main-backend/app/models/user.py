from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    model_config = {"populate_by_name": True}
    id: str = Field(alias="_id")
    created_at: datetime
    
class Token(BaseModel):
    access_token: str
    token_type: str
