from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.todo import Todo
from app.schemas.todo import TodoCreate
from app.config.security import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/todos/")
def create_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    new_todo = Todo(
        title=todo.title,
        user_id=user.id   # ✅ link user
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo
@router.get("/todos/")
def get_todos(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return db.query(Todo).filter(Todo.user_id == user.id).all()