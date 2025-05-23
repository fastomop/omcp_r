import asyncio
from mcp import Server, ServerConfig, Tool, ToolInput, ToolOutput, StdioServerParameters, ClientSession
from mcp.stdio import stdio_server, stdio_client
from mcp.client.sse import sse_client
from omcp_py.tools.run_python import RunPythonTool

# Optional: a proxy tool to forward requests to a Docker-based sandbox. Uncomment if desired.
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
        # Example using sse_client with a URL:
        async with sse_client(self.sandbox_url) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool('run_python_code', {'python_code': code})
                return ToolOutput({"result": result.content[0].text})

# Define server parameters for the MCP Run Python server using Deno.
server_params = StdioServerParameters(
    command='deno',
    args=[
        'run',
        '-N',
        '-R=node_modules',
        '-W=node_modules',
        '--node-modules-dir=auto',
        'jsr:@pydantic/mcp-run-python',
        'stdio'
    ]
)
# The server_params object can be used in creating a stdio_client for integrations.

async def main():
    # Configure the MCP server
    config = ServerConfig(
        name="OMCP Python Environment",
        description="Tools for sandboxed Python execution"
    )
    
    # Create the server and add your tools.
    server = Server(config)
    
    # Add local tool for direct Python code execution.
    server.add_tool(RunPythonTool())
    
    # Optionally, add the proxy tool for Docker-based execution:
    # server.add_tool(PythonSandboxProxy())
    
    # Start the server using stdio.
    await stdio_server(server)

if __name__ == "__main__":
    asyncio.run(main())
