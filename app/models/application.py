from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Enum
from sqlalchemy.orm import relationship
import datetime
import enum
from app.database import Base

class ApplicationStatus(str, enum.Enum):
    applied = "applied"
    reviewed = "reviewed"
    interviewing = "interviewing"
    hired = "hired"
    rejected = "rejected"

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    
    # Snapshot CV saat melamar
    resume_url = Column(String(255), nullable=False)
    cover_letter = Column(Text, nullable=True)
    
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.applied, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")
    histories = relationship("ApplicationHistory", back_populates="application", cascade="all, delete-orphan")

class ApplicationHistory(Base):
    __tablename__ = "application_histories"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    
    status_from = Column(String(50), nullable=False)
    status_to = Column(String(50), nullable=False)
    notes = Column(Text, nullable=True) # Alasan penolakan atau catatan interview
    
    # Siapa yang mengubah (biasanya user dengan role employer/admin)
    changed_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    application = relationship("Application", back_populates="histories")
    author = relationship("User") # Untuk melihat siapa yang melakukan perubahan