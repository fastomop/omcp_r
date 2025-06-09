"""
Main MCP Server - Standard MCP implementation for Python sandbox.

Sets up the MCP server with sandbox management tools, proper logging,
and error handling following MCP conventions.
"""

import asyncio
import logging
import sys
from typing import Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.shared import ServerConfig

from omcp_py.tools.sandbox_tools import CreateSandboxTool, ListSandboxesTool, RemoveSandboxTool
from omcp_py.tools.execution_tools import ExecutePythonTool, InstallPackageTool
from omcp_py.utils.config import get_config

# Load configuration and setup logging
config = get_config()
logging.basicConfig(
    level=config.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr  # Log to stderr as per MCP convention
)

logger = logging.getLogger(__name__)

def create_server() -> Server:
    """Create and configure the MCP server with all tools."""
    # Create server config with metadata
    server_config = ServerConfig(
        name="omcp-sandbox",
        version="0.1.0",
        description="A secure Python code execution sandbox for MCP",
        debug=config.debug
    )
    
    # Initialize server
    server = Server(server_config)
    
    # Register all available tools
    tools = [
        CreateSandboxTool(),
        ListSandboxesTool(),
        RemoveSandboxTool(),
        ExecutePythonTool(),
        InstallPackageTool()
    ]
    
    # Add tools to server
    for tool in tools:
        server.add_tool(tool)
        logger.debug(f"Registered tool: {tool.name}")
    
    return server

async def main() -> Optional[int]:
    """Main entry point - start the MCP server."""
    try:
        logger.info("Starting MCP sandbox server...")
        server = create_server()
        
        # Log registered tools for debugging
        tool_names = [tool.name for tool in server.tools]
        logger.info("Registered tools: %s", ", ".join(tool_names))
        
        # Start server with stdio transport
        await stdio_server(server)
        return 0
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        return 0
    except Exception as e:
        logger.error("Server stopped due to error: %s", e, exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
