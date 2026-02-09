from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

# Ambil dari .env atau gunakan default (hanya untuk dev)
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-jangan-lupa-diganti")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # Token berlaku 24 jam

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Mencocokkan password input dengan hash di database"""
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )

def get_password_hash(password: str) -> str:
    """Mengubah password teks biasa menjadi hash Bcrypt"""
    return bcrypt.hashpw(
        password.encode('utf-8'), 
        bcrypt.gensalt()
    ).decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Membuat Token JWT untuk login"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt