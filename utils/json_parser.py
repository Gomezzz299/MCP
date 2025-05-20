import json
from typing import Optional, Any

def extraer_json(texto: str) -> Optional[Any]:
    """
    Extrae el primer bloque JSON válido de un texto buscando desde la primera llave '{'.

    Esta función intenta construir progresivamente un fragmento válido de JSON a partir de la primera
    llave de apertura encontrada en el texto. Retorna el primer objeto decodificado correctamente.

    Args:
        texto (str): Texto potencialmente con un JSON embebido.

    Returns:
        Optional[Any]: Diccionario o lista decodificada si se encuentra un JSON válido, o None si no se encuentra.
    """
    inicio = texto.find('{')
    if inicio == -1:
        return None

    for fin in range(inicio + 1, len(texto) + 1):
        fragmento = texto[inicio:fin]
        try:
            return json.loads(fragmento)
        except json.JSONDecodeError:
            continue

    return None
