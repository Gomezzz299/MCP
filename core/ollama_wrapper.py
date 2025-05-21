import subprocess
import json
from typing import Optional
from config import OLLAMA_CMD, DEFAULT_OLLAMA_MODEL

class OllamaLLM:
    """
    Wrapper para llamar a modelos Ollama vía CLI.

    Args:
        modelo (str): Nombre del modelo Ollama a usar.
    """

    def __init__(self, modelo: Optional[str] = None):
        self.modelo = modelo or DEFAULT_OLLAMA_MODEL

    def responder(self, prompt: str) -> str:
        """
        Envía el prompt al modelo Ollama y devuelve la respuesta en texto plano.

        Args:
            prompt (str): Texto que se envía al modelo.

        Returns:
            str: Respuesta del modelo, o mensaje de error.
        """
        cmd = [OLLAMA_CMD, "run", self.modelo]

        try:
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate(input=prompt, timeout=30)

            if process.returncode != 0:
                return f"❌ Error al llamar a Ollama: {stderr.strip()}"

            # Intentar parsear JSON (asumiendo que Ollama devuelve JSON con 'text' o similar)
            try:
                respuesta_json = json.loads(stdout)
                return respuesta_json.get("text", stdout.strip())
            except json.JSONDecodeError:
                return stdout.strip()

        except subprocess.TimeoutExpired:
            process.kill()
            return "❌ Timeout al llamar a Ollama."

        except Exception as e:
            return f"❌ Excepción al llamar a Ollama: {str(e)}"
