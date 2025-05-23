from decoradores.utils import responder_con_llm

class AgenteEstadoServidor:
    """
    Agente que informa sobre el estado del servidor MCP.
    """
    def __init__(self, llm: object):
        self.llm = llm

    @responder_con_llm
    def _responder(self, mensaje: str) -> dict:
        """
        Devuelve el estado del servidor incluyendo carga, uptime y memoria.

        Returns:
            dict: Información estructurada del estado del servidor
        """
        return {
            "estado": "activo",
            "uptime_horas": 15,
            "carga_cpu": "23%",
            "memoria_libre": "3.1 GB"
        }