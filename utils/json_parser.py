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
    inicio = texto.find('{')  # Busca la primera aparición de una llave de apertura
    if inicio == -1:
        return None  # Si no hay '{', no hay JSON posible

    # Recorre carácter a carácter desde la llave de apertura hasta el final del texto
    for fin in range(inicio + 1, len(texto) + 1):
        fragmento = texto[inicio:fin]  # Extrae el fragmento actual desde la llave
        try:
            return json.loads(fragmento)  # Intenta parsearlo como JSON
        except json.JSONDecodeError:
            continue  # Si falla, avanza al siguiente carácter y vuelve a intentar

    return None  # Si no se encontró un JSON válido, retorna None
