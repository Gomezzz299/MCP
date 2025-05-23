import sqlite3

DB_PATH = "database/context.db"

def mostrar_patrones():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Verificar si la tabla existe
    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='patrones_agentes';
    """)
    if cursor.fetchone() is None:
        print("⚠️ La tabla 'patrones_agentes' no existe.")
        return

    # Consultar patrones por agente
    cursor.execute("""
        SELECT agente, patron FROM patrones_agentes ORDER BY agente;
    """)
    filas = cursor.fetchall()

    if not filas:
        print("ℹ️ No hay patrones registrados.")
        return

    print("📄 Patrones por agente:")
    agente_actual = None
    for agente, patron in filas:
        if agente != agente_actual:
            if agente_actual is not None:
                print()  # Separador entre agentes
            print(f"🔹 {agente}:")
            agente_actual = agente
        print(f"   - {patron}")

    conn.close()

if __name__ == "__main__":
    mostrar_patrones()
