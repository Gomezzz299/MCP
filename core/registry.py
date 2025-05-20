from agents.fecha_hora import AgenteFecha
from agents.ubicacion import AgenteUbicacion
from agents.clima import AgenteClima
from agents.experto_llm import AgenteLLMExperto
from typing import Dict, Any


class AgentRegistry:
    """
    Registro centralizado de agentes. Permite registrar e invocar
    instancias de agentes por nombre.
    """

    def __init__(self) -> None:
        """
        Inicializa el registro con los agentes predefinidos:
        - FECHA: Devuelve la fecha y hora actuales.
        - UBICACION: Devuelve la ubicación del usuario.
        - CLIMA: Consulta el clima actual en la ubicación.
        - LLM_EXPERTO: Agente LLM generalista para respuestas técnicas.
        """
        self._agentes: Dict[str, Any] = {
            "FECHA": AgenteFecha(),
            "UBICACION": AgenteUbicacion(),
            "CLIMA": AgenteClima(),
            "LLM_EXPERTO": AgenteLLMExperto(),
        }

    def obtener(self, nombre: str) -> Any:
        """
        Obtiene una instancia de un agente dado su nombre.

        Args:
            nombre (str): Identificador del agente (ej. "FECHA", "CLIMA").

        Returns:
            Any: Instancia del agente o None si no se encuentra.
        """
        return self._agentes.get(nombre)

    def registrar(self, nombre: str, agente: Any) -> None:
        """
        Registra dinámicamente un nuevo agente en el sistema.

        Args:
            nombre (str): Nombre clave para identificar el agente.
            agente (Any): Instancia del agente a registrar.
        """
        self._agentes[nombre] = agente
