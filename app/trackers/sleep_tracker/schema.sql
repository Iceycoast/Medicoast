CREATE TABLE IF NOT EXISTS sleep_logs(
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date TEXT NOT NULL, 
    sleep_time TEXT NOT NULL,
    wake_time TEXT NOT NULL,
    duration REAL NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);