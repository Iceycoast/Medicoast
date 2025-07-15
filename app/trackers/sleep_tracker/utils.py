from datetime import datetime, timedelta
from .models import SleepLogResponse
from sqlite3 import Row

def calculate_sleep_duration(sleep_time: str, wake_time: str) -> float:
    
    fmt = "%H:%M"
    t1 = datetime.strptime(sleep_time, fmt)
    t2 = datetime.strptime(wake_time, fmt)

    if t2 < t1:
        t2 += timedelta(days=1)

    duration_seconds = (t2 - t1).total_seconds()
    duration_hours = duration_seconds/3600
    return round(duration_hours, 2)
