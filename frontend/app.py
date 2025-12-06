import streamlit as st
import requests
import pandas as pd
import os
from typing import List


# [Best Practice]: Configuration (API URL)
# Hardcodeamos la URL local por ahora; idealmente iría en un .env propio para el frontend
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/analysis/sentiment")

def run_analysis(feedback_list: List[str]):
    
    # Prepara el payload con la estructura Pydantic esperada (FeedbackInput)
    payload = {"feedbacks": feedback_list}

    # [ACCION DE DEBUGGING TEMPORAL]
    st.code(f"Payload enviado a FastAPI: {payload}") 
    # [FIN ACCION DE DEBUGGING]
    
    try:
        # Realiza la solicitud HTTP POST
        response = requests.post(API_URL, json=payload, timeout=10)

        # [Best Practice]: Status Code Check
        if response.status_code == 200:
            results = response.json()
            st.success("✅ Análisis Completo!")
            return results
        else:
            st.error(f"❌ Error de la API: Código {response.status_code}")
            st.error(response.json())
            return None
            
    except requests.exceptions.ConnectionError:
        st.error(f"⚠️ Error de Conexión: Asegúrate de que el backend (uvicorn) esté corriendo en {API_URL}.")
        return None
    except Exception as e:
        st.error(f"⚠️ Error inesperado: {e}")
        return None


# --- Estructura de la Interfaz Streamlit ---
st.set_page_config(layout="wide")

st.title("🧠 Analizador de Feedback MVP")
st.markdown("---")

# 1. Entrada de datos
st.header("📝 Ingreso de Feedback (Uno por línea)")
feedback_text = st.text_area(
    "Pega aquí los comentarios:", 
    height=200, 
    value="La aplicación es rápida y eficiente.\nEl precio es un poco alto para mis necesidades.\nMe encanta la nueva interfaz, el UX es genial!"
)

# 2. Botón de acción
if st.button("Analizar Sentimiento", type="primary"):
    
    # [CORRECCIÓN DE LÓGICA DE PREPROCESAMIENTO]
    
    # 3. Preprocesamiento: 
    # a) Divide por línea
    raw_feedbacks = feedback_text.split('\n')
    
    # b) Limpia cada string (quita espacios, saltos de línea ocultos) y filtra líneas vacías
    feedbacks_to_analyze = [
        f.strip() 
        for f in raw_feedbacks 
        if f.strip() # Filtra si el string resultante está vacío
    ]
    
    # -----------------------------------------------
    
    if not feedbacks_to_analyze:
        st.warning("Por favor, introduce al menos un comentario.")
    else:
        # [ACCION DE DEBUGGING TEMPORAL RECONFIRMADA]
        # Muestra el payload final que se enviará
        st.code(f"DEBUG: Payload final enviado: {feedbacks_to_analyze}", language='python')
        # [FIN ACCION DE DEBUGGING]
        
        # Llamar a la API
        metrics = run_analysis(feedbacks_to_analyze)
        
        if metrics:
            # 4. Mostrar Resultados (Visualización de datos)
            st.header("📊 Resultados del Análisis Cuantitativo")
            
            total = metrics.get('total_processed', 0)
            
            # Crear DataFrame simple para visualización
            data = {
                'Sentimiento': ['Positivo', 'Negativo', 'Neutral'],
                'Porcentaje (%)': [
                    metrics['positive_percentage'], 
                    metrics['negative_percentage'], 
                    metrics['neutral_percentage']
                ]
            }
            df_results = pd.DataFrame(data)

            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.metric(label="Total de Comentarios Procesados", value=total)
                st.dataframe(df_results, hide_index=True)
                
            with col2:
                # Mostrar un gráfico de barras
                st.subheader("Distribución de Sentimiento")
                st.bar_chart(df_results.set_index('Sentimiento'))