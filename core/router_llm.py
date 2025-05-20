import subprocess
from utils.json_parser import extraer_json

class LLMRouter:
    """
    Clase encargada de enrutar las preguntas del usuario a un modelo LLM
    para que decida cuál agente debe procesar la solicitud.
    """

    def __init__(self, model: str = "mistral", debug: bool = False):
        """
        Inicializa el enrutador con el modelo LLM y configuración de depuración.

        Args:
            model (str): Nombre del modelo en Ollama a utilizar. Por defecto "mistral".
            debug (bool): Si está en True, muestra información de depuración.
        """
        self.model = model
        self.debug = debug

    def ask(self, prompt: str) -> str:
        """
        Envía un prompt al modelo LLM usando Ollama y devuelve la respuesta.

        Args:
            prompt (str): El mensaje a enviar al modelo.

        Returns:
            str: Respuesta en texto plano del modelo LLM.
        """
        comando = ["ollama", "run", self.model, prompt]
        resultado = subprocess.run(comando, capture_output=True, text=True)
        return resultado.stdout.strip()

    def interpretar(self, pregunta: str) -> dict:
        """
        Interpreta una pregunta del usuario enviándola al LLM para decidir
        el agente adecuado o generar una respuesta directa.

        Args:
            pregunta (str): Pregunta o petición del usuario.

        Returns:
            dict: Diccionario con la interpretación del modelo LLM.
                  Puede incluir las claves:
                    - {"agente": ..., "mensaje": ...}
                  o en caso de error:
                    - {"respuesta": ...}
        """
        system_prompt = (
            "Eres un sistema de enrutamiento. Devuelve SOLO un JSON válido con alguno de estos agentes:\n"
            "- Si puedes responder tú: {\"agente\": \"LLM_EXPERTO\", \"mensaje\": \"respuesta a la pregunta\"}\n"
            "- Si necesitas saber el clima: {\"agente\": \"CLIMA\", \"mensaje\": \"obtener_clima\"}\n"
            "- Si necesitas saber la fecha: {\"agente\": \"FECHA\", \"mensaje\": \"obtener_fecha\"}\n"
            "- Si necesitas saber la ubicación: {\"agente\": \"UBICACION\", \"mensaje\": \"obtener_ubicacion\"}\n"
            "NO inventes agentes, NO des texto libre, SOLO devuelve un JSON válido como los anteriores.\n"
            f"Usuario: {pregunta}\nRespuesta:"
        )

        if self.debug:
            print("[DEBUG] 💬 Prompt enviado al LLM:\n", system_prompt)

        raw_response = self.ask(system_prompt)

        if self.debug:
            print("[DEBUG] 🧪 RAW del LLM:\n", raw_response)

        try:
            json_data = extraer_json(raw_response)
            if not json_data:
                raise ValueError("No se encontró JSON válido en la respuesta.")
            return json_data
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] ❌ No se pudo interpretar JSON, fallback con texto plano: {e}")
            return {"respuesta": raw_response.strip()}
