from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .models import models
from .schemas import schemas
from .db.database import engine, SessionLocal
from fastapi import FastAPI
from app.routers import auth, todo
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.exceptions.handlers import (
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler
)
from app.db.database import engine
from app.models import user
app = FastAPI()

# Create Tables
# models.Base.metadata.create_all(bind=engine)


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