from typing import Dict, Any
from hashlib import sha256

from jwt import encode, decode

import dotenv
import os

dotenv.load_dotenv()


def hash_password(password: str) -> str:
    """Returns hashed password"""
    salted = password + os.getenv('SALT')
    return sha256(salted.encode()).hexdigest()


def response(
    success: bool,
    message: str,
    data: Dict[str, Any] = {}
) -> Dict[str, Any]:
    """Creates a response that will be sent to the user"""
    return \
        {
            'success': success,
            'message': message,
            'data': data
        }


# ADD AN EXPIRATION
def create_token(userId: str) -> str:
    """Creates a JWT for authenticated user"""
    json = {
        'userId': userId
    }
    token = encode(
        payload=json,
        key=os.getenv('JWT'),
        algorithm='HS256'
    )
    return token


def validate_token(token: str) -> str | None:
    """Returns userId if valid token, else returns None"""
    try:
        return decode(token, os.getenv('JWT'), 'HS256')['userId']
    except Exception:
        return None
