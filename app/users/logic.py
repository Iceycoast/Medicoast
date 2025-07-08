import hashlib
import sqlite3
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from fastapi import HTTPException, status
from typing import Optional
from app.db.database import get_connection


# ---------------- Pydantic Models ---------------- #

class UserBase(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: Optional[str] = None
    age: int = Field(..., gt=12, lt=90)

class UserCreate(UserBase):
    username: str = Field(..., min_length=4)
    password: str = Field(..., min_length=8)

class UserResponse(UserBase):
    user_id: int
    username: str
    created_at: datetime

    class Config:
        orm_mode = True
        json_encoders = {datetime: lambda v: v.isoformat()}

class UserLogin(BaseModel):
    username: str
    password: str


# ---------------- Utility Functions ---------------- #

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# ---------------- Logic Functions ---------------- #

def register_user(user: UserCreate) -> UserResponse:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    hashed_pwd = hash_password(user.password)
    created_at = datetime.now(timezone.utc).isoformat()

    try:
        cursor.execute('''
            INSERT INTO users (username, first_name, last_name, age, password, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user.username, user.first_name, user.last_name, user.age, hashed_pwd, created_at))

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
        raise HTTPException(status_code=400, detail="Username already exists")

    finally:
        conn.close()


def login_user(data: UserLogin) -> UserResponse:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM users WHERE username = ?", (data.username,))
        row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        hashed_pwd = hash_password(data.password)

        if row["password"] != hashed_pwd:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

        return UserResponse(
            user_id=row["user_id"],
            username=row["username"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            age=row["age"],
            created_at=datetime.fromisoformat(row["created_at"])
        )

    finally:
        conn.close()
