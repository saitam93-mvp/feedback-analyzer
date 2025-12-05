from pydantic import BaseModel
from typing import List, Dict

# Esquema de ENTRADA (Lo que el cliente envía a la API)
class FeedbackInput(BaseModel):
    """Modelo para recibir una lista de strings (feedback de usuarios)."""
    feedbacks: List[str]

    # Ejemplo de datos para la documentación automática (Swagger UI)
    class Config:
        schema_extra = {
            "example": {
                "feedbacks": [
                    "El servicio fue rápido y la comida excelente. Lo recomiendo!",
                    "Muy caro para la calidad ofrecida, no volvería.",
                    "El mesero fue muy atento.",
                ]
            }
        }

# Esquema de SALIDA (Lo que la API devuelve al cliente)
class AnalysisResult(BaseModel):
    """Modelo para devolver los resultados porcentuales del análisis."""
    positive_percentage: float
    negative_percentage: float
    neutral_percentage: float
    total_processed: int
    
    class Config:
        schema_extra = {
            "example": {
                "positive_percentage": 66.67,
                "negative_percentage": 33.33,
                "neutral_percentage": 0.0,
                "total_processed": 3
            }
        }