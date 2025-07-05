from db.database import get_connection
from auth.user_utils import hash_password
from datetime import datetime 
import sqlite3

def register_user(username, first_name, last_name, age, password, created_at):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            return "Username already Exists" 
        
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hashed_password = hash_password(password)

        cursor.execute('''
            INSERT INTO users (username, first_name, last_name, age, password, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, first_name, last_name if last_name else None, age, hashed_password, created_at))
        conn.commit()
        print(f"User '{username}' registerd succesfully!")
        return True
    
    except sqlite3.IntegrityError:
        print(f"Username '{username}' already exists. Please choose another.")
        return False
    
    except Exception as e:
        print(f"Registeration failed: {e}")
        return False
    finally:
        conn.close()


        
