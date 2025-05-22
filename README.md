# 🧠 MCP: Multi-Agent Control Point

Este proyecto implementa un servidor multi-agente que enruta preguntas del usuario a un modelo LLM o a agentes especializados (como fecha, ubicación, clima o un experto técnico). Incluye una interfaz web sencilla construida con Streamlit para facilitar su uso.

---

## 🚀 Características

- 🌐 Backend con FastAPI
- 🧠 Agentes especializados (fecha, ubicación, clima, experto LLM)
- 🤖 Lógica inteligente para que los agentes colaboren entre sí
- 🖥️ Interfaz visual con Streamlit (GUI)
- 🐳 Contenedores Docker para fácil despliegue
- 🔌 Comunicación cliente-servidor lista para red local o remoto

---

## 📁 Estructura del proyecto

```
MCP/
├── core/
│   ├── registry.py          # Registra todos los agentes
│   └── router_llm.py        # Permite distribución entre agentes
├── agents/
│   ├── fecha.py             # Agente de fecha/hora
│   ├── ubicacion.py         # Agente de geolocalización (por IP)
│   └── clima.py             # Agente de clima (usa ubicación)
├── server/
│   ├── mcp_server.py        # Lógica del MCP
│   └── api.py               # Backend FastAPI
├── gui/
│   ├── app.py               # Interfaz Streamlit
│   └── .streamlit/
│       └── secrets.toml     # Configuración del backend
├── utils/
│   └── json_parser.py       # Función para dividir json
├── decoradores/
│   └── utils.py             # Decorador para manejar LLM y respuestas
├── requirements.txt         # Dependencias comunes
├── Dockerfile.backend       # Imagen del backend
├── Dockerfile.frontend      # Imagen del frontend
└── docker-compose.yml       # Orquestación de servicios
```

---

## ⚙️ Requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## 🧪 Instalación rápida

### 1. Clona el repositorio

```bash
git clone https://github.com/tu-usuario/MCP.git
cd MCP
```

### 2. Crea archivo de configuración para Streamlit

Dentro del directorio `gui`, crea el archivo:

```
gui/.streamlit/secrets.toml
```

Con el siguiente contenido:

```toml
server_url = "http://backend:8000/process"
```

### 3. Ejecuta con Docker Compose

```bash
docker-compose up --build
```

Esto construirá y levantará dos contenedores:

- Backend en `http://localhost:8000`
- Interfaz gráfica en `http://localhost:8501`

---

## 🌍 Acceso desde otra máquina (opcional)

1. Asegúrate de exponer correctamente los puertos (`8000`, `8501`).
2. Usa la IP de la máquina servidor en lugar de `localhost` en `secrets.toml`.
3. También puedes configurar redes Docker personalizadas para acceso cruzado entre hosts.

---

## 📦 Para producción

Puedes ejecutar solo el backend si deseas integrarlo con otra interfaz:

```bash
docker build -f Dockerfile.backend -t mcp_backend .
docker run -p 8000:8000 mcp_backend
```

---

## ✨ Ejemplo de uso

En la interfaz web, puedes escribir preguntas como:

- `¿Qué día es hoy?`
- `¿Dónde estoy?`
- `¿Qué clima hace?`
- `Explícame qué es Python`

La aplicación decidirá si responder directamente o delegar la pregunta a un agente.

---

## 🛠️ Agentes disponibles

| Agente       | Función                                 |
|--------------|------------------------------------------|
| FECHA        | Devuelve la fecha y hora actuales        |
| UBICACION    | Detecta la ciudad y país mediante IP     |
| CLIMA        | Devuelve el clima en la ubicación actual |

---

## 🔄 Interacción entre agentes

El agente de clima ahora usa directamente el agente de ubicación para determinar coordenadas geográficas (`lat`, `lon`) y ciudad antes de consultar el clima, permitiendo respuestas adaptadas al lugar real del usuario. Esto mejora la modularidad y colaboración entre agentes.

---

## ⚠️ Notas técnicas importantes

- Los agentes devuelven datos estructurados (`dict`) y luego se genera la respuesta natural mediante el decorador @responder_con_llm.

- Los agentes que necesitan datos de otros agentes deben invocar métodos internos, no los decorados (para evitar recibir solo texto).

- Cada agente especifica qué modelo de LLM utilizar (`llm_simple` o `llm_experto`).

## 📄 Licencia

Este proyecto está licenciado bajo MIT License.

---

## 🙋‍♂️ Autor

Desarrollado por Alejandro Gómez Sierra.