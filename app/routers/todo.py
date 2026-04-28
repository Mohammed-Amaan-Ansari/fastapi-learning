from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List

from app.db.database import SessionLocal
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoResponse
from app.config.security import get_current_user
from app.utils.logger import logger

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# CREATE TODO
# =========================
@router.post("/todos/", response_model=TodoResponse)
def create_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    logger.info(f"User {user.id} creating todo: {todo.title}")

    new_todo = Todo(
        title=todo.title,
        completed=todo.completed,
        user_id=user.id
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo


# =========================
# GET TODOS
# =========================
@router.get("/todos/", response_model=List[TodoResponse])
def get_todos(
    skip: int = 0,
    limit: int = 10,
    completed: Optional[bool] = None,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    logger.info(f"User {user.id} fetching todos")

    query = db.query(Todo).filter(Todo.user_id == user.id)

    if completed is not None:
        query = query.filter(Todo.completed == completed)

    if keyword:
        query = query.filter(Todo.title.ilike(f"%{keyword}%"))

    return query.offset(skip).limit(limit).all()


# =========================
# UPDATE TODO
# =========================
@router.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    updated_title: str,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    logger.info(f"User {user.id} updating todo {todo_id}")

    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        logger.error(f"Todo {todo_id} not found")
        raise HTTPException(status_code=404, detail="Todo not found")

    if todo.user_id != user.id:
        logger.warning(f"Unauthorized update attempt by user {user.id}")
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
    logger.warning(f"User {user.id} deleting todo {todo_id}")

    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        logger.error(f"Todo {todo_id} not found")
        raise HTTPException(status_code=404, detail="Todo not found")

    if todo.user_id != user.id:
        logger.warning(f"Unauthorized delete attempt by user {user.id}")
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(todo)
    db.commit()

    return {"message": "Todo deleted successfully"}