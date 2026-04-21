from fastapi import APIRouter

router = APIRouter()

@router.get("/todos/")
def get_todos():
    return {"message": "Todos will be here"}