import subprocess
from typing import Optional

class AgenteLLMExperto:
    """
    Agente que utiliza un modelo LLM experto (como deepseek-r1:7b) para responder preguntas técnicas.
    Ejecuta el modelo a través de la línea de comandos usando Ollama.
    """

    def __init__(self):
        """
        Inicializa el agente con el nombre del modelo a utilizar.
        """
        self.model = "deepseek-r1:7b"

    def responder(self, mensaje: str, registry: Optional[object] = None) -> str:
        """
        Ejecuta el modelo experto a través de Ollama para responder la pregunta dada.

        Args:
            mensaje (str): Pregunta técnica formulada por el usuario.
            registry (Optional[object]): Referencia al registro de agentes (no usado directamente aquí).

        Returns:
            str: Respuesta generada por el modelo, o mensaje de error si no se obtiene salida.
        """
        prompt = (
            "Eres un asistente experto en temas técnicos. Responde con claridad.\n"
            f"Pregunta: {mensaje}"
        )

        # Ejecutar modelo con ollama y obtener salida
        cmd = ["ollama", "run", self.model, prompt]
        res = subprocess.run(cmd, capture_output=True, text=True)

        return res.stdout.strip() or "❌ No se obtuvo respuesta del modelo experto."
