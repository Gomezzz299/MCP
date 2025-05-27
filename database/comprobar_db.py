import sqlite3

# Ruta a la base de datos SQLite que contiene los patrones por agente
DB_PATH = "database/context.db"

def mostrar_patrones():
    """
    Muestra por consola los patrones registrados para cada agente desde una base de datos SQLite.

    Esta función se conecta a la base de datos especificada en DB_PATH, verifica si existe
    la tabla 'patrones_agentes' y, si existe, imprime todos los patrones agrupados por agente.

    La tabla `patrones_agentes` debe tener al menos dos columnas:
        - agente (str): nombre del agente.
        - patron (str): expresión regular asociada al agente.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Verificar si la tabla 'patrones_agentes' existe
    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='patrones_agentes';
    """)
    if cursor.fetchone() is None:
        print("⚠️ La tabla 'patrones_agentes' no existe.")
        return

    # Consultar todos los patrones registrados, ordenados por agente
    cursor.execute("""
        SELECT agente, patron FROM patrones_agentes ORDER BY agente;
    """)
    filas = cursor.fetchall()

    if not filas:
        print("ℹ️ No hay patrones registrados.")
        return

    # Mostrar los patrones agrupados por agente
    print("📄 Patrones por agente:")
    agente_actual = None
    for agente, patron in filas:
        if agente != agente_actual:
            if agente_actual is not None:
                print()  # Salto de línea entre agentes
            print(f"🔹 {agente}:")
            agente_actual = agente
        print(f"   - {patron}")

    conn.close()

# Punto de entrada cuando se ejecuta este archivo como script
if __name__ == "__main__":
    mostrar_patrones()
