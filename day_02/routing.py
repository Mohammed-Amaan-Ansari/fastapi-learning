from fastapi import FastAPI

app = FastAPI()

# Home route
@app.get("/")
def home():
    return {"message": "Welcome to Day 2 - Routing "}


# Path Parameter
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}


# Query Parameter
@app.get("/products/")
def get_product(name: str, price: float):
    return {
        "product_name": name,
        "price": price
    }


# POST request
@app.post("/create")
def create_item(name: str):
    return {"message": f"{name} created successfully"}


# PUT request
@app.put("/update/{item_id}")
def update_item(item_id: int, name: str):
    return {
        "item_id": item_id,
        "updated_name": name
    }


# DELETE request
@app.delete("/delete/{item_id}")
def delete_item(item_id: int):
    return {"message": f"Item {item_id} deleted"}