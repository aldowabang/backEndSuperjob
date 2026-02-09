from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Memuat variabel dari file .env
load_dotenv()

# Mengambil URL Database dari environment variable
# Contoh format: postgresql://user:password@localhost:5432/superjob_db
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Create Engine: Mesin yang mengelola koneksi ke DB
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal: Setiap instance adalah database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: Kelas induk untuk semua Model kita (User, Job, dll)
Base = declarative_base()

# Dependency: Fungsi ini akan digunakan di Router untuk mendapatkan akses DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()