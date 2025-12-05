# backend/routers/analysis.py

from typing import List
from pydantic import BaseModel
from fastapi import APIRouter

# Importar la lógica de negocio (Domain Layer)
from ..services.analyzer import analyze_feedback 

# 1. Crear la instancia del Router
# [Best Practice]: Namespacing / Routing Prefix
# El prefix='/analyze' garantiza que todas las rutas definidas aquí comiencen con /analyze.
router = APIRouter(
    prefix="/analyze",
    tags=["analysis"] # Agrega el nombre del grupo para Swagger UI
)

# 2. Definir el schema de datos de entrada
# [Best Practice]: Explicit Request Body Schema
class FeedbackRequest(BaseModel):
    feedbacks: List[str]

# 3. Implementación del Endpoint
# Ya no es @app.post, ahora es @router.post
@router.post("/sentiment", status_code=200)
async def perform_sentiment_analysis(request_data: FeedbackRequest):
    """
    Recibe una lista de feedback y retorna un análisis de sentimiento en porcentajes.
    """
    
    feedbacks = request_data.feedbacks
    
    # Delegación al Domain Layer
    analysis_metrics = analyze_feedback(feedbacks)
    
    return {
        "analysis_id": "temp-12345",
        "metrics": analysis_metrics
    }