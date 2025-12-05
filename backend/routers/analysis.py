from fastapi import APIRouter
from backend.schemas import FeedbackInput, AnalysisResult
from backend.services.analyzer import analyze_feedback
from typing import Dict

# [Best Practice]: Router Definition
# Usamos un APIRouter para agrupar endpoints relacionados (ej: /analysis)
router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
)

# [Best Practice]: Async Endpoints (FastAPI standard)
@router.post(
    "/sentiment", 
    response_model=AnalysisResult, 
    status_code=200,
    summary="Calcula el porcentaje de sentimientos (positivo, negativo, neutral) en un conjunto de feedback."
)
async def perform_sentiment_analysis(
    data: FeedbackInput
) -> Dict[str, float]:
    """
    Recibe una lista de comentarios de feedback, los traduce, aplica VADER 
    y devuelve las métricas porcentuales.
    """
    # 1. Extracción de datos tipados (Pydantic validation ya ocurrió)
    feedbacks: List[str] = data.feedbacks
    
    # 2. Llamada a la Lógica de Negocio (Separation of Concerns)
    # Hacemos la llamada a la función que ya probamos en analyzer.py
    results: Dict[str, float] = analyze_feedback(feedbacks)
    
    # 3. Devolvemos el resultado (Pydantic lo valida y serializa automáticamente)
    return results