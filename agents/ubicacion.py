import requests
from decoradores.utils import responder_con_llm

class AgenteUbicacion:
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

    def __init__(self, llm: object):
        self.llm = llm

    def obtener_ubicacion(self) -> dict:
        try:
            response = requests.get("https://ipinfo.io/json")
            data = response.json()
            return {
                "success": True,
                "data": {
                    "ciudad": data.get("city", "desconocida"),
                    "region": data.get("region", "desconocida"),
                    "pais": data.get("country", "desconocido"),
                    "loc": data.get("loc", None)  # formato: "lat,lon"
                }
            }
        except Exception:
            return {"error": "No se pudo obtener la ubicación."}

    @responder_con_llm
    def _responder(self, mensaje: str) -> dict:
        """
        Responde con la ciudad y país del usuario obtenidos por IP.

        Returns:
            dict: Datos con ciudad y país, o error
        """
        try:
            response = requests.get("https://ipinfo.io/json")
            data = response.json()
            return {
                "success": True,
                "data": {
                    "ciudad": data.get("city", "desconocida"),
                    "region": data.get("region", "desconocida"),
                    "pais": data.get("country", "desconocido"),
                    "loc": data.get("loc", None)  # formato: "lat,lon"
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"No se pudo obtener la ubicación: {e}"
            }