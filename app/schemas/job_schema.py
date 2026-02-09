from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Schema dasar untuk Skill
class SkillSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

# Schema untuk Input Lowongan Baru
class JobCreate(BaseModel):
    title: str
    description: str
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    is_salary_hidden: bool = False
    city_id: int
    job_type_id: int
    work_model_id: int
    skill_ids: List[int] = [] # List ID skill yang dibutuhkan

# Schema untuk Response (apa yang dilihat user)
class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    salary_min: Optional[int]
    salary_max: Optional[int]
    is_salary_hidden: bool
    is_open: bool
    created_at: datetime
    
    # Menampilkan data relasi
    company_id: int
    city_id: int
    job_type_id: int
    work_model_id: int
    skills: List[SkillSchema] = []

    class Config:
        from_attributes = True