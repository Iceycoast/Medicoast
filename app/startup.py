import os
from app.db.database import get_connection
from app.config import DB_PATH

def ensure_db_exists():
    """Ensure the DB file and parent folder exist."""
    if not os.path.exists(DB_PATH):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def execute_schema(path: str):
    """Execute a schema file with error handling."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        with open(path, "r") as f:
            cursor.executescript(f.read())
        conn.commit()
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        raise
    finally:
        if 'conn' in locals():
            conn.close()

def load_all_schemas():
    """Ensure DB exists, then load all schema.sql files from app/ recursively."""
    ensure_db_exists()
    base_dir = "app"
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file == "schema.sql":
                schema_path = os.path.join(root, file)
                execute_schema(schema_path)
