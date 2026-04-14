from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# In-memory database
todos = []

# Model
class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False


# CREATE
@app.post("/todos/")
def create_todo(todo: Todo):
    todos.append(todo)
    return {"message": "Todo created", "todo": todo}


# READ ALL
@app.get("/todos/")
def get_todos():
    return todos


# READ ONE
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


# UPDATE
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: Todo):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index] = updated_todo
            return {"message": "Todo updated", "todo": updated_todo}
    raise HTTPException(status_code=404, detail="Todo not found")


# DELETE
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            deleted = todos.pop(index)
            return {"message": "Todo deleted", "todo": deleted}
    raise HTTPException(status_code=404, detail="Todo not found")