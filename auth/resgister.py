from db.database import get_connection
from auth.user_utils import hash_password
from datetime import datetime 
import sqlite3

def create_user(username, first_name, last_name, age, password, created_at):
    conn = get_connection()
    cursor = conn.cursor()
    
    try: 
        cursor.execute('''
            INSERT INTO users (username, first_name, last_name, age, password, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, first_name, last_name if last_name else None, age, password, created_at))
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

def register_user():

    while True:

        print("\nRegister a new User")
        username = input("Choose a username: ").strip()
        first_name = input("Enter your first name: ").strip()
        last_name = input("Enter your last name: ").strip()
        if last_name == "":
            last_name = None

        try:
            age = int(input("Enter your age: ").strip())
        except ValueError:
            print("Invalid age. Must be a number.")
            continue
        
        password = input("Please choose a password: ").strip()
        hashed = hash_password(password)
        created_at = datetime.now().isoformat()

        success = create_user(username, first_name, last_name, age, hashed, created_at)

        if success:
            break
        else:
            print("Let's try again.\n")
        
