from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)

    # Relationship: Satu kota bisa memiliki banyak lowongan dan perusahaan
    jobs = relationship("Job", back_populates="city")
    companies = relationship("Company", back_populates="city")

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)

    # Relationship Many-to-Many ke Job akan didefinisikan di job.py via secondary table

class JobType(Base):
    __tablename__ = "job_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False) # Full-time, Part-time, dll

    jobs = relationship("Job", back_populates="job_type")

class WorkModel(Base):
    __tablename__ = "work_models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False) # Remote, On-site, Hybrid

    jobs = relationship("Job", back_populates="work_model")