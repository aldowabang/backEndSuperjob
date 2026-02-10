from sqlalchemy.orm import Session
from app.models.user import User, Profile
from app.schemas.user_schema import UserCreate, CompanyCreate
from app.core.security import get_password_hash
from app.models.company import Company

def get_user_by_email(db: Session, email: str):
    """Mengecek apakah email sudah terdaftar"""
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    """Fungsi Registrasi: Membuat User dan Profil secara otomatis"""
    # 1. Hash password
    hashed_password = get_password_hash(user.password)
    
    # 2. Buat objek User
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit() # Simpan user dulu agar dapat ID
    db.refresh(db_user)
    
    # 3. Buat Profil kosong otomatis (Sangat membantu Frontend)
    # Nama diambil dari email sebelum simbol @ sebagai default
    default_name = user.email.split('@')[0]
    db_profile = Profile(
        user_id=db_user.id,
        full_name=default_name
    )
    db.add(db_profile)
    db.commit()
    
    return db_user

def create_company(db: Session, company_in: CompanyCreate, user_id: int):
    db_company = Company(
        **company_in.dict(),
        user_id=user_id
    )
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company