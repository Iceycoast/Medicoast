from pydantic import ValidationError
from datetime import datetime

def validate_date_format(v:str) -> str:
    try:
        datetime.strptime(v,"%d-%m-%Y")
    except ValueError:
        raise ValueError ("Date must be in this format dd-mm-yyyy")
    return v

def validate_time_format(v:str) -> str:
    try:
        datetime.strptime(v,"%H:%M")
    except ValueError:
        raise ValueError ("Time must be in this format HH:MM (24-hr)")
    return v

