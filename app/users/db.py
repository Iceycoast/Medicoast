import sqlite3
from app.db.database import get_connection
from .models import UserCreate 

def insert_user_info(register:UserCreate, created_at:str ) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
                INSERT INTO users(username, first_name, last_name, age, gender, email, password, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                (register.username, register.first_name, register.last_name, register.age, register.gender, register.email, register.password, created_at))
        conn.commit()
        user_id = cursor.lastrowid

        if user_id is None:
            raise sqlite3.DatabaseError ("Failed to retrieve user_id")
        return user_id
    
    except sqlite3.IntegrityError as e:
        if "username" in str(e).lower():
            raise ValueError("Username already taken. Please choose another username.")
        
        elif "email" in str(e).lower():
            raise ValueError("An account already exists with this email.")
        
        else:
            raise ValueError ("Invalid details or user already exists")
    
    except sqlite3.DatabaseError as e:
        raise RuntimeError (f"An error occured while registering user: {e}")
    
    finally:
        conn.close()


def get_user_by_username(username: str) -> dict:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()

        if row is None:
            raise ValueError ("User not found.")
        return dict(row)
    
    finally:
        conn.close()