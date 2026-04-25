from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.todo import Todo
from app.schemas.todo import TodoCreate
from app.config.security import get_current_user

router = APIRouter()

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ GET TODOS (Day 17 – FINAL)
@router.get("/todos/")
def get_todos(
    skip: int = 0,
    limit: int = 10,
    completed: bool = None,
    keyword: str = None,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    query = db.query(Todo).filter(Todo.user_id == user.id)

    if completed is not None:
        query = query.filter(Todo.completed == completed)

    if keyword:
        query = query.filter(Todo.title.ilike(f"%{keyword}%"))

    return query.offset(skip).limit(limit).all()


# ✅ UPDATE TODO
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

    if todo.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    todo.title = updated_title
    db.commit()
    db.refresh(todo)

    return todo


# ✅ DELETE TODO
@router.delete("/todos/{todo_id}")
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    if todo.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(todo)
    db.commit()

    return {"message": "Todo deleted successfully"}