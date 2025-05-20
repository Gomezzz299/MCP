import requests
from typing import Optional, Any


class AgenteClima:
    """
    Agente encargado de obtener el clima actual en función de la ubicación del usuario.
    Utiliza la API pública de Open-Meteo y depende de los agentes de ubicación y fecha.
    """

    def responder(self, mensaje: str, registry: Optional[Any] = None) -> str:
        """
        Devuelve el clima actual para la ubicación estimada del usuario.

        Este agente depende de otros agentes registrados:
        - UBICACION: para obtener una cadena representando la ciudad y país
        - FECHA: (actualmente no usado directamente, pero puede ser útil si se amplía)

        Args:
            mensaje (str): Mensaje del usuario (no se utiliza directamente).
            registry (Optional[Any]): Registro de agentes que permite acceder a otros agentes.

        Returns:
            str: Una cadena con la temperatura actual o un mensaje de error si falla.
        """
        try:
            # Obtener ubicación (solo como texto para mostrar)
            ubicacion = registry.obtener("UBICACION").responder("obtener_ubicacion", registry)

            # Coordenadas fijas de ejemplo (Madrid)
            lat, lon = 40.4168, -3.7038

            url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat}&longitude={lon}&current_weather=true"
            )
            response = requests.get(url, timeout=5)
            data = response.json()
            temperatura = data["current_weather"]["temperature"]

            return f"En {ubicacion} la temperatura actual es {temperatura}°C."
        except Exception:
            return "No pude obtener el clima."
