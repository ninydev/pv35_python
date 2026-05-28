from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime
from typing import List, Optional

class RoleRead(BaseModel):
    id: int
    name: str
    
    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=1024)

class UserLogin(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    is_active: bool
    roles: List[RoleRead]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
