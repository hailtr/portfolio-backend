import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

def find_and_load_env():
    
    current_path = Path(__file__).resolve().parent
    print(f" Iniciando búsqueda desde: {current_path}")

    
    while current_path != current_path.parent:
        potential_env = current_path / '.env'
    
        
        if potential_env.exists():
            print(f" ¡ENCONTRADO! Cargando variables desde: {potential_env}")
            load_dotenv(dotenv_path=potential_env)
            return True
        
        current_path = current_path.parent

    print(" No se encontró ningún archivo '.env' en ninguna carpeta superior.")
    return False

# --- EJECUCIÓN ---

# 1. Cargar entorno
if not find_and_load_env():
    print(" Asegúrate de que el archivo se llame exactamente '.env' y no '.env.txt'")
    sys.exit(1)

# 2. Verificar Key
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print(" El archivo .env existe, pero NO tiene la variable GEMINI_API_KEY dentro.")
    sys.exit(1)

# 3. Probar Conexión (Modo REST para Venezuela)
try:
    genai.configure(api_key=api_key, transport='rest') # IMPORTANTE: 'rest'
    print("\n Probando conexión con Google (esto puede tardar unos segundos)...")
    
    models = list(genai.list_models())
    
    print("\n ¡CONEXIÓN EXITOSA! Modelos disponibles:")
    for m in models:
        if 'generateContent' in m.supported_generation_methods:
            print(f"   * {m.name}")

except Exception as e:
    print(f"\n Error de Conexión: {e}")
    print("Diagnóstico: Si esto falla, es bloqueo de ISP. Necesitas VPN.")