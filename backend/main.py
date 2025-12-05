from fastapi import FastAPI
from backend.routers import analysis
from dotenv import load_dotenv

# [Best Practice]: Environment Loading at Startup
load_dotenv() 

# Inicialización de la aplicación FastAPI
app = FastAPI(
    title="Feedback Analyzer MVP API",
    description="API robusta para análisis de sentimiento impulsada por Google Cloud Translation y VADER.",
    version="1.0.0",
)

# Montar Routers
# [Best Practice]: Router Inclusion
app.include_router(analysis.router)

@app.get("/", tags=["Healthcheck"], status_code=200)
def healthcheck():
    """Endpoint simple para verificar que la API está viva."""
    return {"status": "ok", "service": "Feedback Analyzer API"}