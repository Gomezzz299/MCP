import json
from functools import wraps
from typing import Callable, Any

def responder_con_llm(func: Callable) -> Callable:
    """
    Decorador para convertir la salida estructurada de un agente (dict) en una respuesta natural usando el LLM simple.

    Requiere que la función decorada reciba como primer argumento `mensaje` (str)
    y como segundo argumento `registry`, que contiene el LLM simple como `registry.llm_simple`.

    Returns:
        str: Respuesta generada en lenguaje natural.
    """
    @wraps(func)
    def wrapper(self, mensaje: str, *args: Any, **kwargs: Any) -> str:
        datos = func(self, mensaje, *args, **kwargs)
        if not isinstance(datos, dict):
            return "❌ El agente no devolvió datos en formato JSON/dict."
        if not hasattr(self, "llm") or self.llm is None:
            return "❌ El agente no tiene un modelo LLM asignado."

        try:
            datos_json = json.dumps(datos, indent=2, ensure_ascii=False)
        except Exception as e:
            return f"❌ Error al serializar datos JSON: {e}"

        prompt = (
            "Eres un asistente experto. El siguiente agente ha proporcionado esta información estructurada:\n"
            f"{datos_json}\n\n"
            "Usa solo esta información para redactar una respuesta clara y natural a la siguiente pregunta del usuario:\n"
            f"{mensaje}"
        )

        return self.llm.responder(prompt)
    return wrapper
