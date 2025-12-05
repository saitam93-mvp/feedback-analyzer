# backend/main.py (El archivo final)

from dotenv import load_dotenv
from fastapi import FastAPI
from .routers import analysis # Importamos el módulo router que acabamos de crear

# Cargar variables de entorno del archivo .env
load_dotenv()

# Inicializar la aplicación FastAPI
app = FastAPI(
    title="Feedback Analyzer API MVP",
    version="1.0.0",
    description="API para procesar y analizar feedback de usuarios.",
)

# 1. [Best Practice]: Incorporar Routers Modulares
# El método include_router monta todas las rutas definidas en analysis.py en la app.
app.include_router(analysis.router)

# 2. Endpoint de prueba (Health Check)
@app.get("/", status_code=200)
async def health_check():
    """Endpoint simple para verificar el estado de la API."""
    
    # Mantenemos el chequeo de la configuración
    import os
    api_port = os.getenv("API_PORT", "Puerto no encontrado") 
    
    return {
        "status": "online",
        "message": "Bienvenido al Analizador de Feedback.",
        "api_port_loaded": api_port
    }

# *** ¡Asegúrate de eliminar el código Pydantic y el endpoint viejo de aquí! ***