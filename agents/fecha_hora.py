from datetime import datetime
from decoradores.utils import responder_con_llm

class AgenteFecha:
    """
    Agente que responde con la fecha o la hora actual según el mensaje.
    """
    
    patrones = [
        r"\bfecha\b", r"\bd[ií]a es\b", r"\bqué d[ií]a es\b",
        r"\bhora\b", r"\bqué hora\b"
    ]

    def __init__(self, llm: object):
        self.llm = llm

    @responder_con_llm
    def _responder(self, mensaje: str) -> dict:
        """
        Responde con la fecha u hora actual si se detecta en el mensaje.

        Args:
            mensaje (str): Pregunta del usuario
            registry (dict, optional): Registro de agentes

        Returns:
            dict: Datos estructurados con la fecha u hora
        """
        try:
            now = datetime.now()
            return {
                "success": True,
                "data": {
                    "fecha_completa": now.strftime("%A %d de %B de %Y"),
                    "iso": now.strftime("%Y-%m-%d"),
                    "dia": now.strftime("%A"),
                    "dia_numero": now.strftime("%d"),
                    "mes": now.strftime("%B"),
                    "anio": now.strftime("%Y")
                }
            }
        except Exception as e:
            return {"success": False, "error": f"Error al obtener la fecha: {e}"}