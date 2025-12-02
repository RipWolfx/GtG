from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Student, PersonalData, CareerData
from app.schemas import PersonalDataResponse, CareerDataResponse
from app.routers.auth import get_current_student

router = APIRouter()


@router.get("/{student_id}/personal-data", response_model=PersonalDataResponse)
async def get_personal_data(
    student_id: str,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Obtener datos personales del estudiante"""
    if current_student.id != student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a estos datos"
        )
    
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    
    personal_data = db.query(PersonalData).filter(PersonalData.student_id == student_id).first()
    if not personal_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Datos personales no encontrados"
        )
    
    return PersonalDataResponse(
        first_name=student.first_name,
        last_name=student.last_name,
        dni=student.dni,
        student_id=student.id,
        email=personal_data.email,
        phone=personal_data.phone,
        address=personal_data.address
    )


@router.get("/{student_id}/career-data", response_model=CareerDataResponse)
async def get_career_data(
    student_id: str,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Obtener datos de carrera del estudiante"""
    if current_student.id != student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a estos datos"
        )
    
    career_data = db.query(CareerData).filter(CareerData.student_id == student_id).first()
    if not career_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Datos de carrera no encontrados"
        )
    
    return career_data

