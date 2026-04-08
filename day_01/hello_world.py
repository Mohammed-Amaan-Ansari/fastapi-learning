from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello World - Day 1"}

@app.get("/about")
def about():
    return {"message": "This is my FastAPI learning journey"}