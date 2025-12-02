from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.database import get_db
from app.models import Student
from app.schemas import LoginRequest, LoginResponse
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60  

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_student(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        student_id: str = payload.get("sub")
        if student_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise credentials_exception
    return student


@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Endpoint de login con ID de estudiante y contraseña"""
    student = db.query(Student).filter(Student.id == login_data.student_id).first()
    
    if not student or not student.verify_password(login_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ID de estudiante o contraseña incorrectos",
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": student.id}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "student_id": student.id,
        "student_name": f"{student.first_name} {student.last_name}"
    }

