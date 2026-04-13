from fastapi import FastAPI, Depends, HTTPException

app = FastAPI()

# 🔹 Dependency function
def verify_token(token: str):
    if token != "secret123":
        raise HTTPException(status_code=401, detail="Invalid Token")
    return token


# 🔹 Using dependency in route
@app.get("/protected/")
def protected_route(token: str = Depends(verify_token)):
    return {"message": "Access granted", "token": token}


# 🔹 Another dependency
def get_username(username: str):
    return username


@app.get("/user/")
def get_user(username: str = Depends(get_username)):
    return {"username": username}