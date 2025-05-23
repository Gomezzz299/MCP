import json

class AgenteBase:
    patrones = []

    def __init__(self, llm):
        self.llm = llm

    def responder(self, mensaje: str) -> str:
        """
        Llama al método _responder_raw del agente, maneja errores y genera
        una respuesta natural usando el LLM con los datos estructurados.
        """
        try:
            datos = self.agente()
            if not isinstance(datos, dict):
                return "❌ El agente no devolvió datos en formato JSON/dict."

            datos_json = json.dumps(datos, indent=2, ensure_ascii=False)
            prompt = (
                "Eres un asistente experto. El siguiente agente ha proporcionado esta información estructurada:\n"
                f"{datos_json}\n\n"
                "Usa solo esta información para redactar una respuesta clara y natural a la siguiente pregunta del usuario:\n"
                f"{mensaje}"
            )
            return self.llm.responder(prompt)

        except Exception as e:
            return f"❌ Error en el agente: {e}"

    def agente(self) -> dict:
        raise NotImplementedError("El agente debe implementar el método _responder_raw().")
