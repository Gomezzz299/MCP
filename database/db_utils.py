import sqlite3
from typing import Dict, Optional

def cargar_contexto_desde_sqlite(path: str) -> Optional[Dict[str, str]]:
    try:
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contexto")
        filas = cursor.fetchall()
        conn.close()
        return {clave: valor for clave, valor in filas}
    except Exception as e:
        print(f"[ERROR DB]: {e}")
        return None
