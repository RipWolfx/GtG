from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, students, schedule
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SENATI Backend API",
    description="API backend para la aplicación móvil SENATI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(students.router, prefix="/api/students", tags=["Students"])
app.include_router(schedule.router, prefix="/api/schedule", tags=["Schedule"])

@app.get("/")
async def root():
    return {"message": "SENATI Backend API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

