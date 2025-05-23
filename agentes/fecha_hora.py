from datetime import datetime
from utils.agente_base import AgenteBase

class AgenteFecha(AgenteBase):
    patrones = [
    # Fecha
    r"\bfecha\b",
    r"\bd[ií]a\b",
    r"\bqué d[ií]a es\b",
    r"\bqué fecha\b",
    r"\bcu[aá]l es la fecha\b",
    r"\bd[ií]a actual\b",
    r"\bfecha de hoy\b",
    r"\bhoy qu[eé] d[ií]a es\b",
    r"\bd[ií]a de hoy\b",
    
    # Hora
    r"\bhora\b",
    r"\bqué hora\b",
    r"\bqu[eé] hora es\b",
    r"\bhora actual\b",
    r"\bme dices la hora\b",
    r"\bsabes la hora\b",
    r"\btienes la hora\b",
    r"\bhora por favor\b",
    r"\bcu[aá]l es la hora\b"
]


    def agente(self) -> dict:
        now = datetime.now()
        return {
            "success": True,
            "data": {
                "fecha_completa": now.strftime("%A %d de %B de %Y"),
                "iso": now.strftime("%Y-%m-%d"),
                "dia": now.strftime("%A"),
                "dia_numero": now.strftime("%d"),
                "mes": now.strftime("%B"),
                "anio": now.strftime("%Y"),
                "hora_24h": now.strftime("%H:%M:%S"),
                "hora_12h": now.strftime("%I:%M:%S %p"),
            }
        }
