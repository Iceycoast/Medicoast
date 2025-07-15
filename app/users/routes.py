from fastapi import APIRouter, status
from app.users.models import UserCreate, UserLogin, UserResponse
from . import controller

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model= UserResponse, status_code= status.HTTP_201_CREATED)
def register(user:UserCreate):
    return controller.register_user(user)

@router.post("/login", response_model= UserResponse)
def login(data: UserLogin):
    return controller.login_user(data)