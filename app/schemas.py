from pydantic import BaseModel, EmailStr
from datetime import date, time
from typing import Optional, List

class LoginRequest(BaseModel):
    student_id: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    student_id: str
    student_name: str

class PersonalDataResponse(BaseModel):
    first_name: str
    last_name: str
    dni: str
    student_id: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None

    class Config:
        from_attributes = True

class CareerDataResponse(BaseModel):
    level: str
    program: str
    school: str
    campus: str

    class Config:
        from_attributes = True

class ScheduleEntryResponse(BaseModel):
    id: int
    date: date
    start_time: time
    end_time: time
    course_name: str
    instructor_name: str
    location: str

    class Config:
        from_attributes = True


class ScheduleResponse(BaseModel):
    date: date
    entries: List[ScheduleEntryResponse]

