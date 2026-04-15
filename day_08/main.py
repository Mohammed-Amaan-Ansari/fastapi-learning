from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models
from .database import engine, SessionLocal

app = FastAPI()

# Create tables
models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE
@app.post("/todos/")
def create_todo(title: str, db: Session = Depends(get_db)):
    todo = models.Todo(title=title)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


# READ
@app.get("/todos/")
def get_todos(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()