import logging
import sys
from typing import Optional, Dict, Any
from mcp.server.fastmcp import FastMCP
from omcp_r.sandbox_manager import SessionManager
from omcp_r.config import get_config
from omcp_r.errors import SandboxError, error_payload

config = get_config()

logging.basicConfig(
    level=config.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)

logger = logging.getLogger(__name__)

mcp = FastMCP("R Sandbox")

session_manager = SessionManager(config)


def success_payload(**kwargs: Any) -> Dict[str, Any]:
    return {"success": True, **kwargs}


def map_error(e: Exception, default_code: str, default_message: str) -> Dict[str, Any]:
    if isinstance(e, SandboxError):
        return error_payload(
            e.code,
            e.message,
            retryable=e.retryable,
            details=e.details,
        )
    logger.exception(default_message)
    return error_payload(default_code, default_message, retryable=True, details={"reason": str(e)})

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
            raise SandboxError("session_create_failed", "Failed to get session information after creation")
        return success_payload(
            session_id=session_id,
            created_at=session_info["created_at"],
            last_used=session_info["last_used"],
            host_port=session_info["host_port"],
        )
    except Exception as e:
        return map_error(e, "session_create_failed", "Failed to create R session")

@mcp.tool()
async def list_sessions() -> Dict[str, Any]:
    """List all active R sessions."""
    try:
        sessions = session_manager.list_sessions()
        return success_payload(
            sessions=sessions,
            count=len(sessions),
        )
    except Exception as e:
        return map_error(e, "list_sessions_failed", "Failed to list sessions")

@mcp.tool()
async def close_session(session_id: str) -> Dict[str, Any]:
    """Close and remove an R session."""
    try:
        session_manager.close_session(session_id)
        return success_payload(message=f"Closed R session {session_id}")
    except Exception as e:
        return map_error(e, "session_close_failed", f"Failed to close session {session_id}")

@mcp.tool()
async def execute_in_session(
    session_id: str,
    code: str,
    limits: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Execute R code in a session. State persists and output is captured."""
    try:
        result = session_manager.execute_in_session(session_id, code, limits_payload=limits)
        return result
    except Exception as e:
        return map_error(e, "execution_failed", f"Failed to execute code in session {session_id}")

@mcp.tool()
async def list_session_files(session_id: str, path: str = ".") -> Dict[str, Any]:
    """List files in the session's workspace."""
    try:
        files = session_manager.list_files(session_id, path)
        return success_payload(files=files)
    except Exception as e:
        return map_error(e, "list_files_failed", f"Failed to list files for {session_id}")

@mcp.tool()
async def read_session_file(session_id: str, path: str) -> Dict[str, Any]:
    """Read a text file from the session."""
    try:
        content = session_manager.read_file(session_id, path)
        return success_payload(content=content)
    except Exception as e:
        return map_error(e, "read_file_failed", f"Failed to read file from {session_id}")

@mcp.tool()
async def write_session_file(session_id: str, path: str, content: str) -> Dict[str, Any]:
    """Write content to a file in the session."""
    try:
        session_manager.write_file(session_id, path, content)
        return success_payload(message=f"Successfully wrote to {path}")
    except Exception as e:
        return map_error(e, "write_file_failed", f"Failed to write file for {session_id}")

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
            return error_payload("invalid_source", "Invalid source. Use CRAN or GitHub.")

        result = session_manager.execute_in_session(session_id, install_cmd)

        if result["success"]:
            return success_payload(
                message=f"Installed {package_name}",
                output=result.get("output", ""),
                meta=result.get("meta", {}),
            )
        return result

    except Exception as e:
        return map_error(
            e,
            "install_package_failed",
            f"Failed to install package {package_name} in session {session_id}",
        )

if __name__ == "__main__":
    logger.info("Starting OMCP R Sandbox MCP Server...")
    mcp.run()
