from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.utils.logger import logger
from .models import models
from .schemas import schemas
from .db.database import engine, SessionLocal
from fastapi import FastAPI
from app.routers import auth, todo
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.routers import upload
from fastapi.staticfiles import StaticFiles
from app.exceptions.handlers import (
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler
)
from app.db.database import engine
from app.models import user
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from app.routers import websocket
app = FastAPI()

# Create Tables
# models.Base.metadata.create_all(bind=engine)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

app.include_router(websocket.router)
@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={
            "success": False,
            "message": "Too many requests. Try again later."
        }
    )

user.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(todo.router)
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#  CREATE (using schema instead of query param)
@app.post("/todos/", response_model=schemas.TodoResponse)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    db_todo = models.Todo(title=todo.title)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


#  READ ALL
@app.get("/todos/", response_model=list[schemas.TodoResponse])
def get_todos(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
logger.info("🚀 FastAPI application started")

app.include_router(upload.router)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")