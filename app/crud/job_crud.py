from sqlalchemy.orm import Session
from app.models.job import Job
from app.models.master import Skill
from app.schemas.job_schema import JobCreate

def create_job(db: Session, job_in: JobCreate, company_id: int):
    # 1. Buat objek Job (tanpa skills dulu)
    db_job = Job(
        title=job_in.title,
        description=job_in.description,
        salary_min=job_in.salary_min,
        salary_max=job_in.salary_max,
        is_salary_hidden=job_in.is_salary_hidden,
        city_id=job_in.city_id,
        job_type_id=job_in.job_type_id,
        work_model_id=job_in.work_model_id,
        company_id=company_id
    )
    
    # 2. Tambahkan Skills jika ada
    if job_in.skill_ids:
        skills = db.query(Skill).filter(Skill.id.in_(job_in.skill_ids)).all()
        db_job.skills = skills
    
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Job).filter(Job.is_open == True).offset(skip).limit(limit).all()