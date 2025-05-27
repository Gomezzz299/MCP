import sqlite3
import re
from utils.agente_base import AgenteBase

class AgenteConsultaSQLLLM(AgenteBase):
    patrones = [
        # Consultas genéricas
        r"\bconsulta\b",
        r"\bdame\b",
        r"\bmuestra\b",
        r"\bbusca\b",
        r"\bhay\b",
        r"\bexiste\b",
        r"\bver\b",
        r"\bfiltra\b",
        r"\bresultados\b",
        r"\bdatos\b",
        r"\bregistros\b",
        r"\btabla\b",
        r"\binformaci[oó]n\b",

        # Preguntas comunes
        r"\bcu[aá]les son\b",
        r"\bqu[eé] datos hay\b",
        r"\bqu[eé] registros hay\b",
        r"\bqu[eé] hay en\b",
        r"\bpuedes mostrar\b",
        r"\bme ense[ñn]as\b",
        r"\bmu[eé]strame\b",
        r"\bd[ée]jame ver\b",
        r"\bhaz una consulta\b",
    ]

    def __init__(self, llm, db_path="database/context.db"):
        super().__init__(llm)
        self.db_path = db_path

    def responder(self, mensaje: str) -> str:
        self.ultimo_mensaje = mensaje
        return super().responder(mensaje)

    def agente(self) -> dict:
        mensaje = self.ultimo_mensaje
        try:
            schema = self._get_db_schema()

            prompt_sql = (
                "Eres un experto en SQL con acceso a la siguiente base de datos SQLite:\n"
                f"{schema}\n\n"
                f"Usuario: {mensaje}\n\n"
                "Genera únicamente una consulta SQL de solo lectura (SELECT), sin explicaciones, sin comentarios y en una línea."
            )

            sql = self.llm.responder(prompt_sql).strip().split("\n")[0]

            # Validar que sea una consulta segura
            if not self._es_consulta_segura(sql):
                return {"error": "La consulta generada no es segura. Solo se permiten SELECTs."}

            # Ejecutar la consulta
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(sql)
                resultados = [dict(row) for row in cursor.fetchall()]

            return {
                "consulta_sql": sql,
                "total_encontrados": len(resultados),
                "resultados": resultados
            }

        except Exception as e:
            return {"error": str(e)}

    def _get_db_schema(self) -> str:
        schema = ""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tablas = [row[0] for row in cursor.fetchall()]

            for tabla in tablas:
                cursor = conn.execute(f"PRAGMA table_info({tabla})")
                columnas = [f"{row[1]} ({row[2]})" for row in cursor.fetchall()]
                schema += f"Tabla: {tabla}\n  Columnas: {', '.join(columnas)}\n\n"
        return schema

    def _es_consulta_segura(self, sql: str) -> bool:
        """
        Valida que la consulta sea una instrucción SELECT y no contenga operaciones peligrosas.
        """
        sql_limpia = sql.strip().lower()
        patrones_peligrosos = ["insert", "update", "delete", "drop", "alter", "create", "replace", "truncate"]
        if not sql_limpia.startswith("select"):
            return False
        if any(re.search(rf"\b{p}\b", sql_limpia) for p in patrones_peligrosos):
            return False
        return True
