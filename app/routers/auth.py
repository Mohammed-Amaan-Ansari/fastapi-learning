from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.user import User
from app.config.security import get_current_user
from fastapi import Depends
from app.schemas.user import UserCreate, UserLogin, Token
from app.config.security import hash_password, verify_password, create_access_token

router = APIRouter()

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# REGISTER
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        username=user.username,
        password=hash_password(user.password),
        role=user.role   # ✅ add role
    )

    db.add(new_user)
    db.commit()
    return {"message": "User created"}


# LOGIN
@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
    "sub": db_user.username,
    "role": db_user.role
})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/protected")
def protected_route(user: str = Depends(get_current_user)):
    return {
        "message": "You are authorized",
        "user": user
    }
@router.get("/user-data")
def user_data(user = Depends(get_current_user)):
    return {"message": "User access", "user": user}
from app.config.security import require_role

@router.delete("/admin-only")
def admin_only(user = Depends(require_role("admin"))):
    return {"message": "Admin access granted"}