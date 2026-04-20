from pydantic import BaseModel

# Create schema (only title)
class TodoCreate(BaseModel):
    title: str


# Update schema (can change completed)
class TodoUpdate(BaseModel):
    title: str
    completed: bool


# Response schema
class TodoResponse(BaseModel):
    id: int
    title: str
    completed: bool

    class Config:
        from_attributes = True