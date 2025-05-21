from datetime import datetime
from decoradores.utils import responder_con_llm

class AgenteFecha:
    """
    Agente que responde con la fecha o la hora actual según el mensaje.
    """
    def __init__(self, llm: object):
        self.llm = llm

    @responder_con_llm
    def _responder(self, mensaje: str, registry: dict = None) -> dict:
        """
        Responde con la fecha u hora actual si se detecta en el mensaje.

        Args:
            mensaje (str): Pregunta del usuario
            registry (dict, optional): Registro de agentes

        Returns:
            dict: Datos estructurados con la fecha u hora
        """
        '''
        if "fecha" in mensaje.lower() or "día" in mensaje.lower():
            return {"fecha": datetime.now().strftime("%d de %B del %Y")}
        elif "hora" in mensaje.lower():
            return {"hora": datetime.now().strftime("%H:%M:%S")}
        else:
            return {"error": "Consulta de fecha/hora no reconocida."}
        '''
        try:
            now = datetime.now()
            return {
                "success": True,
                "data": {
                    "fecha": now.strftime("%Y-%m-%d"),
                    "dia_semana": now.strftime("%A")
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error al obtener la fecha: {e}"
            }