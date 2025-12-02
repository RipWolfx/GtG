# SENATI Backend API

Backend desarrollado con Python, FastAPI y PostgreSQL para la aplicación móvil SENATI.

## Características

- Autenticación con JWT (ID de estudiante y contraseña)
- Endpoints para datos personales del estudiante
- Endpoints para datos de carrera
- Endpoints para horarios de clases
- Base de datos PostgreSQL con SQLAlchemy ORM
- Validación de datos con Pydantic
- CORS configurado para React Native

## Requisitos

- Python 3.8+
- PostgreSQL 12+
- pip

## Instalación

1. Clonar el repositorio:
```bash
git clone <repository-url>
cd senati_backend
```

2. Crear un entorno virtual:
```bash
python -m venv venv
```

3. Activar el entorno virtual:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Instalar dependencias:
```bash
pip install -r requirements.txt
```

5. Configurar variables de entorno:
```bash
cp env.example .env
```

Editar el archivo `.env` con tus credenciales de PostgreSQL:
```
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/senati_db
SECRET_KEY=tu-clave-secreta-aqui
```

6. Crear la base de datos en PostgreSQL:
```sql
CREATE DATABASE senati_db;
```

7. Inicializar la base de datos con datos de ejemplo:
```bash
python app/init_db.py
```

## Ejecutar la aplicación

```bash
uvicorn app.main:app --reload
```

La API estará disponible en `http://localhost:8000`

## Documentación de la API

Una vez que la aplicación esté corriendo, puedes acceder a:
- Documentación interactiva (Swagger): `http://localhost:8000/docs`
- Documentación alternativa (ReDoc): `http://localhost:8000/redoc`

## Endpoints

### Autenticación

- `POST /api/auth/login` - Login con ID de estudiante y contraseña

### Estudiantes

- `GET /api/students/{student_id}/personal-data` - Obtener datos personales
- `GET /api/students/{student_id}/career-data` - Obtener datos de carrera

### Horario

- `GET /api/schedule/{student_id}?schedule_date=YYYY-MM-DD` - Obtener horario para una fecha específica

## Datos de ejemplo

Después de ejecutar `init_db.py`, se crea un estudiante de ejemplo:
- **ID de estudiante**: `001234567`
- **Contraseña**: `password123`

## Estructura del proyecto

```
senati_backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicación principal FastAPI
│   ├── database.py          # Configuración de base de datos
│   ├── models.py            # Modelos SQLAlchemy
│   ├── schemas.py           # Esquemas Pydantic
│   ├── init_db.py           # Script de inicialización
│   └── routers/
│       ├── __init__.py
│       ├── auth.py          # Endpoints de autenticación
│       ├── students.py      # Endpoints de estudiantes
│       └── schedule.py      # Endpoints de horario
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Notas de seguridad

- Cambiar `SECRET_KEY` en producción
- Cambiar la contraseña por defecto del estudiante de ejemplo
- Configurar CORS con dominios específicos en producción
- Usar HTTPS en producción
- Implementar rate limiting para prevenir ataques de fuerza bruta

## Desarrollo

Para desarrollo, se recomienda usar:
- `uvicorn app.main:app --reload` para recarga automática
- Herramientas como Postman o Insomnia para probar los endpoints

