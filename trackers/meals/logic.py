from db.database import get_connection
import os 

def initialize_meals_db():
    conn = get_connection()
    cursor = conn.cursor()

    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')

    try:
        with open(schema_path, 'r') as f:
            schema = f.read()

            cursor.executescript(schema)
        conn.commit()
    except FileNotFoundError:
        print(f"schema.sql not found at: {schema_path}")
    except Exception as e:
        print(f"Error initializing BMI DB: {e}")

    finally:
        conn.close()
def log_meal_entry(username:str, date:str, time:str, meal_name:str, calories:int, meal_type=None):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
                INSERT INTO meals_logs(username, date, time , meal_name, calories, meal_type)
                VALUES (?, ?, ?, ?, ?, ?)''', (username, date, time, meal_name, calories, meal_type))
        conn.commit()
        return f"Meal log added successfully"
    except Exception as e:
        return f"An error occured: {e}"
    finally:
        conn.close()

def get_meal_logs_by_user(username:str) -> list[tuple]:

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
                        SELECT * FROM meals_logs
                        WHERE username = ?
                        ORDER BY date DESC, time DESC
                        ''',(username,))
        data = cursor.fetchall()
        if not data:
            print(f"No Logs found for this user: {username}")
            return []
        return data
    except Exception as e:
        print(f"An error occured: {e}")
        return []
    finally:
        conn.close()

def get_total_calories_by_day(username:str, date:str) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
                        SELECT SUM(calories) FROM meals_logs
                        WHERE username = ? AND date = ?''',
                        (username,date))
        result = cursor.fetchone()
        return result[0] if result[0] else 0 
    except Exception as e:
        print(f"An error occured {e}")
        return 0
    finally:
        conn.close()
    
def delete_meal_entry(log_id:int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''DELETE FROM meals_logs WHERE id =?''',(log_id,))
        if cursor.rowcount == 0:
            return False
        else:
            conn.commit()
            print("Your entry has been deleted.")
            return True
    except Exception as e:
        print(f"An error occured: {e}")
        return False
    finally:
        conn.close()
    