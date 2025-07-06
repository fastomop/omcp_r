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
from omcp_r.sandbox_manager import SandboxManager
from omcp_r.config import get_config

config = get_config()

logging.basicConfig(
    level=config.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)

logger = logging.getLogger(__name__)

mcp = FastMCP("R Sandbox")

sandbox_manager = SandboxManager(config)

@mcp.tool()
async def create_sandbox(timeout: Optional[int] = 300) -> Dict[str, Any]:
    try:
        sandbox_id = sandbox_manager.create_sandbox()
        sandbox_info = next(
            (s for s in sandbox_manager.list_sandboxes() if s["id"] == sandbox_id),
            None
        )
        if not sandbox_info:
            raise Exception("Failed to get sandbox information after creation")
        return {
            "success": True,
            "sandbox_id": sandbox_id,
            "created_at": sandbox_info["created_at"],
            "last_used": sandbox_info["last_used"]
        }
    except Exception as e:
        logger.error(f"Failed to create R sandbox: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def list_sandboxes(include_inactive: bool = False) -> Dict[str, Any]:
    try:
        sandboxes = sandbox_manager.list_sandboxes()
        if not include_inactive:
            from datetime import datetime
            sandboxes = [
                s for s in sandboxes
                if (datetime.now() - datetime.fromisoformat(s["last_used"])).total_seconds() < config.sandbox_timeout
            ]
        return {
            "success": True,
            "sandboxes": sandboxes,
            "count": len(sandboxes)
        }
    except Exception as e:
        logger.error(f"Failed to list R sandboxes: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def remove_sandbox(sandbox_id: str, force: bool = False) -> Dict[str, Any]:
    try:
        if sandbox_id not in [s["id"] for s in sandbox_manager.list_sandboxes()]:
            return {
                "success": False,
                "error": "Sandbox not found"
            }
        sandbox_manager.remove_sandbox(sandbox_id)
        return {
            "success": True,
            "message": f"Removed R sandbox {sandbox_id}"
        }
    except Exception as e:
        logger.error(f"Failed to remove R sandbox {sandbox_id}: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def execute_r_code(sandbox_id: str, code: str, timeout: Optional[int] = 30) -> Dict[str, Any]:
    try:
        exec_result = sandbox_manager.execute_code(sandbox_id, code)
        output = exec_result.output.decode() if exec_result.output else ""
        exit_code = exec_result.exit_code
        return {
            "success": exit_code == 0,
            "output": output,
            "exit_code": exit_code
        }
    except Exception as e:
        logger.error(f"Failed to execute R code in sandbox {sandbox_id}: {e}")
        return {
            "success": False,
            "error": str(e)
        } 