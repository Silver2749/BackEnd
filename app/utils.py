import jwt
from datetime import datetime, timedelta
from bcrypt import hashpw, checkpw, gensalt
from config import Config


def hash_password(password: str) -> str:   
    salt = gensalt()
    return hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    return checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(user_id: int, expires_delta: timedelta = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(hours=24)
    
    expire = datetime.utcnow() + expires_delta  #depr.
    payload = {
        "user_id": user_id,
        "exp": expire
    }
    token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm="HS256")
    return token


def verify_token(token: str) -> int:
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
        user_id: int = payload.get("user_id")
        if user_id is None:
            return None
        return user_id
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
