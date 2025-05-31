import asyncio
from mcp.server import Server
from mcp.types import Tool, ToolInput, ToolOutput
from mcp.stdio import stdio_server
import httpx

# Proxy tool that forwards Python execution requests to the Node.js Pyodide sandbox
class PythonSandboxProxy(Tool):
    """Proxy tool that forwards Python execution requests to the Node.js Pyodide sandbox"""
    
    def __init__(self):
        super().__init__(
            name="run_python_code",
            description="Run Python code in a secure sandboxed environment",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Python code to execute"
                    }
                },
                "required": ["code"]
            }
        )
        self.sandbox_url = "http://localhost:8000/run"
        
    async def execute(self, params: ToolInput) -> ToolOutput:
        code = params.get("code")
        async with httpx.AsyncClient() as client:
            response = await client.post(self.sandbox_url, json={"code": code})
            data = response.json()
            return ToolOutput({"result": data.get("result"), "error": data.get("error")})

async def main():
    # Create the server and add only the proxy tool for Docker-based execution.
    server = Server()
    server.add_tool(PythonSandboxProxy())
    
    # Start the server using stdio.
    await stdio_server(server)

if __name__ == "__main__":
    asyncio.run(main())
