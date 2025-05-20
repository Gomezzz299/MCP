from server.mcp_server import MCPServer

if __name__ == "__main__":
    mcp = MCPServer(debug=True)
    print("🤖 MCP Server iniciado. Escribe tu pregunta (o 'salir')")
    while True:
        user_input = input("🧑 Tú: ")
        if user_input.lower() == "salir":
            break
        print("🤖", mcp.procesar(user_input))