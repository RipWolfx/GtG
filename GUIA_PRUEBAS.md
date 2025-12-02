# Guía de Pruebas - Backend SENATI

Esta guía te muestra todas las formas de probar tu backend y APIs.

## 🚀 Opción 1: Script Automático de Pruebas (Más Rápido)

### Paso 1: Asegúrate de que el servidor esté corriendo

En una terminal, ejecuta:
```bash
uvicorn app.main:app --reload
```

### Paso 2: Ejecuta el script de pruebas

En otra terminal, ejecuta:
```bash
python test_api.py
```

Este script probará automáticamente:
- ✅ Health check
- ✅ Login exitoso
- ✅ Login con credenciales incorrectas
- ✅ Acceso sin autorización
- ✅ Datos personales
- ✅ Datos de carrera
- ✅ Horario

---

## 🌐 Opción 2: Documentación Interactiva (Swagger UI) - RECOMENDADO

### Paso 1: Inicia el servidor
```bash
uvicorn app.main:app --reload
```

### Paso 2: Abre tu navegador en:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Paso 3: Prueba los endpoints

1. **Primero, haz login:**
   - Expande `POST /api/auth/login`
   - Haz clic en "Try it out"
   - Ingresa:
     ```json
     {
       "student_id": "001234567",
       "password": "password123"
     }
     ```
   - Haz clic en "Execute"
   - **Copia el `access_token` de la respuesta**

2. **Autoriza en Swagger:**
   - Haz clic en el botón **"Authorize"** (🔒) en la parte superior
   - Pega el token en el campo "Value"
   - Haz clic en "Authorize"
   - Cierra el diálogo

3. **Prueba los otros endpoints:**
   - `GET /api/students/{student_id}/personal-data`
   - `GET /api/students/{student_id}/career-data`
   - `GET /api/schedule/{student_id}` (con `schedule_date=2024-01-28`)

---

## 📡 Opción 3: Usar cURL (Terminal/Command Line)

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"student_id\":\"001234567\",\"password\":\"password123\"}"
```

**Guarda el `access_token` de la respuesta.**

### 3. Datos Personales
```bash
curl -X GET "http://localhost:8000/api/students/001234567/personal-data" \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

### 4. Datos de Carrera
```bash
curl -X GET "http://localhost:8000/api/students/001234567/career-data" \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

### 5. Horario
```bash
curl -X GET "http://localhost:8000/api/schedule/001234567?schedule_date=2024-01-28" \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

---

## 🛠️ Opción 4: Postman o Insomnia

### Configuración en Postman:

1. **Crear una colección** llamada "SENATI API"

2. **Variables de colección:**
   - `base_url` = `http://localhost:8000`
   - `token` = (se llenará automáticamente)

3. **Request 1: Login**
   - Method: `POST`
   - URL: `{{base_url}}/api/auth/login`
   - Body (raw JSON):
     ```json
     {
       "student_id": "001234567",
       "password": "password123"
     }
     ```
   - **Tests** (para guardar el token automáticamente):
     ```javascript
     if (pm.response.code === 200) {
         var jsonData = pm.response.json();
         pm.collectionVariables.set("token", jsonData.access_token);
     }
     ```

4. **Requests siguientes:**
   - Method: `GET`
   - URL: `{{base_url}}/api/students/001234567/personal-data`
   - Headers:
     - Key: `Authorization`
     - Value: `Bearer {{token}}`

---

## ✅ Credenciales de Prueba

- **ID de Estudiante**: `001234567`
- **Contraseña**: `password123`

---

## 📋 Checklist de Pruebas

### Pruebas Básicas:
- [ ] Health check responde correctamente
- [ ] Login con credenciales correctas funciona
- [ ] Login con credenciales incorrectas retorna 401
- [ ] Acceso sin token retorna 401

### Pruebas de Endpoints Protegidos:
- [ ] Obtener datos personales funciona
- [ ] Obtener datos de carrera funciona
- [ ] Obtener horario funciona
- [ ] Intentar acceder a datos de otro estudiante retorna 403

### Pruebas de Datos:
- [ ] Los datos personales coinciden con los datos de ejemplo
- [ ] Los datos de carrera coinciden con los datos de ejemplo
- [ ] El horario muestra las 4 clases del 28 de enero de 2024

---

## 🔍 Verificar que el Servidor Esté Corriendo

Si obtienes errores de conexión, verifica:

1. **El servidor está corriendo:**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **La base de datos está configurada:**
   - Verifica que el archivo `.env` existe
   - Verifica que PostgreSQL está corriendo
   - Verifica que la base de datos `senati_db` existe

3. **Los datos están inicializados:**
   ```bash
   python app/init_db.py
   ```

---

## 🐛 Solución de Problemas

### Error: "Connection refused"
- El servidor no está corriendo. Ejecuta `uvicorn app.main:app --reload`

### Error: "401 Unauthorized"
- El token no está en el header o está mal formateado
- Asegúrate de usar: `Authorization: Bearer <token>`
- Verifica que el token no haya expirado (válido por 30 días)

### Error: "404 Not Found"
- Verifica que la URL sea correcta
- Verifica que el `student_id` sea `001234567`

### Error: "500 Internal Server Error"
- Revisa los logs del servidor
- Verifica que la base de datos esté conectada
- Verifica que los datos estén inicializados

---

## 📊 Respuestas Esperadas

### Login Exitoso:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "student_id": "001234567",
  "student_name": "Juan Carlos Flores García"
}
```

### Datos Personales:
```json
{
  "first_name": "Juan Carlos",
  "last_name": "Flores García",
  "dni": "12345678",
  "student_id": "001234567",
  "email": "1234567@senati.pe",
  "phone": "987 654 321",
  "address": "Avenida Horizonte Azul"
}
```

### Datos de Carrera:
```json
{
  "level": "Profesional Técnico",
  "program": "Desarrollo de Software",
  "school": "Tecnologías de la información",
  "campus": "IND-ETI"
}
```

---

¡Listo para probar! 🚀

