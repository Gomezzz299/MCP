from core.router_llm import LLMRouter
from core.registry import AgentRegistry

class MCPServer:
    """
    Servidor MCP (Multi-Agent Control Point) que enruta preguntas de usuario
    a un modelo LLM o a agentes especializados registrados dinámicamente.
    """

    def __init__(self, debug: bool = False):
        """
        Inicializa el servidor MCP.

        Args:
            debug (bool): Si está en True, muestra información de depuración.
        """
        self.registry = AgentRegistry()
        self.router = LLMRouter(debug=debug)
        self.debug = debug

    def procesar(self, mensaje: str) -> str:
        """
        Procesa un mensaje del usuario utilizando el router LLM.
        Si la interpretación indica un agente, se invoca al agente correspondiente.
        En caso de error o interpretación inválida, se devuelve un mensaje de error.

        Args:
            mensaje (str): Pregunta o petición del usuario.

        Returns:
            str: Respuesta generada por el agente o mensaje de error si no se puede procesar.
        """
        interpretacion = self.router.interpretar(mensaje)

        if self.debug:
            print("[DEBUG] Interpretación:", interpretacion)

        if "agente" in interpretacion:
            agente_id = interpretacion["agente"]
            msg = interpretacion.get("mensaje", "")

            agente = self.registry.obtener(agente_id)
            if agente:
                try:
                    return agente.responder(msg, self.registry)
                except Exception as e:
                    return f"❌ Error al ejecutar el agente '{agente_id}': {e}"
            else:
                return f"❌ Agente '{agente_id}' no encontrado"

        return f"❌ No se pudo procesar la petición: {interpretacion}"
