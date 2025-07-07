from fastapi import APIRouter, status
from app.users.logic import UserCreate, UserLogin, UserResponse, register_user, login_user

router = APIRouter()

@router.post("/register", response_model= UserResponse, status_code= status.HTTP_201_CREATED)
def register(user:UserCreate):
    return register_user(user)

@router.post("/login", response_model= UserResponse)
def login(data: UserLogin):
    return login_user(data)