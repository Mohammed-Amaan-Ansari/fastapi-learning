from fastapi import FastAPI, Query, Path

app = FastAPI()

# PATH PARAMETER
@app.get("/items/{item_id}")
def get_item(
    item_id: int = Path(..., gt=0, description="ID must be greater than 0")
):
    return {"item_id": item_id}


# QUERY PARAMETERS
@app.get("/products/")
def get_products(
    name: str,
    price: float = Query(..., gt=0),
    in_stock: bool = True
):
    return {
        "name": name,
        "price": price,
        "in_stock": in_stock
    }


# OPTIONAL QUERY PARAM
@app.get("/search/")
def search(q: str = None):
    if q:
        return {"search_query": q}
    return {"message": "No query provided"}


# DEFAULT VALUES
@app.get("/users/")
def get_users(limit: int = 10, skip: int = 0):
    return {
        "limit": limit,
        "skip": skip
    }


# COMBINED (PATH + QUERY)
@app.get("/orders/{order_id}")
def get_order(
    order_id: int,
    status: str = Query("pending", description="Order status")
):
    return {
        "order_id": order_id,
        "status": status
    }