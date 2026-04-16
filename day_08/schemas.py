from pydantic import BaseModel

# For creating todo
class TodoCreate(BaseModel):
    title: str

# For response
class TodoResponse(BaseModel):
    id: int
    title: str
    completed: bool

    class Config:
        from_attributes = True