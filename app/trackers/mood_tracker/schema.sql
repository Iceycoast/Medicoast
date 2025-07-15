CREATE TABLE IF NOT EXISTS mood_logs(
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL, 
    mood TEXT,
    note TEXT,
    ai_sentiment TEXT NOT NULL,
    ai_suggestion TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);