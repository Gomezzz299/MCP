from database.db_utils import cargar_contexto_desde_sqlite
from typing import Optional

def obtener_contexto_global(db_path: Optional[str]) -> str:
    if not db_path:
        return ""
    
    contexto_dict = cargar_contexto_desde_sqlite(db_path)
    if not contexto_dict:
        return ""
    
    contexto_str = "\n".join(f"{k}: {v}" for k, v in contexto_dict.items())
    return f"CONTEXTUAL DATA:\n{contexto_str}\n"