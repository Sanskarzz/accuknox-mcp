# MCP Echo Server with Streamable HTTP Transport

This project implements a [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server using the **FastMCP** framework. FastMCP provides built-in streamable HTTP transport and makes it incredibly easy to create production-ready MCP servers.

## Features

- 🚀 **FastMCP Framework**: Uses the official FastMCP framework for minimal boilerplate
- 🔄 **Automatic HTTP Transport**: Built-in streamable HTTP transport with SSE support
- 🛡️ **Built-in Security**: Automatic CORS, origin validation, and security features
- 🔧 **Echo Tool**: A simple but complete tool implementation for demonstration
- 📡 **Auto Protocol Handling**: Automatic MCP protocol compliance and JSON-RPC handling
- 🎯 **Production Ready**: Includes health checks, logging, and error handling

## Architecture

FastMCP automatically handles all the MCP protocol complexity:

- **Automatic Endpoints**: FastMCP creates all necessary MCP endpoints
- **Protocol Compliance**: Built-in JSON-RPC and MCP protocol handling
- **Transport Layer**: Streamable HTTP transport with SSE support
- **Tool Registration**: Decorator-based tool registration

## Installation

1. **Clone or create the project directory**:
   ```bash
   mkdir mcp-echo-server
   cd mcp-echo-server
   ```

2. **Create and activate a virtual environment** (recommended):
   ```bash
   python3 -m venv mcp-venv
   source mcp-venv/bin/activate  # On Windows: mcp-venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

**Note**: If you get an "externally managed environment" error, you must use a virtual environment as shown above.

## Usage

### Starting the Server

Run the MCP server:

```bash
python server.py
```

The server will start on `http://127.0.0.1:8000` and FastMCP automatically provides:

- **MCP Protocol Endpoints**: All necessary MCP endpoints (automatically configured)
- **Health Checks**: Built-in health monitoring
- **OpenAPI Documentation**: Automatic API documentation at `http://127.0.0.1:8000/docs`
- **Interactive Testing**: Swagger UI for testing tools

### Testing with MCP Inspector

The easiest way to test your server is with the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector
```

Then connect to: `http://127.0.0.1:8000/mcp`

### Using with Cursor

Add this to your Cursor MCP configuration:

```json
{
  "mcp-echo-server": {
    "url": "http://localhost:8000/mcp"
  }
}
```

### Using the Development CLI

FastMCP includes development tools for easy testing:

```bash
# Test your server locally
fastmcp dev server.py

# Run your server with custom transport
fastmcp run server.py --transport http --port 8000
```

## Echo Tool

The server provides a simple echo tool with the following features:

### Parameters

- **message** (required): The text message to echo back
- **repeat** (optional): Number of times to repeat the message (1-10, default: 1)

### Example Usage

```json
{
  "name": "echo",
  "arguments": {
    "message": "Hello, World!",
    "repeat": 3
  }
}
```

### Response

```json
{
  "content": [
    {
      "type": "text",
      "text": "Echo (3x): Hello, World!\nHello, World!\nHello, World!"
    }
  ]
}
```

## Implementation Details

### FastMCP Framework

This implementation uses the FastMCP framework which provides:

- **Automatic Protocol Handling**: All MCP protocol details handled automatically
- **Decorator-based Tools**: Simple `@mcp.tool()` decorator for tool registration
- **Type Safety**: Full type hints and automatic schema generation
- **Built-in HTTP Server**: Production-ready HTTP server with streamable transport
- **Error Handling**: Automatic error handling and JSON-RPC compliance

### Tool Development

Creating tools with FastMCP is extremely simple:

```python
@mcp.tool()
def my_tool(param1: str, param2: int = 10) -> str:
    """Tool description here."""
    return f"Result: {param1} repeated {param2} times"
```

FastMCP automatically:
- Generates JSON schema from type hints
- Validates inputs and outputs
- Handles errors and exceptions
- Registers tools with the MCP protocol

### Security and Production Features

- **Built-in Security**: FastMCP includes CORS, origin validation, and other security features
- **Localhost Binding**: Server binds to localhost by default
- **Logging**: Comprehensive logging for debugging and monitoring
- **Health Checks**: Automatic health check endpoints

## Project Structure

```
mcp-echo-server/
├── server.py              # FastMCP server with echo tool
├── requirements.txt       # Python dependencies  
├── run_server.sh          # Convenient startup script
└── README.md             # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Dependencies

- **fastmcp**: FastMCP framework for easy MCP server development

FastMCP includes all necessary dependencies internally:
- FastAPI for the web framework
- Uvicorn for the ASGI server
- Starlette for SSE support  
- Pydantic for data validation
- Full MCP protocol support

## License

This project is provided as an example implementation. Feel free to use, modify, and distribute as needed.

## References

- [Model Context Protocol Specification](https://modelcontextprotocol.io/specification/)
- [MCP Streamable HTTP Transport](https://modelcontextprotocol.io/specification/draft/basic/transports#streamable-http)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Christian Posta's MCP Authorization Blog Series](https://blog.christianposta.com/understanding-mcp-authorization-step-by-step/) 