from pydantic import BaseModel
from typing import Optional

class TodoCreate(BaseModel):
    title: str
    completed: Optional[bool] = False

class TodoResponse(BaseModel):
    id: int
    title: str
    completed: bool

    class Config:
        from_attributes = True