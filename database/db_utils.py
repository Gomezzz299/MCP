import sqlite3
from typing import Dict, Optional

def cargar_contexto_desde_sqlite(path: str) -> Optional[Dict[str, str]]:
    """
    Carga datos de contexto desde una base de datos SQLite.

    Esta función se conecta a una base de datos SQLite localizada en `path`,
    lee todos los pares clave-valor de la tabla `contexto` y los devuelve
    como un diccionario.

    La tabla `contexto` debe tener exactamente dos columnas: clave y valor.

    Args:
        path (str): Ruta al archivo de base de datos SQLite.

    Returns:
        Optional[Dict[str, str]]: Diccionario con los datos de contexto si la lectura es exitosa,
        o None si ocurre algún error.
    """
    try:
        # Conexión a la base de datos
        conn = sqlite3.connect(path)
        cursor = conn.cursor()

        # Obtener todas las filas de la tabla `contexto`
        cursor.execute("SELECT * FROM contexto")
        filas = cursor.fetchall()

        # Cerrar la conexión
        conn.close()

        # Convertir a diccionario (clave, valor)
        return {clave: valor for clave, valor in filas}
    except Exception as e:
        print(f"[ERROR DB]: {e}")
        return None
