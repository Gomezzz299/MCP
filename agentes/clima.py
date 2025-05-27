import requests
from utils.agente_base import AgenteBase
from agentes.ubicacion import AgenteUbicacion

class AgenteClima(AgenteBase):
    """
    Agente que proporciona el clima actual según la ubicación del usuario.
    """
    patrones = [
        r"\bclima\b",
        r"\btiempo\b",
        r"\bqu[eé] tiempo hace\b",
        r"\bc[oó]mo est[aá] el clima\b",
        r"\bc[oó]mo est[aá] el tiempo\b",
        r"\bqu[eé] clima hay\b",
        r"\bqu[eé] clima hace\b",
        r"\btemperatura\b",
        r"\bva a llover\b",
        r"\bhace fr[ií]o\b",
        r"\bhace calor\b",
        r"\best[aá] lloviendo\b",
        r"\bpron[oó]stico\b"
    ]

    def agente(self) -> dict:
        agente_ubicacion = AgenteUbicacion(llm=self.llm)
        ubicacion = agente_ubicacion.agente()

        if not isinstance(ubicacion, dict) or not ubicacion.get("success"):
            return {
                "success": False,
                "error": "No se pudo determinar la ubicación para consultar el clima."
            }

        ciudad = ubicacion["data"].get("ciudad", "desconocida")
        loc = ubicacion["data"].get("loc")
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
        weather = data.get("current_weather", {})

        return {
            "ciudad": ciudad,
            "temperatura": weather.get("temperature"),
            "unidad": "°C",
            "viento": weather.get("windspeed"),
            "descripcion": weather.get("weathercode")
        }