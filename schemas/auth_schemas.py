from pydantic import EmailStr, BaseModel
from typing import Any, Optional


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginUser(BaseModel):
    email: EmailStr
    password: str
    
