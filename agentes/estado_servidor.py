import psutil
import time
from utils.agente_base import AgenteBase


class AgenteEstadoServidor(AgenteBase):
    """
    Agente que informa sobre el estado del servidor MCP.
    """
    patrones = [
        r"\bestado del servidor\b",
        r"\best[aá] activo el servidor\b",
        r"\bestado de funcionamiento\b",
        r"\best[aá] ca[ií]do el servidor\b",
        r"\bc[oó]mo est[aá] el servidor\b",
        r"\buptime\b",
        r"\bmemoria disponible\b",
        r"\bcarga del sistema\b",
        r"\bcpu\b",
        r"\buso de memoria\b"
    ]

    def agente(self) -> dict:
        """
        Devuelve el estado del servidor incluyendo carga, uptime y memoria.

        Returns:
            dict: Información estructurada del estado del servidor
        """
        # Uptime (en horas)
        uptime_segundos = time.time() - psutil.boot_time()
        uptime_horas = round(uptime_segundos / 3600, 2)

        # Carga CPU y memoria
        carga_cpu = psutil.cpu_percent(interval=1)
        memoria_libre = round(psutil.virtual_memory().available / (1024 ** 3), 2)

        return {
            "success": True,
            "data": {
                "estado": "activo",
                "uptime_horas": uptime_horas,
                "carga_cpu": f"{carga_cpu}%",
                "memoria_libre": f"{memoria_libre} GB"
            }
        }