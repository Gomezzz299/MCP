import streamlit as st
import requests

st.set_page_config(page_title="MCP Chat", layout="centered")

st.title("🤖 Interfaz de MCP")

# Inicializa sesión
if "historial" not in st.session_state:
    st.session_state.historial = []

server_url = st.secrets.get("server_url", "http://localhost:8000/process")

def enviar_pregunta():
    pregunta = st.session_state.pregunta_input.strip()
    if not pregunta:
        st.warning("Escribe una pregunta.")
        return
    # Vaciar la caja de texto para evitar dobles envíos
    st.session_state.pregunta_input = ""

    st.session_state.historial.append({"usuario": pregunta})

    with st.spinner("Esperando respuesta..."):
        try:
            response = requests.post(server_url, json={"pregunta": pregunta})
            response.raise_for_status()
            data = response.json()
            respuesta = data.get("respuesta", "❌ Respuesta vacía del servidor.")
        except Exception as e:
            respuesta = f"❌ Error de conexión: {e}"

    st.session_state.historial.append({"mcp": respuesta})

st.text_input("Pregunta:", key="pregunta_input", on_change=enviar_pregunta)

st.markdown("---")
st.write("### Historial de conversación:")

for msg in st.session_state.historial:
    if "usuario" in msg:
        st.markdown(f"<p style='color:blue;'>🧑 Tú: {msg['usuario']}</p>", unsafe_allow_html=True)
    elif "mcp" in msg:
        st.markdown(f"<p style='color:green;'>🤖 MCP: {msg['mcp']}</p>", unsafe_allow_html=True)

if st.button("Limpiar historial"):
    st.session_state.historial = []
