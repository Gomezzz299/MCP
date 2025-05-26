from database.db_utils import cargar_contexto_desde_sqlite
from typing import Optional

def obtener_contexto_global(db_path: Optional[str]) -> str:
    """
    Obtiene el contexto global almacenado en la base de datos SQLite.

    Esta función carga un diccionario con datos clave-valor desde la tabla de contexto
    y los concatena en un string legible para ser usado como contexto en prompts LLM.

    Args:
        db_path (Optional[str]): Ruta al archivo SQLite que contiene la tabla de contexto.
                                 Si es None o no existe, retorna cadena vacía.

    Returns:
        str: Cadena con el contexto formateado para incluir en el prompt, o cadena vacía si no hay contexto.
    """
    if not db_path:
        # No hay ruta válida, devolver contexto vacío
        return ""
    
    contexto_dict = cargar_contexto_desde_sqlite(db_path)
    if not contexto_dict:
        # No se pudo cargar contexto o está vacío
        return ""
    
    # Formatear el diccionario en líneas "clave: valor"
    contexto_str = "\n".join(f"{k}: {v}" for k, v in contexto_dict.items())
    return f"CONTEXTUAL DATA:\n{contexto_str}\n"
