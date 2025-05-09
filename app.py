# app.py
from fastapi import FastAPI
from fastmcp import FastMCP, Client
from fastmcp.client.transports import PythonStdioTransport
import uvicorn

# 1) Initialize the proxy client with UvxStdioTransport
backend_transport = PythonStdioTransport(script_path="mcp-server-fetch")
backend_client    = Client(backend_transport)

# 2) Create a proxy server with correct SSE and message paths
proxy_server = FastMCP.from_client(
    backend_client,
    name="FetchServer Proxy",
)

# 3) Initialize FastAPI and mount the proxy server's SSE app
app = FastAPI()

# 4) Health check endpoint
@app.get("/ping")
async def ping():
    """
    Health check endpoint that returns a simple pong message.
    Example: curl http://localhost:8000/ping
    Response: {"message": "pong"}
    """
    return {"message": "pong"}

# 5) Test endpoint: trigger communication with the backend MCP server
@app.get("/test")
async def test_tools():
    """
    Calls backend_client.list_tools() to list all available tools on the MCP server.
    Example: curl http://localhost:8000/test
    Response: {"available_tools": [...]}
    """
    async with backend_client:
        tools = await backend_client.list_tools()
        # call tools
        result = await backend_client.call_tool("fetch", {"url": "https://github.com/docker/mcp-servers/"})
        return {"available_tools": tools, "result": result}

app.mount("/", proxy_server.sse_app())


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)
