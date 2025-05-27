from core.router_llm import LLMRouter
from core.context_loader import obtener_contexto_global
import os

class MCPServer:
    """
    Servidor principal de MCP (Multi-Agent Chat Platform).

    Esta clase actúa como el núcleo del sistema, coordinando la recepción de mensajes
    del usuario, el enrutamiento al agente apropiado y la generación de respuestas,
    ya sea por un agente específico o directamente a través del modelo LLM.

    Atributos:
        debug (bool): Si es True, muestra información adicional útil para depuración.
        db_path (str): Ruta a la base de datos usada para cargar el contexto global.
        router (LLMRouter): Instancia del enrutador que decide qué LLM y agente usar.
    """

    def __init__(self, debug: bool = False, db_path: str = "database/context.db"):
        """
        Inicializa el servidor MCP, con opción de depuración y base de datos de contexto.

        Args:
            debug (bool): Habilita o deshabilita mensajes de depuración.
            db_path (str): Ruta al archivo de base de datos SQLite para contexto global.
        """
        self.debug = debug
        self.db_path = db_path if os.path.exists(db_path) else None  # Solo se usa si existe el archivo
        self.router = LLMRouter()  # Enrutador para decidir el agente/LLM apropiado
    
    def procesar_mensaje(self, mensaje: str) -> str:
        """
        Procesa un mensaje del usuario utilizando agentes y modelos LLM.

        Determina si hay un agente relevante para responder la consulta.
        Si no lo hay, el sistema utiliza el modelo LLM complejo directamente
        y añade contexto global desde una base de datos (si está disponible).

        Args:
            mensaje (str): Pregunta del usuario.

        Returns:
            str: Respuesta generada por un agente o directamente por un LLM.
        """
        try:
            # Usa el enrutador para seleccionar un LLM y un agente que coincida con el mensaje
            llm, clase_agente = self.router.elegir_agente(mensaje)
            if self.debug:
                print("DEBUG: agente:", clase_agente, "llm:", type(llm))

            if clase_agente is None:
                # No se detectó ningún agente → usar LLM complejo directamente
                contexto = obtener_contexto_global(self.db_path) if self.db_path else ""
                prompt = f"{contexto}Usuario: {mensaje}\nAsistente:"
                if self.debug:
                    print("DEBUG: sin agente → usando llm_complejo")
                return self.router.llm_complex.responder(prompt)

            # Si hay un agente coincidente → usar LLM simple y delegar respuesta al agente
            agente = clase_agente(llm=self.router.llm_simple)
            if self.debug:
                print(f"DEBUG: usando agente {clase_agente.__name__} con llm_simple")
            return agente.responder(mensaje)

        except Exception as e:
            # Captura cualquier error que ocurra en el proceso
            print("ERROR:", e)
            if self.debug:
                print("DEBUG: agente:", repr(clase_agente), "llm:", type(llm))
            return "⚠️ Ocurrió un error procesando tu mensaje."
