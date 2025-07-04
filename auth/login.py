from db.database import get_connection
from auth.user_utils import hash_password

def authenticate_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()

        if not user:
            print("Username not found")
            return None
        
        hashed = hash_password(password)
        if user[4] == hashed:
            print(f" Welcome back, {user[1]}!")
            return user
        else: 
            print("Incorrect password")
            return None
        
    except Exception as e:
        print(f"Login failed: {e}")
        return None
    
    finally:
        conn.close()

def login_user():
    print("\nLogin to your account")

    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    user = authenticate_user(username, password)

    if user:
        return user
    else:
        print("Login Failed.\n")
        return None