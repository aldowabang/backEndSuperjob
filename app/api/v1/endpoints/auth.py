from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database import get_db
from app.crud import user_crud
from app.schemas import user_schema, auth_schema
from app.core import security

router = APIRouter()

@router.post("/register", response_model=user_schema.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_in: user_schema.UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint untuk pendaftaran user baru.
    """
    # 1. Cek apakah email sudah terdaftar
    db_user = user_crud.get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email sudah terdaftar. Silakan gunakan email lain."
        )
    
    # 2. Buat user baru
    return user_crud.create_user(db=db, user=user_in)


@router.post("/login", response_model=auth_schema.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """
    Endpoint Login standar OAuth2. 
    Field 'username' pada form_data harus diisi dengan 'email'.
    """
    # 1. Otentikasi user
    user = user_crud.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email atau password salah",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 2. Buat Access Token
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email, "role": user.role}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}