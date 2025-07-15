from datetime import datetime

def validate_date_format(v:str) -> str:
    try:
        datetime.strptime(v,"%Y-%m-%d")
    except ValueError:
        raise ValueError ("Date must be in this format YYYY-MM-DD")
    return v

def validate_time_format(v:str) -> str:
    try:
        datetime.strptime(v,"%H:%M")
    except ValueError:
        raise ValueError ("Time must be in this format HH:MM (24-hr)")
    return v

def validate_male_or_female(v:str) -> str:
    v = v.strip().lower()

    if v in ('male' ,'m'):
        return 'male'
    if v in ('female', 'f'):
        return 'female'
    else:
        raise ValueError ("Gender must be 'male' or 'female' (or M/F).")