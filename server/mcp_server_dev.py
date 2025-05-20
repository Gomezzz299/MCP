from core.router_llm import LLMRouter
from core.registry import AgentRegistry
import subprocess

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

    def procesar(self, pregunta: str):
        try:
            # Extrae posibles instrucciones del modelo pequeño
            prompt = f"Analiza la siguiente pregunta y genera una instrucción JSON indicando qué agentes deben intervenir y en qué orden.\nPregunta: {pregunta}"
            res = subprocess.run(
                ["ollama", "run", self.model_router, prompt],
                capture_output=True, text=True
            )
            texto = res.stdout.strip()
            ruta = extraer_json(texto)

            interpretacion = {
                "prompt_usado": prompt,
                "respuesta_llm_ruteador": texto,
                "json_extraido": ruta,
                "agentes_involucrados": [],
                "errores": [],
            }

            if not ruta or "agentes" not in ruta:
                interpretacion["errores"].append("No se pudo extraer una ruta válida.")
                return {
                    "respuesta": "❌ No pude entender cómo responder a tu pregunta.",
                    "interpretacion": interpretacion
                }

            resultado = None
            for paso in ruta["agentes"]:
                nombre = paso.get("nombre")
                mensaje = paso.get("mensaje", pregunta)
                agente = self.registry.obtener(nombre)
                if not agente:
                    interpretacion["errores"].append(f"Agente '{nombre}' no encontrado.")
                    continue
                interpretacion["agentes_involucrados"].append(nombre)
                resultado = agente.responder(mensaje, self.registry)

            return {
                "respuesta": resultado or "❌ No se pudo generar una respuesta.",
                "interpretacion": interpretacion
            }

        except Exception as e:
            return {
                "respuesta": "❌ Error interno al procesar la solicitud.",
                "interpretacion": {
                    "errores": [str(e)]
                }
            }

