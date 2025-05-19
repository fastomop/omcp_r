import asyncio
from mcp import Server, ServerConfig
from mcp.stdio import stdio_server
from .tools.run_python import RunPythonTool

async def main():
    # Configure the MCP server
    config = ServerConfig(
        name="Python Sandbox",
        description="A sandbox for executing Python code safely"
    )
    
    # Create the server with our tools
    server = Server(config)
    server.add_tool(RunPythonTool())
    
    # Start the server using stdio
    await stdio_server(server)

if __name__ == "__main__":
    asyncio.run(main())
