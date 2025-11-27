import streamlit as st
import requests
import os

# --- Configuración del modelo ---
HF_TOKEN = os.environ.get("HF_TOKEN")   # Lo pones en Streamlit Secrets
HF_MODEL = "google/gemma-2-2b-it"       # Modelo gratuito compatible
API_URL = "https://router.huggingface.co/v1/chat/completions"

# --- Prompt del asistente ---
SYSTEM_PROMPT = """
Eres un asistente técnico especializado en instalaciones fotovoltaicas.
Respondes SIEMPRE como experto en placas solares.
Explicas paso a paso, das datos técnicos y priorizas la seguridad eléctrica.
Respondes siempre en español.
"""

# --- Función para llamar al modelo ---
def generar_respuesta(mensaje):
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    body = {
        "model": HF_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": mensaje}
        ],
        "temperature": 0.6
    }

    response = requests.post(API_URL, headers=headers, json=body)

    if response.status_code != 200:
        return f"❌ Error {response.status_code}: {response.text}"

    data = response.json()
    return data["choices"][0]["message"]["content"]

# --- Interfaz Streamlit ---
st.title("🔌 Asistente Técnico de Instalaciones Fotovoltaicas")
st.write("Haz tu pregunta sobre placas solares y te respondo como técnico experto.")

st.subheader("Ejemplos:")
st.write("- ¿Cómo dimensionar un inversor para 8 paneles de 420W?")
st.write("- Mi string marca 0V, ¿qué reviso primero?")
st.write("- ¿Qué producción anual puedo esperar en un tejado al sur en Sevilla?")

pregunta = st.text_area("Escribe tu pregunta aquí:")

if st.button("Enviar"):
    if pregunta.strip() == "":
        st.warning("Por favor escribe una pregunta.")
    else:
        respuesta = generar_respuesta(pregunta)
        st.write("### Respuesta del Asistente:")
        st.write(respuesta)
