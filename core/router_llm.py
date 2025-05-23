import os
import re
import importlib
from typing import Optional, Dict, Tuple, Type

from core.ollama_wrapper import OllamaLLM
from config import DEFAULT_OLLAMA_MODEL, DEEPSEEK_MODEL
from core.context_loader import obtener_contexto_global


class LLMRouter:
    """
    Router que elige el modelo LLM más adecuado según el contenido del mensaje.
    Carga los patrones y clases de agente dinámicamente desde la carpeta 'agents'.
    """

    def __init__(self, db_path: str = "database/context.db", agents_folder: str = "agents"):
        self.db_path = db_path
        self.agents_folder = agents_folder
        self.llm_simple = OllamaLLM(DEFAULT_OLLAMA_MODEL)
        self.llm_complex = OllamaLLM(DEEPSEEK_MODEL)
        self.agentes = self._cargar_agentes()

    def _cargar_agentes(self) -> Dict[str, dict]:
        agentes = {}

        for filename in os.listdir(self.agents_folder):
            if not filename.endswith(".py") or filename in ["base.py", "__init__.py"] or filename.startswith("_"):
                continue

            module_name = filename[:-3]  # sin .py
            module_path = f"{self.agents_folder}.{module_name}"

            try:
                module = importlib.import_module(module_path)
            except Exception as e:
                print(f"[ERROR] No se pudo importar {module_path}: {e}")
                continue

            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and hasattr(attr, "patrones") and isinstance(attr.patrones, list):
                    llm = self.llm_experto if getattr(attr, "llm_experto_required", False) else self.llm_simple
                    instancia = attr(llm=llm)
                    agentes[attr_name.lower()] = {
                        "instancia": instancia,
                        "patrones": [re.compile(p, re.IGNORECASE) for p in attr.patrones]
                    }

        return agentes

    def elegir_agente(self, mensaje: str) -> Tuple[OllamaLLM, Optional[Type]]:
        texto = mensaje.lower()
        for nombre, datos in self.agentes.items():
            if any(patron.search(texto) for patron in datos["patrones"]):
                clase_agente = datos["instancia"].__class__
                return self.llm_simple, clase_agente

        return self.llm_complex, None

    def enrutar_a_llm(self, mensaje: str, modelo=None, db_path: Optional[str] = None) -> str:
        modelo = modelo or self.llm_complex
        contexto = obtener_contexto_global(db_path or self.db_path)
        prompt = f"{contexto}Usuario: {mensaje}\nAsistente:"
        return modelo.responder(prompt)
