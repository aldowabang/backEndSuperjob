from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=True)
    logo_url = Column(String(255), nullable=True)

    # Relationships
    user = relationship("User", back_populates="company")
    city = relationship("City", back_populates="companies")
    jobs = relationship("Job", back_populates="company", cascade="all, delete-orphan")