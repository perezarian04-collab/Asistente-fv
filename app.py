import streamlit as st
import requests
import os

# --- CONFIGURACIÓN DEL MODELO ---
HF_MODEL = "google/flan-t5-large"
HF_API_URL = "https://api-inference.huggingface.co/models/google/gemma-7b-it"
HF_TOKEN = os.environ.get("HF_TOKEN")  #

# --- PROMPT FIJO (ROL DEL ASISTENTE) ---
SYSTEM_PROMPT = """
Eres un asistente técnico especializado en instalaciones fotovoltaicas.
Debes responder SIEMPRE como experto en placas solares.
Explicas paso a paso, pides datos técnicos si faltan, y priorizas la seguridad eléctrica.
Respondes siempre en español.
"""

# --- FUNCIÓN PARA HABLAR CON LA IA ---
def generar_respuesta(mensaje_usuario):
    if not HF_TOKEN:
        return "? ERROR: Falta el token HF_TOKEN. Debes configurarlo en Streamlit ? Settings ? Secrets."

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": SYSTEM_PROMPT + "\nUsuario: " + mensaje_usuario + "\nAsistente:",
        "parameters": {"max_new_tokens": 300, "temperature": 0.2}
    }

    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]
        return str(data)

    except Exception as e:
        return f"? Error conectando con la IA: {e}"

# --- INTERFAZ STREAMLIT ---
st.title("? Asistente Técnico de Instalaciones Fotovoltaicas")
st.write("Haz tu pregunta sobre placas solares y te responderé como técnico experto.")

st.subheader("Ejemplos:")
st.write("- ¿Cómo dimensionar un inversor para 8 paneles de 420W?")
st.write("- Mi string marca 0V, ¿qué reviso primero?")
st.write("- ¿Qué producción anual puedo esperar en un tejado al sur en Sevilla?")

pregunta = st.text_area("Escribe tu pregunta aquí:")

if st.button("Enviar"):
    if pregunta.strip() == "":
        st.warning("Por favor, escribe una pregunta.")
    else:
        with st.spinner("Generando respuesta..."):
            respuesta = generar_respuesta(pregunta)
        st.write("### Respuesta del asistente:")
        st.write(respuesta)



