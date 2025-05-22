from core.router_llm import LLMRouter
from core.registry import AgentRegistry
from core.context_loader import obtener_contexto_global  # NUEVO
from agents.base import AgenteBase
import os

class MCPServer:
    """
    Servidor principal de MCP. Maneja el enrutamiento y registro de agentes.
    """

    def __init__(self, debug: bool = False, db_path: str = "database/context.db"):  # NUEVO
        self.debug = debug
        self.db_path = db_path if os.path.exists(db_path) else None  # verifica si existe
        self.router = LLMRouter()
        self.registry = AgentRegistry(llm_router=self.router)
    
    def procesar_mensaje(self, mensaje: str) -> str:
        """
        Procesa un mensaje de usuario seleccionando el agente adecuado.

        Args:
            mensaje (str): Pregunta del usuario.

        Returns:
            str: Respuesta generada por el agente y LLM.
        """
        llm, clase_agente = self.router.elegir_llm(mensaje)
        print("DEBUG: agente:", clase_agente, "llm:", type(llm))

        if clase_agente is None:
            contexto = obtener_contexto_global(self.db_path) if self.db_path else ""
            prompt = f"{contexto}Usuario: {mensaje}\nAsistente:"
            return llm.responder(prompt)

        agente = clase_agente(llm=llm)
        return agente._responder(mensaje, self.registry)
