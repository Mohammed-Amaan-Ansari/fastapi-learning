from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Request Model
class UserCreate(BaseModel):
    name: str
    email: str
    password: str


# Response Model (NO password)
class UserResponse(BaseModel):
    name: str
    email: str


@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate):
    return user