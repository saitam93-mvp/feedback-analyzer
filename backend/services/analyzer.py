import pandas as pd
from typing import List, Dict
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from google.cloud import translate_v2 as translate
from dotenv import load_dotenv
import os

def translate_text(text: str, target_language: str = 'en') -> str:
    """Traduce un texto usando la API oficial de Google Cloud Translation."""

    if not GCP_PROJECT_ID:
         print("❌ [ERROR] GCP_PROJECT_ID no configurado.")
         return text
    
    try:
        result = translate_client.translate(
            text,
            target_language=target_language
        )
        
        translated = result['translatedText']
        
        # [DEBUG 3] ¡Éxito! ¿Cuál fue el resultado?
        print(f"✅ [DEBUG] Traducción exitosa: '{translated}'")
        
        return translated

    except Exception as e:
        # [DEBUG 4] ¡Fallo! Aquí veremos por qué
        print(f"🔥 [ERROR CRÍTICO] Falló la traducción. Razón: {e}")
        return text # Retorna el original si falla (Causa del 100% Neutral)

# ----------------------------------------------------
# 1. Configuración
# [Best Practice]: Configuration Loading (dotenv)
load_dotenv()
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
# La variable GOOGLE_APPLICATION_CREDENTIALS se carga automáticamente desde el .env

# ----------------------------------------------------
# 2. Inicialización de Recursos
# [Best Practice]: Resource Initialization
# Inicializar NLTK/VADER
try:
    sia = SentimentIntensityAnalyzer()
except LookupError:
    nltk.download('vader_lexicon')
    sia = SentimentIntensityAnalyzer()

# Inicializar el servicio de traducción oficial (se autentica automáticamente)
translate_client = translate.Client()


def get_vader_sentiment(text: str) -> str:
    """Clasifica el sentimiento basado en la puntuación compuesta de VADER."""
    score = sia.polarity_scores(text)['compound']

    if score >= 0.05:
        return 'Positive'
    elif score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'


def translate_text(text: str, target_language: str = 'en') -> str:
    """Traduce un texto usando la API oficial de Google Cloud Translation."""
    # [Best Practice]: Error Handling and Logging
    if not GCP_PROJECT_ID:
         print("ERROR: GCP_PROJECT_ID no está configurado en el .env.")
         return text
    
    try:
        result = translate_client.translate(
            text,
            target_language=target_language
        )
        return result['translatedText']
    except Exception as e:
        print(f"ERROR: Fallo de traducción para '{text[:30]}...'. Error: {e}")
        return text


def analyze_feedback(feedbacks: List[str]) -> Dict[str, float]:
    """
    Traduce el feedback a inglés y luego calcula métricas de sentimiento.
    """
    df = pd.DataFrame(feedbacks, columns=['original_text'])
    df['translated_text'] = df['original_text'].apply(translate_text)
    df['sentiment'] = df['translated_text'].apply(get_vader_sentiment)
    
    sentiment_counts = df['sentiment'].value_counts(normalize=True) * 100

    results = {
        'positive_percentage': sentiment_counts.get('Positive', 0.0),
        'negative_percentage': sentiment_counts.get('Negative', 0.0),
        'neutral_percentage': sentiment_counts.get('Neutral', 0.0),
        'total_processed': len(feedbacks)
    }

    return results


if __name__ == "__main__":
    sample_data = [
        "Todo es maravilloso, un gran producto.",
        "El servicio al cliente es terrible y lento.",
        "Es un producto funcional, no es ni bueno ni malo.",
    ]
    
    print("--- Probando la conexión con la API Oficial ---")
    metrics = analyze_feedback(sample_data)
    print("--- Resultados del Análisis ---")
    print(metrics)