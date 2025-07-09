import sqlite3
from app.config import DB_PATH

def get_connection():
    """Returns a SQLite connection using the global DB_PATH, with threading disabled for FastAPI."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn