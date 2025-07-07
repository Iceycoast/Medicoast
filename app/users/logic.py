import hashlib
from datetime import datetime, timezone
from pydantic import BaseModel, Field
import sqlite3
from app.db.database import get_connection
from fastapi import HTTPException, status
from typing import Optional



class UserBase(BaseModel):
    first_name: str = Field(..., min_length= 1)
    last_name: Optional[str] = None
    age: int = Field(..., gt=12, lt=90)

class UserCreate(UserBase):
    username: str = Field(..., min_length=4)
    password: str = Field(..., min_length=8)

class UserResponse(UserBase):
    user_id: int
    username : str
    created_at : datetime

    class Config:
        orm_mode = True
        json_encoders = { datetime: lambda v : v.isoformat()}

class UserLogin(BaseModel):
    username: str
    password : str


def hash_password(password:str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def init_user_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
                CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT,
                age INTEGER NOT NULL,
                password TEXT NOT NULL,
                created_at TEXT NOT NULL)
    
    ''')
    conn.commit()
    conn.close()



def register_user(user: UserCreate) -> UserResponse:
    conn = get_connection()
    cursor = conn.cursor()

    hashed_pwd = hash_password(user.password)
    created_at = datetime.now(timezone.utc).isoformat()

    try:
        cursor.execute('''
                INSERT INTO users (username, first_name, last_name, age, password, created_at)
                VALUES (?, ?, ?, ?, ?, ?)''',
                (user.username, user.first_name, user.last_name, user.age, hashed_pwd, created_at))
        conn.commit()
        user_id = cursor.lastrowid
        if user_id is None:
            raise HTTPException(status_code=500, detail="Failed to retrieve user ID after registration")
        return UserResponse(
            user_id=user_id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            age=user.age,
            created_at=datetime.fromisoformat(created_at)
        )
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="username already exists")
    finally:
        conn.close()


def login_user(data: UserLogin) -> UserResponse:

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM users WHERE username = ? ", (data.username,))
        row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        hashed_pwd = hash_password(data.password)

        if row[5] != hashed_pwd:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

        return UserResponse(
                user_id= row[0],
                username= row[1],
                first_name= row[2],
                last_name= row[3],
                age = row[4],
                created_at= datetime.fromisoformat(row[6])
        )

    finally:
        conn.close()