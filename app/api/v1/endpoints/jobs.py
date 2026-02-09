from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.crud import job_crud, user_crud
from app.schemas import job_schema
from app.core import security
from app.core.security import get_current_user
from app.models.user import User, UserRole

router = APIRouter()

@router.post("/", response_model=job_schema.JobResponse)
def post_new_job(
    job_in: job_schema.JobCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint bagi Employer untuk memposting lowongan kerja baru.
    """
    # 1. Cek apakah user adalah Employer
    if current_user.role != UserRole.employer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hanya Employer yang dapat memposting lowongan kerja."
        )
    # 2. Buat lowongan kerja baru
    if not current_user.company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employer harus memiliki perusahaan terdaftar sebelum memposting lowongan."
        )
    return job_crud.create_job(
        db=db, 
        job_in=job_in, 
        company_id=current_user.company.id
    )

@router.get("/", response_model=List[job_schema.JobResponse])
def read_jobs(db: Session = Depends(get_db)):
    """
    Endpoint untuk melihat semua lowongan kerja yang aktif.
    """
    return job_crud.get_jobs(db)