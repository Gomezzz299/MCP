from datetime import datetime
from typing import Optional, Any


class AgenteFecha:
    """
    Agente especializado en proporcionar la fecha y hora actual
    en respuesta a mensajes que contengan consultas relacionadas.
    """

    def responder(self, mensaje: str, registry: Optional[Any] = None) -> str:
        """
        Responde con la fecha o la hora actual según el contenido del mensaje.

        Args:
            mensaje (str): Mensaje o pregunta del usuario sobre fecha/hora.
            registry (Optional[Any]): Registro de agentes (no usado aquí, pero incluido para interfaz común).

        Returns:
            str: Fecha en formato "dd de Mes del YYYY", hora en "HH:MM:SS"
                 o un mensaje de error si no se entiende la consulta.
        """
        texto = mensaje.lower()
        if "fecha" in texto or "día" in texto:
            return datetime.now().strftime("%d de %B del %Y")
        elif "hora" in texto:
            return datetime.now().strftime("%H:%M:%S")
        else:
            return "No entiendo la consulta de fecha/hora."
