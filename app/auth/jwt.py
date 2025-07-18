from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from app.config import SECRET_KEY


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 

def create_access_token(data: dict, expires_delta: Optional[timedelta]= None):
    to_encode = data.copy()
    if expires_delta is None:
        expires_delta = timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    if not SECRET_KEY:
        raise RuntimeError("JWT_SECRET_KEY environment variable is not set!")
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        if not SECRET_KEY:
            raise RuntimeError ("JWT_SECRET_KEY environment variable is not set!")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None