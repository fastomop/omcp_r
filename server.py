import asyncio
from mcp import Server, ServerConfig
from mcp.stdio import stdio_server
from omcp_py.tools.run_python import RunPythonTool

async def main():
    # Configure the MCP server
    config = ServerConfig(
        name="Python Sandbox",
        description="A sandbox for executing Python code safely"
    )
    
    # Create the server with our tool
    server = Server(config)
    server.add_tool(RunPythonTool())
    
    # Start the server using stdio
    await stdio_server(server)

if __name__ == "__main__":
    asyncio.run(main())
import asyncio
from mcp import Server, ServerConfig, Tool, ToolInput, ToolOutput
from mcp.stdio import stdio_server
from mcp.client.sse import sse_client
from mcp import ClientSession

class PythonSandboxProxy(Tool):
    """Proxy tool that forwards Python execution requests to the Docker-based sandbox"""
    
    def __init__(self):
        super().__init__(
            name="run_python_code",
            description="Run Python code in a secure sandboxed environment",
            input_schema={
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
        self.sandbox_url = "http://localhost:8000"
        
    async def execute(self, params: ToolInput) -> ToolOutput:
        code = params.get("code")
        
        async with sse_client(self.sandbox_url) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool('run_python_code', {'python_code': code})
                return ToolOutput({"result": result.content[0].text})

async def main():
    # Configure the MCP server
    config = ServerConfig(
        name="OMCP Python Environment",
        description="Tools for OMOP data manipulation with sandboxed Python execution"
    )
    
    # Create the server with our proxy tool
    server = Server(config)
    server.add_tool(PythonSandboxProxy())
    
    # Start the server using stdio
    await stdio_server(server)

if __name__ == "__main__":
    asyncio.run(main())
