import requests
from decoradores.utils import responder_con_llm
from agents.ubicacion import AgenteUbicacion

class AgenteClima:
    """
    Agente que proporciona el clima actual para una ubicación fija (Madrid).
    """
    def __init__(self, llm: object):
        self.llm = llm

    @responder_con_llm
    def _responder(self, mensaje: str, registry: dict = None) -> dict:
        try:
            agente_ubicacion = AgenteUbicacion(llm=self.llm)
            ubicacion = agente_ubicacion.obtener_ubicacion()
            print("DEBUG - ubicación:", ubicacion)

            if not isinstance(ubicacion, dict) or not ubicacion.get("success"):
                return {
                    "success": False,
                    "error": "No se pudo determinar la ubicación para consultar el clima."
                }

            ciudad = ubicacion["data"].get("ciudad", "desconocida")
            loc = ubicacion["data"].get("loc")
            print("DEBUG - loc:", loc)
            if not loc:
                return {
                    "success": False,
                    "error": "No se encontró la latitud/longitud en la ubicación."
                }

            lat, lon = map(float, loc.split(','))

            url = (
                f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
                "&current_weather=true"
            )
            r = requests.get(url)
            data = r.json()
            print("DEBUG - clima raw data:", data)
            weather = data.get("current_weather", {})

            return {
                "success": True,
                "data": {
                    "ciudad": ciudad,
                    "temperatura": weather.get("temperature"),
                    "unidad": "°C",
                    "viento": weather.get("windspeed"),
                    "descripcion": weather.get("weathercode")
                }
            }
        except Exception as e:
            print("DEBUG - error en clima:", e)
            return {
                "success": False,
                "error": f"No se pudo obtener el clima: {e}"
            }
