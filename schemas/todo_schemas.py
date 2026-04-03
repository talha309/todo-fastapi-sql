from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class StandardResponse(BaseModel):
    status: str
    message: str
    data: Optional[Any] = None

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: bool = False
    created_at: Optional[datetime] = None

class UpdateTodo(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None
    
class ResponseTodo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: bool
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True