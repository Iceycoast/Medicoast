CREATE TABLE IF NOT EXISTS daily_ai_summaries (
    summary_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    summary TEXT NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE(user_id, date),
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);
