"""
Script de prueba para la API de SENATI
Ejecuta todos los endpoints disponibles para verificar que funcionan correctamente
"""
import requests
import json
from datetime import date

# Configuración
BASE_URL = "http://localhost:8000"
STUDENT_ID = "001234567"
PASSWORD = "password123"

def print_response(title, response):
    """Imprime la respuesta de forma legible"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")

def test_health_check():
    """Prueba el endpoint de health check"""
    print("\n🔍 Probando Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print_response("Health Check", response)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print(f"\n❌ ERROR: No se pudo conectar al servidor en {BASE_URL}")
        print("   Asegúrate de que el servidor esté corriendo:")
        print("   uvicorn app.main:app --reload")
        return False
    except requests.exceptions.Timeout:
        print(f"\n❌ ERROR: El servidor no respondió a tiempo")
        return False
    except Exception as e:
        print(f"\n❌ ERROR inesperado: {e}")
        return False

def test_login():
    """Prueba el endpoint de login"""
    print("\n🔐 Probando Login...")
    try:
        login_data = {
            "student_id": STUDENT_ID,
            "password": PASSWORD
        }
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=login_data,
            timeout=5
        )
        print_response("Login", response)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("access_token")
        return None
    except Exception as e:
        print(f"\n❌ ERROR en login: {e}")
        return None

def test_login_fail():
    """Prueba el login con credenciales incorrectas"""
    print("\n❌ Probando Login con credenciales incorrectas...")
    login_data = {
        "student_id": STUDENT_ID,
        "password": "wrong_password"
    }
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json=login_data
    )
    print_response("Login Fallido", response)
    return response.status_code == 401

def test_personal_data(token):
    """Prueba obtener datos personales"""
    print("\n👤 Probando Datos Personales...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{BASE_URL}/api/students/{STUDENT_ID}/personal-data",
            headers=headers,
            timeout=5
        )
        print_response("Datos Personales", response)
        return response.status_code == 200
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False

def test_career_data(token):
    """Prueba obtener datos de carrera"""
    print("\n🎓 Probando Datos de Carrera...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{BASE_URL}/api/students/{STUDENT_ID}/career-data",
            headers=headers,
            timeout=5
        )
        print_response("Datos de Carrera", response)
        return response.status_code == 200
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False

def test_schedule(token):
    """Prueba obtener horario"""
    print("\n📅 Probando Horario...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        # Usar la fecha del ejemplo (28 de enero de 2024)
        schedule_date = "2024-01-28"
        response = requests.get(
            f"{BASE_URL}/api/schedule/{STUDENT_ID}",
            headers=headers,
            params={"schedule_date": schedule_date},
            timeout=5
        )
        print_response(f"Horario para {schedule_date}", response)
        return response.status_code == 200
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False

def test_unauthorized_access():
    """Prueba acceder sin token"""
    print("\n🚫 Probando acceso sin autorización...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/students/{STUDENT_ID}/personal-data",
            timeout=5
        )
        print_response("Acceso No Autorizado", response)
        return response.status_code == 401
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False

def main():
    """Ejecuta todas las pruebas"""
    print("="*60)
    print("🧪 PRUEBAS DE LA API SENATI")
    print("="*60)
    print(f"\n📍 Conectando a: {BASE_URL}")
    print("⚠️  Asegúrate de que el servidor esté corriendo en otra terminal:")
    print("   uvicorn app.main:app --reload\n")
    
    # Verificar que el servidor esté corriendo
    if not test_health_check():
        print("\n" + "="*60)
        print("❌ El servidor no está respondiendo")
        print("="*60)
        print("\n📝 Pasos para solucionarlo:")
        print("1. Abre una nueva terminal")
        print("2. Navega a la carpeta del proyecto:")
        print("   cd", BASE_URL.replace("http://localhost:8000", ""))
        print("3. Inicia el servidor:")
        print("   uvicorn app.main:app --reload")
        print("4. Espera a ver: 'Uvicorn running on http://127.0.0.1:8000'")
        print("5. Vuelve a ejecutar este script: python test_api.py")
        return
    
    # Pruebas de autenticación
    token = test_login()
    test_login_fail()
    
    if not token:
        print("\n❌ No se pudo obtener el token. No se pueden probar los endpoints protegidos.")
        return
    
    # Pruebas de endpoints protegidos
    test_unauthorized_access()
    test_personal_data(token)
    test_career_data(token)
    test_schedule(token)
    
    print("\n" + "="*60)
    print("✅ Pruebas completadas")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: No se pudo conectar al servidor.")
        print("   Asegúrate de que el servidor esté corriendo:")
        print("   uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")

