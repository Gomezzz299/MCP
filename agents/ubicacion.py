import requests
from decoradores.utils import responder_con_llm

class AgenteUbicacion:
    """
    Agente que obtiene la ubicación aproximada del usuario mediante su IP.
    """
    def __init__(self, llm: object):
        self.llm = llm

    @responder_con_llm
    def _responder(self, mensaje: str, registry: dict = None) -> dict:
        """
        Responde con la ciudad y país del usuario obtenidos por IP.

        Returns:
            dict: Datos con ciudad y país, o error
        """
        try:
            response = requests.get("https://ipinfo.io/json")
            data = response.json()
            return {
                "ciudad": data.get("city", "desconocida"),
                "pais": data.get("country", "desconocido")
            }
        except Exception:
            return {"error": "No se pudo obtener la ubicación."}