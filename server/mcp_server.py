from core.router_llm import LLMRouter
from core.context_loader import obtener_contexto_global  # NUEVO
import os

class MCPServer:
    """
    Servidor principal de MCP. Maneja el enrutamiento y registro de agentes.
    """

    def __init__(self, debug: bool = False, db_path: str = "database/context.db"):  # NUEVO
        self.debug = debug
        self.db_path = db_path if os.path.exists(db_path) else None  # verifica si existe
        self.router = LLMRouter()
    
    def procesar_mensaje(self, mensaje: str) -> str:
        """
        Procesa un mensaje de usuario seleccionando el agente adecuado.

        Args:
            mensaje (str): Pregunta del usuario.

        Returns:
            str: Respuesta generada por el agente y LLM.
        """
        try:
            llm, clase_agente = self.router.elegir_agente(mensaje)
            print("DEBUG: agente:", clase_agente, "llm:", type(llm))

            if clase_agente is None:
                # No se detectó ningún agente, usamos el modelo complejo
                contexto = obtener_contexto_global(self.db_path) if self.db_path else ""
                prompt = f"{contexto}Usuario: {mensaje}\nAsistente:"
                print("DEBUG: sin agente → usando llm_complejo")
                return self.router.llm_complex.responder(prompt)

            # Si se detectó un agente, usamos el modelo simple
            agente = clase_agente(llm=self.router.llm_simple)
            print(f"DEBUG: usando agente {clase_agente.__name__} con llm_simple")
            return agente.responder(mensaje)
        except Exception as e:
            print("ERROR:", e)
            print("DEBUG: agente:", repr(clase_agente), "llm:", type(llm))
            
            return "⚠️ Ocurrió un error procesando tu mensaje."