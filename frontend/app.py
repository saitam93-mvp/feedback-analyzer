# frontend/app.py

import os # <--- Nuevo Import
import streamlit as st
import requests
import json
import pandas as pd

# [Best Practice]: Configuration via Environment Variables (Cloud Ready)
# Leer la variable de entorno API_URL. Usar http://localhost:8000 como fallback
# para el desarrollo local sin Docker.
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Feedback Analyzer MVP", layout="wide")

## Encabezado y Health Check
st.title(" Análisis de Sentimiento de Feedback 📊")
st.subheader("MVP usando FastAPI + Pandas")

# Verificar el estado de la API con el health check que ya implementamos
try:
    health_response = requests.get(f"{API_URL}/")
    if health_response.status_code == 200:
        st.success(f"Backend API está **ONLINE** en {API_URL}")
    else:
        st.error(f"Backend API está DOWN o no responde (Status: {health_response.status_code})")
except requests.exceptions.ConnectionError:
    st.error(f"⚠️ ERROR DE CONEXIÓN: Asegúrate de que Uvicorn esté corriendo en la terminal en {API_URL}")

st.markdown("---")

## Formulario de Entrada de Datos
st.header("Ingresar Feedback")
st.caption("Introduce una línea de feedback por campo.")

# Campo de texto multi-línea en Streamlit
feedback_input = st.text_area(
    "Ingresa múltiples líneas de feedback aquí:",
    height=150,
    placeholder="Ej: El producto es genial.\nEj: Tuve un error, el soporte es lento.\nEj: El precio es neutral."
)

if st.button("Analizar Feedback"):
    # 1. Preprocesamiento: Convertir el texto en una lista de strings
    # [Clean Code]: Filtering empty lines
    feedbacks_list = [line.strip() for line in feedback_input.split('\n') if line.strip()]

    if not feedbacks_list:
        st.warning("Por favor, ingresa al menos una línea de feedback para analizar.")
    else:
        st.info(f"Enviando {len(feedbacks_list)} líneas de feedback al backend...")
        
        # 2. Construir el payload JSON
        payload = {"feedbacks": feedbacks_list}
        
        # 3. Llamada HTTP POST al backend (Client-Server Interaction)
        try:
            response = requests.post(f"{API_URL}/analyze/sentiment", json=payload)
            response.raise_for_status() # Lanza una excepción para errores 4xx/5xx

            # 4. Procesar la Respuesta
            results = response.json()
            metrics = results['metrics']

            st.subheader("Resultados del Análisis:")
            
            # Mostrar métricas en columnas (Layout Streamlit)
            col1, col2, col3 = st.columns(3)
            col1.metric("Positivo", f"{metrics['positive_percentage']:.2f}%")
            col2.metric("Negativo", f"{metrics['negative_percentage']:.2f}%")
            col3.metric("Neutral", f"{metrics['neutral_percentage']:.2f}%")

            # Crear un DataFrame simple para mostrar los datos procesados
            st.markdown("---")
            
            # 5. Generar un gráfico de barras
            data_chart = pd.DataFrame(
                {
                    'Sentimiento': ['Positivo', 'Negativo', 'Neutral'],
                    'Porcentaje': [metrics['positive_percentage'], metrics['negative_percentage'], metrics['neutral_percentage']]
                }
            )
            st.bar_chart(data_chart.set_index('Sentimiento'))
            
        except requests.exceptions.RequestException as e:
            st.error(f"Error al comunicarse con la API: {e}")
            st.code(f"Asegúrate de que Uvicorn está corriendo y es accesible en {API_URL}")