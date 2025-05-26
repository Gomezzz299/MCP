import json

class AgenteBase:
    """
    Clase base para todos los agentes del sistema MCP. 
    Define la lógica común que utilizan los agentes, como el formateo de respuestas 
    y la generación de lenguaje natural usando un modelo LLM.

    Atributos:
        patrones (list): Lista de expresiones regulares que identifican si un mensaje debe ser manejado por este agente.
        llm (object): Modelo de lenguaje que se utiliza para generar respuestas naturales a partir de datos estructurados.
    """
    
    patrones = []  # Cada subclase puede definir sus propios patrones para detectar mensajes relevantes.

    def __init__(self, llm: object):
        """
        Inicializa el agente con un modelo de lenguaje.

        Args:
            llm (object): Instancia del modelo de lenguaje usado para generar respuestas naturales.
        """
        self.llm = llm

    def responder(self, mensaje: str) -> str:
        """
        Procesa un mensaje del usuario, ejecuta la lógica del agente y genera una respuesta natural.

        Llama internamente al método `agente()` que debe ser implementado por las subclases,
        obtiene los datos estructurados devueltos por el agente y los transforma en una
        respuesta legible mediante el modelo LLM.

        Args:
            mensaje (str): Pregunta del usuario.

        Returns:
            str: Respuesta generada por el modelo LLM o mensaje de error.
        """
        try:
            datos = self.agente()

            if not isinstance(datos, dict):
                return "❌ El agente no devolvió datos en formato JSON/dict."

            # Convertimos los datos estructurados a JSON para usarlos como contexto en el prompt
            datos_json = json.dumps(datos, indent=2, ensure_ascii=False)

            # Prompt que se enviará al modelo LLM para generar una respuesta natural
            prompt = (
                "Eres un asistente experto. El siguiente agente ha proporcionado esta información estructurada:\n"
                f"{datos_json}\n\n"
                "Usa solo esta información para redactar una respuesta clara y natural a la siguiente pregunta del usuario:\n"
                f"{mensaje}"
            )

            # Generamos y devolvemos la respuesta final
            return self.llm.responder(prompt)

        except Exception as e:
            # En caso de excepción, devolvemos un mensaje de error
            return f"❌ Error en el agente: {e}"

    def agente(self) -> dict:
        """
        Método base que debe ser implementado por todas las subclases de agentes.

        Este método se encarga de obtener los datos estructurados que describen la respuesta del agente.

        Returns:
            dict: Diccionario con los datos generados por el agente.

        Raises:
            NotImplementedError: Si no se implementa en la subclase.
        """
        raise NotImplementedError("El agente debe implementar el método _responder_raw().")
