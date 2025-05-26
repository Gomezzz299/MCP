import requests
from utils.agente_base import AgenteBase

class AgenteUbicacion(AgenteBase):
    """
    Agente que obtiene la ubicación aproximada del usuario mediante su IP.
    """
    patrones = [
        r"\bubicaci[oó]n\b",
        r"\bd[oó]nde estoy\b",
        r"\bd[oó]nde estamos\b",
        r"\bd[oó]nde est[aá]s\b",
        r"\best[aá]s en\b",
        r"\bd[oó]nde queda\b",
        r"\bcu[aá]l es mi ubicaci[oó]n\b",
        r"\bubicado\b",
        r"\bubicaci[oó]n actual\b",
        r"\bd[oó]nde me encuentro\b",
        r"\bd[oó]nde se encuentra\b"
    ]

    def agente(self) -> dict:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        return {
            "ciudad": data.get("city", "desconocida"),
            "region": data.get("region", "desconocida"),
            "pais": data.get("country", "desconocido"),
            "loc": data.get("loc", None)  # formato: "lat,lon"
        }