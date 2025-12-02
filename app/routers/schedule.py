from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.models import Student, ScheduleEntry
from app.schemas import ScheduleResponse, ScheduleEntryResponse
from app.routers.auth import get_current_student

router = APIRouter()


@router.get("/{student_id}", response_model=ScheduleResponse)
async def get_schedule(
    student_id: str,
    schedule_date: date = Query(..., description="Fecha del horario (YYYY-MM-DD)"),
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Obtener horario del estudiante para una fecha específica"""
    if current_student.id != student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a este horario"
        )
    
    schedule_entries = db.query(ScheduleEntry).filter(
        ScheduleEntry.student_id == student_id,
        ScheduleEntry.date == schedule_date
    ).order_by(ScheduleEntry.start_time).all()
    
    if not schedule_entries:
        return ScheduleResponse(
            date=schedule_date,
            entries=[]
        )
    
    return ScheduleResponse(
        date=schedule_date,
        entries=[ScheduleEntryResponse.model_validate(entry) for entry in schedule_entries]
    )

