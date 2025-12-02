from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
import bcrypt


class Student(Base):
    __tablename__ = "students"

    id = Column(String, primary_key=True, index=True)  
    password_hash = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    dni = Column(String, unique=True, nullable=False)
    

    personal_data = relationship("PersonalData", back_populates="student", uselist=False)
    career_data = relationship("CareerData", back_populates="student", uselist=False)
    schedule_entries = relationship("ScheduleEntry", back_populates="student")

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))


class PersonalData(Base):
    __tablename__ = "personal_data"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, ForeignKey("students.id"), unique=True, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    
    student = relationship("Student", back_populates="personal_data")


class CareerData(Base):
    __tablename__ = "career_data"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, ForeignKey("students.id"), unique=True, nullable=False)
    level = Column(String, nullable=False) 
    program = Column(String, nullable=False) 
    school = Column(String, nullable=False) 
    campus = Column(String, nullable=False) 
    
  
    student = relationship("Student", back_populates="career_data")


class ScheduleEntry(Base):
    __tablename__ = "schedule_entries"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, ForeignKey("students.id"), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    course_name = Column(String, nullable=False)
    instructor_name = Column(String, nullable=False)
    location = Column(String, nullable=False) 
    
    student = relationship("Student", back_populates="schedule_entries")

