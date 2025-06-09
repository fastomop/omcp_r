"""
MCP Tools for sandbox lifecycle management.

Provides tools for creating, listing, and removing Python sandboxes
with proper error handling and validation.
"""

from mcp import Tool, ToolInput, ToolOutput, ToolError
from ..core.sandbox import SandboxManager
from ..utils.config import get_config
from typing import Any, Dict, Optional
from datetime import datetime

class CreateSandboxTool(Tool):
    """MCP tool for creating new Python sandboxes."""
    
    def __init__(self):
        super().__init__(
            name="create_sandbox",
            description="Create a new Python sandbox environment",
            input_schema={
                "type": "object",
                "properties": {
                    "timeout": {
                        "type": "integer",
                        "description": "Sandbox timeout in seconds (optional)",
                        "default": 300
                    }
                },
                "required": []
            }
        )
        self.sandbox_manager = SandboxManager(get_config())
    
    async def execute(self, params: ToolInput) -> ToolOutput:
        """Create a new sandbox and return its metadata."""
        try:
            # Create sandbox and get info
            sandbox_id = self.sandbox_manager.create_sandbox()
            sandbox_info = next(
                (s for s in self.sandbox_manager.list_sandboxes() if s["id"] == sandbox_id),
                None
            )
            
            if not sandbox_info:
                raise ToolError("Failed to get sandbox information after creation")
            
            return ToolOutput({
                "success": True,
                "sandbox_id": sandbox_id,
                "created_at": sandbox_info["created_at"],
                "last_used": sandbox_info["last_used"]
            })
            
        except ToolError as e:
            return ToolOutput({"success": False, "error": str(e)})
        except Exception as e:
            return ToolOutput({"success": False, "error": f"Unexpected error: {str(e)}"})

class ListSandboxesTool(Tool):
    """MCP tool for listing active sandboxes."""
    
    def __init__(self):
        super().__init__(
            name="list_sandboxes",
            description="List all active Python sandboxes",
            input_schema={
                "type": "object",
                "properties": {
                    "include_inactive": {
                        "type": "boolean",
                        "description": "Include inactive sandboxes (optional)",
                        "default": False
                    }
                },
                "required": []
            }
        )
        self.sandbox_manager = SandboxManager(get_config())
    
    async def execute(self, params: ToolInput) -> ToolOutput:
        """List sandboxes with optional inactive filtering."""
        try:
            include_inactive = params.get("include_inactive", False)
            sandboxes = self.sandbox_manager.list_sandboxes()
            
            # Filter inactive sandboxes unless requested
            if not include_inactive:
                sandboxes = [
                    s for s in sandboxes
                    if (datetime.now() - datetime.fromisoformat(s["last_used"])).total_seconds() < self.sandbox_manager.config.sandbox_timeout
                ]
            
            return ToolOutput({
                "success": True,
                "sandboxes": sandboxes,
                "count": len(sandboxes)
            })
            
        except ToolError as e:
            return ToolOutput({"success": False, "error": str(e)})
        except Exception as e:
            return ToolOutput({"success": False, "error": f"Unexpected error: {str(e)}"})

class RemoveSandboxTool(Tool):
    """MCP tool for removing sandboxes with safety checks."""
    
    def __init__(self):
        super().__init__(
            name="remove_sandbox",
            description="Remove a Python sandbox",
            input_schema={
                "type": "object",
                "properties": {
                    "sandbox_id": {
                        "type": "string",
                        "description": "The ID of the sandbox to remove"
                    },
                    "force": {
                        "type": "boolean",
                        "description": "Force removal even if sandbox is active (optional)",
                        "default": False
                    }
                },
                "required": ["sandbox_id"]
            }
        )
        self.sandbox_manager = SandboxManager(get_config())
    
    async def execute(self, params: ToolInput) -> ToolOutput:
        """Remove sandbox with optional force override."""
        try:
            sandbox_id = params["sandbox_id"]
            force = params.get("force", False)
            
            # Validate sandbox exists
            if sandbox_id not in self.sandbox_manager.sandboxes:
                raise ToolError(f"Sandbox {sandbox_id} not found")
            
            # Check if sandbox is active (unless force is True)
            if not force:
                sandbox = self.sandbox_manager.sandboxes[sandbox_id]
                if (datetime.now() - sandbox["last_used"]).total_seconds() < self.sandbox_manager.config.sandbox_timeout:
                    raise ToolError(f"Sandbox {sandbox_id} is still active. Use force=True to remove it.")
            
            # Remove the sandbox
            self.sandbox_manager.remove_sandbox(sandbox_id)
            
            return ToolOutput({
                "success": True,
                "message": f"Sandbox {sandbox_id} removed successfully"
            })
            
        except ToolError as e:
            return ToolOutput({"success": False, "error": str(e)})
        except Exception as e:
            return ToolOutput({"success": False, "error": f"Unexpected error: {str(e)}"}) 