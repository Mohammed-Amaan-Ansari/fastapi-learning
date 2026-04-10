from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Pydantic Model
class Item(BaseModel):
    name: str
    price: float
    is_available: bool = True


# POST - Create item
@app.post("/items/")
def create_item(item: Item):
    return {
        "message": "Item created successfully",
        "item": item
    }


# PUT - Update item
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {
        "item_id": item_id,
        "updated_item": item
    }