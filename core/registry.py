from agents.fecha_hora import AgenteFecha
from agents.ubicacion import AgenteUbicacion
from agents.clima import AgenteClima
from agents.estado_servidor import AgenteEstadoServidor
from agents.base import AgenteBase
from typing import Dict, Any



class AgentRegistry:
    """
    Registra manualmente los agentes del sistema.
    """

    def __init__(self, llm_router):
        self.llm_router = llm_router
        self.llm_simple = self.llm_router.llm_simple
        self.llm_experto = self.llm_router.llm_complex

        self.agentes = {
            "fecha": AgenteFecha(llm=self.llm_simple),
            "ubicacion": AgenteUbicacion(llm=self.llm_simple),
            "clima": AgenteClima(llm=self.llm_experto),
            
        }

    def encontrar_agente(self, mensaje: str):
        """
        Devuelve el primer agente disponible para responder.

        Args:
            mensaje (str): Pregunta del usuario.

        Returns:
            Agente adecuado.
        """
        return self.agentes[0] if self.agentes else None
