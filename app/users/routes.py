from fastapi import APIRouter, HTTPException, status
from app.users.models import UserCreate, UserLogin, UserResponse
from . import controller
from app.auth.jwt import create_access_token

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate):
    return controller.register_user(user)

@router.post("/login")
def login(data: UserLogin):
    user = controller.login_user(data)
    access_token = create_access_token({"sub": user["user_id"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/check-username/{username}")
def check_username(username: str):
    return controller.check_username_availability(username)