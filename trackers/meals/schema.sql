CREATE TABLE IF NOT EXISTS meals_logs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL, 
    meal_name TEXT NOT NULL,
    calories INTEGER NOT NULL,
    meal_type TEXT 
);