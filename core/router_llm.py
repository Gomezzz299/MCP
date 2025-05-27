import os
import re
import importlib
from typing import Optional, Dict, Tuple, Type

from core.ollama_wrapper import OllamaLLM
from config import DEFAULT_OLLAMA_MODEL, DEEPSEEK_MODEL
from core.context_loader import obtener_contexto_global


class LLMRouter:
    """
    Router para elegir el modelo LLM y agente más adecuado según el contenido del mensaje.

    Este router:
    - Carga dinámicamente las clases de agentes y sus patrones desde archivos Python en la carpeta `agentes`.
    - Mantiene dos modelos LLM:
        * `llm_simple`: modelo ligero para respuestas guiadas por agentes.
        * `llm_complex`: modelo potente para respuestas generales.
    - Decide qué agente usar basado en la detección de patrones en el mensaje.
    """

    def __init__(self, db_path: str = "database/context.db", agents_folder: str = "agentes"):
        """
        Inicializa el router con las rutas a la base de datos y carpeta de agentes,
        y carga los agentes dinámicamente.

        Args:
            db_path (str): Ruta al archivo SQLite con contexto global.
            agents_folder (str): Carpeta donde se encuentran los módulos agentes.
        """
        self.db_path = db_path
        self.agents_folder = agents_folder
        self.llm_simple = OllamaLLM(DEFAULT_OLLAMA_MODEL)
        self.llm_complex = OllamaLLM(DEEPSEEK_MODEL)
        self.agentes = self._cargar_agentes()

    def _cargar_agentes(self) -> Dict[str, dict]:
        """
        Escanea la carpeta de agentes, importa cada módulo y extrae las clases
        que definen agentes (clases con atributo `patrones`).

        Cada agente se instancia con el LLM correspondiente y sus patrones
        se compilan en expresiones regulares para facilitar la detección.

        Returns:
            Dict[str, dict]: Diccionario con nombre del agente como clave y
                             diccionario con instancia y patrones compilados.
        """
        agentes = {}

        for filename in os.listdir(self.agents_folder):
            # Ignorar archivos no Python, archivos base y privados
            if not filename.endswith(".py") or filename in ["base.py", "__init__.py"] or filename.startswith("_"):
                continue

            module_name = filename[:-3]  # quitar extensión .py
            module_path = f"{self.agents_folder}.{module_name}"

            try:
                module = importlib.import_module(module_path)
            except Exception as e:
                print(f"[ERROR] No se pudo importar {module_path}: {e}")
                continue

            # Buscar clases con atributo 'patrones' en el módulo
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and hasattr(attr, "patrones") and isinstance(attr.patrones, list):
                    # Determinar si el agente requiere el LLM experto (opcional)
                    llm = self.llm_complex if getattr(attr, "llm_experto_required", False) else self.llm_simple
                    instancia = attr(llm=llm)
                    agentes[attr_name.lower()] = {
                        "instancia": instancia,
                        "patrones": [re.compile(p, re.IGNORECASE) for p in attr.patrones]
                    }

        return agentes

    def elegir_agente(self, mensaje: str) -> Tuple[OllamaLLM, Optional[Type]]:
        """
        Elige el modelo LLM y la clase de agente según el mensaje.

        Escanea el mensaje para detectar coincidencias con los patrones de los agentes.
        Si hay coincidencia, retorna el modelo simple y la clase del agente correspondiente.
        Si no, retorna el modelo complejo y None para el agente.

        Args:
            mensaje (str): Mensaje del usuario.

        Returns:
            Tuple[OllamaLLM, Optional[Type]]: Modelo LLM a usar y clase del agente (o None).
        """
        texto = mensaje.lower()
        for nombre, datos in self.agentes.items():
            if any(patron.search(texto) for patron in datos["patrones"]):
                clase_agente = datos["instancia"].__class__
                return self.llm_simple, clase_agente

        return self.llm_complex, None

    def enrutar_a_llm(self, mensaje: str, modelo=None, db_path: Optional[str] = None) -> str:
        """
        Genera una respuesta del modelo LLM con contexto global opcional.

        Args:
            mensaje (str): Mensaje del usuario.
            modelo (OllamaLLM, opcional): Modelo LLM a usar. Por defecto `llm_complex`.
            db_path (str, opcional): Ruta al archivo de contexto global. Si no se pasa, usa la ruta por defecto.

        Returns:
            str: Respuesta generada por el LLM.
        """
        modelo = modelo or self.llm_complex
        contexto = obtener_contexto_global(db_path or self.db_path)
        prompt = f"{contexto}Usuario: {mensaje}\nAsistente:"
        return modelo.responder(prompt)
