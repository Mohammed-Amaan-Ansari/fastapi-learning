from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "user"   # optional

class UserResponse(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        from_attributes = True