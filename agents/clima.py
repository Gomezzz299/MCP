import requests
from decoradores.utils import responder_con_llm

class AgenteClima:
    """
    Agente que proporciona el clima actual para una ubicación fija (Madrid).
    """
    def __init__(self, llm: object):
        self.llm = llm

    @responder_con_llm
    def _responder(self, mensaje: str, registry: dict = None) -> dict:
        """
        Devuelve el clima actual (temperatura) de Madrid.

        Returns:
            dict: Información del clima o mensaje de error
        """
        try:
            lat, lon = 40.4168, -3.7038
            url = (
                f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
                "&current_weather=true"
            )
            r = requests.get(url)
            data = r.json()
            weather = data.get("current_weather", {})

            return {
                "success": True,
                "data": {
                    "ciudad": "Madrid",
                    "temperatura": weather.get("temperature"),
                    "unidad": "°C",
                    "viento": weather.get("windspeed"),
                    "descripcion": weather.get("weathercode")  # Puedes mapearlo si quieres
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"No se pudo obtener el clima: {e}"
            }