CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL CHECK(gender IN ('male', 'female')),
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    created_at TEXT NOT NULL
);

INSERT INTO sqlite_sequence (name , seq) VALUES ('users', 10000);