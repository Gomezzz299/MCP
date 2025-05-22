import re
from typing import Optional

from core.ollama_wrapper import OllamaLLM
from config import DEFAULT_OLLAMA_MODEL, DEEPSEEK_MODEL
from agents.clima import AgenteClima
from agents.fecha_hora import AgenteFecha
from agents.ubicacion import AgenteUbicacion
from core.context_loader import obtener_contexto_global

class LLMRouter:
    """
    Router que elige el modelo LLM más adecuado según el contenido del mensaje.
    """

    def __init__(self):
        self.llm_simple = OllamaLLM(DEFAULT_OLLAMA_MODEL)
        self.llm_complex = OllamaLLM(DEEPSEEK_MODEL)

    def elegir_llm(self, mensaje: str) -> OllamaLLM:
        """
        Decide qué modelo usar en función del tipo de mensaje.

        Args:
            mensaje (str): Mensaje del usuario.

        Returns:
            OllamaLLM: Modelo elegido.
        """
        texto = mensaje.lower()

        patrones_clima = [
            r"\bclima\b", r"\btiempo\b", r"\btemperatura\b",
            r"\bqué d[ií]a hace\b", r"\bc[oó]mo est[aá] el d[ií]a\b", r"\bc[oó]mo est[aá] el tiempo\b"
        ]
        if any(re.search(pat, texto) for pat in patrones_clima):
            return self.llm_simple, AgenteClima

        patrones_fecha = [
            r"\bfecha\b", r"\bd[ií]a es\b", r"\bqué d[ií]a es\b",
            r"\bhora\b", r"\bqué hora\b", r"\bhoy\b"
        ]
        if any(re.search(pat, texto) for pat in patrones_fecha):
            return self.llm_simple, AgenteFecha

        patrones_ubicacion = [r"\búbicaci[oó]n\b", r"\bd[oó]nde estoy\b", r"\blugar\b"]
        if any(re.search(pat, texto) for pat in patrones_ubicacion):
            return self.llm_simple, AgenteUbicacion

        return self.llm_complex, None  # O podrías definir un agente por defecto

    def enrutar_a_llm(mensaje: str, modelo, db_path: Optional[str] = None) -> str:
        contexto = obtener_contexto_global(db_path)
        prompt = f"{contexto}Usuario: {mensaje}\nAsistente:"
        respuesta = modelo.completar(prompt)
        return respuesta