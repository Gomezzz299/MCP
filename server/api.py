from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from server.mcp_server import MCPServer

# Crear instancia de la aplicación FastAPI
app = FastAPI()

# Inicializar el servidor MCP con modo de depuración activado
mcp = MCPServer(debug=True)

# Configuración del middleware CORS
# Permite que clientes en otros dominios (como localhost:4200 de Angular) puedan hacer peticiones al backend
# ⚠️ En producción deberías reemplazar allow_origins=["*"] por una lista específica de dominios permitidos.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # Permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],            # Permitir todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],            # Permitir todos los encabezados
)

@app.post("/process")
async def procesar(request: Request):
    """
    Punto de entrada principal para procesar preguntas desde el cliente.

    Este endpoint espera una petición POST con un cuerpo JSON que contenga la clave "pregunta".
    Luego utiliza el servidor MCP para procesar esa pregunta y devuelve la respuesta generada.

    Args:
        request (Request): Objeto de solicitud HTTP con cuerpo JSON.

    Returns:
        dict: Respuesta con una clave "respuesta" que contiene el texto generado.
    """
    # Extraer el cuerpo JSON de la petición
    data = await request.json()
    pregunta = data.get("pregunta", "")

    # Procesar la pregunta usando MCP
    respuesta = mcp.procesar_mensaje(pregunta)

    # Devolver la respuesta como JSON
    return {"respuesta": respuesta}
