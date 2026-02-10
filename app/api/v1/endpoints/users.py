from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.crud import user_crud
from app.schemas import user_schema


router = APIRouter()

@router.post("/company", response_model=user_schema.CompanyResponse)
def setup_company_profile(
    company_in: user_schema.CompanyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Pastikan dia adalah employer
    if current_user.role != UserRole.employer:
        raise HTTPException(status_code=403, detail="Hanya Employer yang bisa membuat profil perusahaan")
    
    # Cek jika sudah ada profil perusahaan
    if current_user.company:
        raise HTTPException(status_code=400, detail="Profil perusahaan sudah ada")
        
    return user_crud.create_company(db, company_in, current_user.id)