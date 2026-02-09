from sqlalchemy import Column, Integer, String, ForeignKey, Text, BigInteger, Boolean, DateTime, Table
from sqlalchemy.orm import relationship
import datetime
from app.database import Base

# Tabel Pivot untuk Many-to-Many antara Jobs dan Skills
job_skills = Table(
    "job_skills",
    Base.metadata,
    Column("job_id", Integer, ForeignKey("jobs.id"), primary_key=True),
    Column("skill_id", Integer, ForeignKey("skills.id"), primary_key=True)
)

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    title = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=False)
    
    # Gaji menggunakan BigInteger untuk menghindari overflow pada mata uang Rupiah
    salary_min = Column(BigInteger, nullable=True)
    salary_max = Column(BigInteger, nullable=True)
    is_salary_hidden = Column(Boolean, default=False)
    
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    job_type_id = Column(Integer, ForeignKey("job_types.id"), nullable=False)
    work_model_id = Column(Integer, ForeignKey("work_models.id"), nullable=False)
    
    is_open = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="jobs")
    city = relationship("City", back_populates="jobs")
    job_type = relationship("JobType", back_populates="jobs")
    work_model = relationship("WorkModel", back_populates="jobs")
    
    # Relationship Many-to-Many menggunakan secondary=job_skills
    skills = relationship("Skill", secondary=job_skills)
    
    # Relationship ke lamaran
    applications = relationship("Application", back_populates="job")