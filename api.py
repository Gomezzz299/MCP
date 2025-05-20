from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from server.mcp_server import MCPServer

app = FastAPI()
mcp = MCPServer(debug=True)

# Permitir peticiones CORS desde cualquier origen (ajusta en producción)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process")
async def procesar(request: Request):
    data = await request.json()
    pregunta = data.get("pregunta", "")
    respuesta = mcp.procesar(pregunta)
    return {"respuesta": respuesta}
