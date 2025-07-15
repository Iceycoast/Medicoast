from fastapi import HTTPException, status
from datetime import datetime, timezone
from typing import Optional
from .models import UserCreate, UserLogin, UserResponse
from .utils import hash_password, verify_password
from . import db 


def register_user(user: UserCreate) -> UserResponse:
    
    try:
        created_at = datetime.now(timezone.utc).isoformat()
        user.password = hash_password(user.password)
        user_id = db.insert_user_info(user, created_at)

        return UserResponse(
            user_id= user_id,
            username= user.username,
            first_name= user.first_name,
            last_name= user.last_name,
            age= user.age,
            gender= user.gender,
            email= user.email
        )
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
    except RuntimeError as re:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(re))
    
    
def login_user(data:UserLogin) -> UserResponse:

    try:
        user = db.get_user_by_username(data.username)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    if not verify_password(data.password, user['password']):
        raise HTTPException(status_code=401, detail="Incorrect Password.")
    
    return UserResponse(
            user_id= user['user_id'],
            username= user['username'],
            first_name= user['first_name'],
            last_name = user['last_name'],
            age = user['age'],
            gender= user['gender'],
            email = user['email']
        )
    
        
    
        