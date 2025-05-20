import streamlit as st
import requests

st.set_page_config(page_title="MCP Chat", layout="centered")

st.title("🤖 Interfaz de MCP")

# Inicializa sesión
if "historial" not in st.session_state:
    st.session_state.historial = []
if "debug_info" not in st.session_state:
    st.session_state.debug_info = []
if "mostrar_debug" not in st.session_state:
    st.session_state.mostrar_debug = False

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
            interpretacion = data.get("interpretacion", None)
            if st.session_state.mostrar_debug:
                st.session_state.debug_info.append(interpretacion)
        except Exception as e:
            respuesta = f"❌ Error de conexión: {e}"
            if st.session_state.mostrar_debug:
                st.session_state.debug_info.append({"error": str(e)})

    st.session_state.historial.append({"mcp": respuesta})

# Entrada de texto
st.text_input("Pregunta:", key="pregunta_input", on_change=enviar_pregunta)

# Toggle para depuración
st.checkbox("🔍 Mostrar depuración", key="mostrar_debug")

st.markdown("---")
st.subheader("🗨️ Historial de conversación")

for i, msg in enumerate(st.session_state.historial):
    if "usuario" in msg:
        st.markdown(
            f"<div style='background-color:#e0f0ff;padding:10px;border-radius:10px;margin-bottom:5px;'>"
            f"<b>🧑 Tú:</b><br>{msg['usuario']}</div>",
            unsafe_allow_html=True,
        )
    elif "mcp" in msg:
        st.markdown(
            f"<div style='background-color:#e6ffe6;padding:10px;border-radius:10px;margin-bottom:10px;'>"
            f"<b>🤖 MCP:</b><br>{msg['mcp']}</div>",
            unsafe_allow_html=True,
        )
        # Mostrar depuración si está activo
        if st.session_state.mostrar_debug and i // 2 < len(st.session_state.debug_info):
            debug_data = st.session_state.debug_info[i // 2]
            with st.expander("🛠️ Depuración"):
                st.json(debug_data)

# Botón para limpiar
if st.button("🧹 Limpiar historial"):
    st.session_state.historial = []
    st.session_state.debug_info = []
