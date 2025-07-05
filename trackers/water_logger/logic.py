import os 
from db.database import get_connection

def initialize_water_db():
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
def log_water_entry(username:str, date:str, time:str, quantity:int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT INTO water_logs(username, date, time, quantity)
        VALUES (?, ?, ?, ?)
        ''',(username, date, time, quantity))
        conn.commit()
        return True
    except Exception as e:
        return f"An error occured: {e}"

    finally:
        conn.close()

def delete_water_entry(log_id:int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('DELETE FROM water_logs WHERE id = ?',(log_id,))
        if cursor.rowcount == 0:
             return False
        conn.commit()
        return True
    except Exception as e: 
        print(f"An error occured: {e}")
        return False
    finally:
        conn.close()
    

def get_water_logs_by_user(username:str) -> list[tuple]:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM water_logs WHERE username = ?', (username,))
        data = cursor.fetchall()
        if not data:
            print("No data")
            return []
        else:
            return data
    except Exception as e:
            print(f"An error occured: {e}")
            return []
    finally:
            conn.close()