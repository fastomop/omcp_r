import asyncio
import logging
import sys
from typing import Optional, Dict, Any
from mcp.server.fastmcp import FastMCP
from omcp_r.sandbox_manager import SessionManager
from omcp_r.config import get_config

config = get_config()

logging.basicConfig(
    level=config.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)

logger = logging.getLogger(__name__)

mcp = FastMCP("R Sandbox")

session_manager = SessionManager(config)

@mcp.tool()
async def create_session(timeout: Optional[int] = 300) -> Dict[str, Any]:
    """Start a new persistent R session."""
    try:
        session_id = session_manager.create_session()
        session_info = next(
            (s for s in session_manager.list_sessions() if s["id"] == session_id),
            None
        )
        if not session_info:
            raise Exception("Failed to get session information after creation")
        return {
            "success": True,
            "session_id": session_id,
            "created_at": session_info["created_at"],
            "last_used": session_info["last_used"],
            "host_port": session_info["host_port"]
        }
    except Exception as e:
        logger.error(f"Failed to create R session: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def list_sessions() -> Dict[str, Any]:
    """List all active R sessions."""
    try:
        sessions = session_manager.list_sessions()
        return {
            "success": True,
            "sessions": sessions,
            "count": len(sessions)
        }
    except Exception as e:
        logger.error(f"Failed to list R sessions: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def close_session(session_id: str) -> Dict[str, Any]:
    """Close and remove an R session."""
    try:
        session_manager.close_session(session_id)
        return {
            "success": True,
            "message": f"Closed R session {session_id}"
        }
    except Exception as e:
        logger.error(f"Failed to close R session {session_id}: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def execute_in_session(session_id: str, code: str) -> Dict[str, Any]:
    """Execute R code in a session. State persists and output is captured."""
    try:
        result = session_manager.execute_in_session(session_id, code)
        return result
    except Exception as e:
        logger.error(f"Failed to execute R code in session {session_id}: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def list_session_files(session_id: str, path: str = ".") -> Dict[str, Any]:
    """List files in the session's workspace."""
    try:
        files = session_manager.list_files(session_id, path)
        return {
            "success": True,
            "files": files
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def read_session_file(session_id: str, path: str) -> Dict[str, Any]:
    """Read a text file from the session."""
    try:
        content = session_manager.read_file(session_id, path)
        return {
            "success": True,
            "content": content
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def write_session_file(session_id: str, path: str, content: str) -> Dict[str, Any]:
    """Write content to a file in the session."""
    try:
        session_manager.write_file(session_id, path, content)
        return {
            "success": True,
            "message": f"Successfully wrote to {path}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def install_package(session_id: str, package_name: str, source: str = "CRAN") -> Dict[str, Any]:
    """Install an R package dynamically (CRAN or GitHub)."""
    try:
        install_cmd = ""
        if source.upper() == "CRAN":
            install_cmd = f'install.packages("{package_name}", repos="https://cloud.r-project.org")'
        elif source.upper() == "GITHUB":
            install_cmd = f'remotes::install_github("{package_name}", auth_token=Sys.getenv("GITHUB_PAT"))'
        else:
            return {"success": False, "error": "Invalid source. Use CRAN or GitHub."}
            
        result = session_manager.execute_in_session(session_id, install_cmd)
        
        if result["success"]:
             return {"success": True, "message": f"Installed {package_name}", "output": result.get("output", "")}
        else:
             return {"success": False, "error": result.get("error"), "output": result.get("output", "")}
             
    except Exception as e:
        logger.error(f"Failed to install package {package_name} in session {session_id}: {e}")
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    logger.info("Starting OMCP R Sandbox MCP Server...")
    mcp.run()