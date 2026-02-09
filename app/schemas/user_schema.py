from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.models.user import UserRole

# Schema dasar (Data yang umum ada di setiap proses)
class UserBase(BaseModel):
    email: EmailStr

# Schema untuk pendaftaran User baru (Request)
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Password minimal 8 karakter")
    role: UserRole = UserRole.seeker

# Schema untuk mengupdate Profil
class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    resume_url_default: Optional[str] = None

# Schema untuk Response Profil
class ProfileResponse(BaseModel):
    full_name: str
    phone: Optional[str]
    bio: Optional[str]
    resume_url_default: Optional[str]

    class Config:
        from_attributes = True

# Schema untuk Response User (Data yang dikembalikan ke Client)
class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime
    profile: Optional[ProfileResponse] = None

    class Config:
        from_attributes = True # Mengizinkan Pydantic membaca data dari objek SQLAlchemy