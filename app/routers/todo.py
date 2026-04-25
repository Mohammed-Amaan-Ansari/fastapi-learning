from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.db.database import SessionLocal
from app.models.todo import Todo
from app.schemas.todo import TodoCreate
from app.config.security import get_current_user

router = APIRouter()

# =========================
# DB Dependency
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# CREATE TODO
# =========================
@router.post("/todos/")
def create_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    new_todo = Todo(
        title=todo.title,
        user_id=user.id
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo


# =========================
# GET TODOS (Day 17)
# Pagination + Filter + Search
# =========================
@router.get("/todos/")
def get_todos(
    skip: int = 0,
    limit: int = 10,
    completed: Optional[bool] = None,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    query = db.query(Todo).filter(Todo.user_id == user.id)

    # Filter by completed
    if completed is not None:
        query = query.filter(Todo.completed == completed)

    # Search by title
    if keyword:
        query = query.filter(Todo.title.ilike(f"%{keyword}%"))

    # Pagination
    todos = query.offset(skip).limit(limit).all()

    return todos


# =========================
# UPDATE TODO
# =========================
@router.put("/todos/{todo_id}")
def update_todo(
    todo_id: int,
    updated_title: str,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Ownership check
    if todo.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    todo.title = updated_title
    db.commit()
    db.refresh(todo)

    return todo


# =========================
# DELETE TODO
# =========================
@router.delete("/todos/{todo_id}")
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Ownership check
    if todo.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(todo)
    db.commit()

    return {"message": "Todo deleted successfully"}