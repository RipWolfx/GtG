"""
Script para inicializar la base de datos con datos de ejemplo
"""
import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from app.database import SessionLocal, engine
from app.models import Base, Student, PersonalData, CareerData, ScheduleEntry
import bcrypt
from datetime import date, time


def init_db():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        if db.query(Student).first():
            print("La base de datos ya contiene datos. Saltando inicialización.")
            return
        
        password = "password123"
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        student = Student(
            id="001234567",
            password_hash=password_hash,
            first_name="Juan Carlos",
            last_name="Flores García",
            dni="12345678"
        )
        db.add(student)
        db.flush()
        
        personal_data = PersonalData(
            student_id=student.id,
            email="1234567@senati.pe",
            phone="987 654 321",
            address="Avenida Horizonte Azul"
        )
        db.add(personal_data)
        
        career_data = CareerData(
            student_id=student.id,
            level="Profesional Técnico",
            program="Desarrollo de Software",
            school="Tecnologías de la información",
            campus="IND-ETI"
        )
        db.add(career_data)
        
        schedule_entries = [
            ScheduleEntry(
                student_id=student.id,
                date=date(2024, 1, 28),  
                start_time=time(7, 0),
                end_time=time(10, 0),
                course_name="SEMINARIO COMPLEMENT PRÁCT I",
                instructor_name="GARCIA FORTUNA, MOISES EDUARDO",
                location="IND - TORRE B 60TB - 200"
            ),
            ScheduleEntry(
                student_id=student.id,
                date=date(2024, 1, 28),
                start_time=time(10, 15),
                end_time=time(13, 15),
                course_name="SEMINARIO COMPLEMENT PRÁCT I",
                instructor_name="GARCIA FORTUNA, MOISES EDUARDO",
                location="IND - TORRE B 60TB - 200"
            ),
            ScheduleEntry(
                student_id=student.id,
                date=date(2024, 1, 28),
                start_time=time(14, 0),
                end_time=time(15, 30),
                course_name="DESARROLLO HUMANO",
                instructor_name="OLAZA GARIBAY, JENNY ROSARIO",
                location="IND - TORRE C 60TC - 504"
            ),
            ScheduleEntry(
                student_id=student.id,
                date=date(2024, 1, 28),
                start_time=time(15, 45),
                end_time=time(17, 15),
                course_name="DESARROLLO HUMANO",
                instructor_name="OLAZA GARIBAY, JENNY ROSARIO",
                location="IND - TORRE C 60TC - 504"
            ),
        ]
        
        for entry in schedule_entries:
            db.add(entry)
        
        db.commit()
        print("Base de datos inicializada correctamente con datos de ejemplo.")
        print(f"Estudiante creado: ID={student.id}, Contraseña=password123")
        
    except Exception as e:
        db.rollback()
        print(f"Error al inicializar la base de datos: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()

