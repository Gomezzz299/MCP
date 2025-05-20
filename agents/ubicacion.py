import requests
from typing import Optional, Any


class AgenteUbicacion:
    """
    Agente encargado de obtener la ubicación aproximada del usuario
    utilizando un servicio externo basado en la IP pública.
    """

    def responder(self, mensaje: str, registry: Optional[Any] = None) -> str:
        """
        Devuelve la ubicación del usuario (ciudad y país) según su IP.

        Args:
            mensaje (str): Mensaje del usuario (no es usado en este agente).
            registry (Optional[Any]): Registro de agentes (no usado aquí, pero se mantiene para compatibilidad).

        Returns:
            str: Una cadena con la ubicación aproximada o un mensaje de error si no se puede obtener.
        """
        try:
            response = requests.get("https://ipinfo.io/json", timeout=5)
            data = response.json()
            ciudad = data.get("city", "desconocida")
            pais = data.get("country", "desconocido")
            return f"Estás en {ciudad}, {pais}."
        except Exception as e:
            return "No pude obtener la ubicación."
