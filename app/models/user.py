from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
import datetime
from app.database import Base
import enum

class UserRole(str, enum.Enum):
    seeker = "seeker"
    employer = "employer"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.seeker, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationship
    # uselist=False memastikan hubungan One-to-One
    profile = relationship("Profile", back_populates="user", uselist=False)
    company = relationship("Company", back_populates="user", uselist=False)
    applications = relationship("Application", back_populates="user")
    notifications = relationship("Notification", back_populates="user")

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    bio = Column(String, nullable=True)
    resume_url_default = Column(String(255), nullable=True) # Link ke CV utama

    # Relationship
    user = relationship("User", back_populates="profile")