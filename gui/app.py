import streamlit as st
import requests

st.set_page_config(page_title="MCP Chat", layout="centered")
st.title("🤖 Interfaz de MCP")

# Inicializa estado
if "historial" not in st.session_state:
    st.session_state.historial = []
if "debug_info" not in st.session_state:
    st.session_state.debug_info = []
if "mostrar_debug" not in st.session_state:
    st.session_state.mostrar_debug = False
if "limpiar" not in st.session_state:
    st.session_state.limpiar = False

server_url = st.secrets.get("server_url", "http://localhost:8000/process")

def enviar_pregunta():
    pregunta = st.session_state.pregunta_input.strip()
    if not pregunta:
        st.warning("Escribe una pregunta.")
        return
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

# Entrada de texto
st.text_input("Pregunta:", key="pregunta_input", on_change=enviar_pregunta)

# Toggle de depuración
mostrar_debug = st.checkbox("🔍 Mostrar depuración", value=st.session_state.mostrar_debug)
st.session_state.mostrar_debug = mostrar_debug

# Botón de limpieza, solo si hay historial
if st.session_state.historial or st.session_state.debug_info:
    if st.button("🧹 Limpiar historial"):
        st.session_state.historial = []
        st.session_state.debug_info = []
        st.session_state.limpiar = True

# Mostrar historial solo si no acabamos de limpiar
if not st.session_state.limpiar:
    st.markdown("---")
    st.subheader("🗨️ Historial de conversación")
    for i, msg in enumerate(st.session_state.historial):
        if "usuario" in msg:
            st.markdown(f"<p style='color:blue;'>🧑 Tú: {msg['usuario']}</p>", unsafe_allow_html=True)
        elif "mcp" in msg:
            st.markdown(f"<p style='color:green;'>🤖 MCP: {msg['mcp']}</p>", unsafe_allow_html=True)
        if mostrar_debug and i // 2 < len(st.session_state.debug_info):
            debug_data = st.session_state.debug_info[i // 2]
            with st.expander("🛠️ Depuración"):
                st.json(debug_data)

# Resetear bandera al final
st.session_state.limpiar = False
