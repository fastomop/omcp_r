"""
FastMCP R Sandbox Server

Implements a Model Context Protocol (MCP) server for secure, Docker-based R code execution.
Mirrors the omcp_py architecture for consistency.
"""

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
async def list_sessions(include_inactive: bool = False) -> Dict[str, Any]:
    try:
        sessions = session_manager.list_sessions()
        if not include_inactive:
            from datetime import datetime
            sessions = [
                s for s in sessions
                if (datetime.now() - datetime.fromisoformat(s["last_used"])).total_seconds() < config.sandbox_timeout
            ]
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
    try:
        if session_id not in [s["id"] for s in session_manager.list_sessions()]:
            return {
                "success": False,
                "error": "Session not found"
            }
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
    try:
        result = session_manager.execute_in_session(session_id, code)
        return result
    except Exception as e:
        logger.error(f"Failed to execute R code in session {session_id}: {e}")
        return {
            "success": False,
            "error": str(e)
        } 