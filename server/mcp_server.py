from core.router_llm import LLMRouter
from core.registry import AgentRegistry
from agents.base import AgenteBase


class MCPServer:
    """
    Servidor principal de MCP. Maneja el enrutamiento y registro de agentes.
    """

    def __init__(self, debug: bool = False):
        self.debug = debug
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
            return llm.responder(mensaje)

        agente = clase_agente(llm=llm)
        return agente._responder(mensaje, self.registry)
