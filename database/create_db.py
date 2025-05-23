import sqlite3

# Ruta a la base de datos
DB_PATH = "database/context.db"

# Patrones por agente
datos_iniciales = {
    "AgenteClima": [
        r"\bclima\b", r"\btiempo\b", r"\btemperatura\b",
        r"\bqué d[ií]a hace\b", r"\bc[oó]mo est[aá] el d[ií]a\b", r"\bc[oó]mo est[aá] el tiempo\b"
    ],
    "AgenteFecha": [
        r"\bfecha\b", r"\bd[ií]a es\b", r"\bqué d[ií]a es\b",
        r"\bhora\b", r"\bqué hora\b", r"\bhoy\b"
    ],
    "AgenteUbicacion": [
        r"\búbicaci[oó]n\b", r"\bd[oó]nde estoy\b", r"\blugar\b"
    ]
}

# Crear la tabla y poblarla
def inicializar_bd():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Crear tabla si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patrones_agentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agente TEXT NOT NULL,
            patron TEXT NOT NULL,
            UNIQUE(agente, patron)
        )
    """)

    # Insertar los patrones evitando duplicados
    for agente, patrones in datos_iniciales.items():
        for patron in patrones:
            try:
                cursor.execute(
                    "INSERT INTO patrones_agentes (agente, patron) VALUES (?, ?)",
                    (agente, patron)
                )
            except sqlite3.IntegrityError:
                pass  # Ya existe

    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada con patrones de agentes.")

if __name__ == "__main__":
    inicializar_bd()
