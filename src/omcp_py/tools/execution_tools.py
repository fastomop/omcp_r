"""
MCP Tools for Python code execution and package management.

Provides tools for running Python code in sandboxes and installing
packages with proper error handling and output processing.
"""

from mcp import Tool, ToolInput, ToolOutput, ToolError
from ..core.sandbox import SandboxManager
from ..utils.config import get_config
import json
from typing import Any, Dict, Optional

class ExecutePythonTool(Tool):
    """MCP tool for executing Python code in sandboxes."""
    
    def __init__(self):
        super().__init__(
            name="execute_python_code",
            description="Execute Python code in a secure sandbox environment",
            input_schema={
                "type": "object",
                "properties": {
                    "sandbox_id": {
                        "type": "string",
                        "description": "The ID of the sandbox to execute code in"
                    },
                    "code": {
                        "type": "string",
                        "description": "Python code to execute"
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Execution timeout in seconds (optional)",
                        "default": 30
                    }
                },
                "required": ["sandbox_id", "code"]
            }
        )
        self.sandbox_manager = SandboxManager(get_config())
    
    async def execute(self, params: ToolInput) -> ToolOutput:
        """Execute Python code in sandbox with output processing."""
        try:
            sandbox_id = params["sandbox_id"]
            code = params["code"]
            timeout = params.get("timeout", 30)
            
            # Validate code input
            if not isinstance(code, str) or not code.strip():
                raise ToolError("Code must be a non-empty string")
            
            # Escape quotes for shell safety
            code = code.replace("'", "'\\''")
            
            # Execute code and process output
            result = self.sandbox_manager.execute_code(sandbox_id, code)
            stdout = result["stdout"].strip()
            stderr = result["stderr"].strip()
            
            # Try to parse JSON output for structured data
            try:
                if stdout and (stdout.startswith("{") or stdout.startswith("[")):
                    stdout = json.loads(stdout)
            except json.JSONDecodeError:
                pass  # Keep as string if not valid JSON
            
            return ToolOutput({
                "success": result["exit_code"] == 0,
                "output": stdout,
                "error": stderr if stderr else None,
                "exit_code": result["exit_code"]
            })
            
        except ToolError as e:
            return ToolOutput({"success": False, "error": str(e)})
        except Exception as e:
            return ToolOutput({"success": False, "error": f"Unexpected error: {str(e)}"})

class InstallPackageTool(Tool):
    """MCP tool for installing Python packages in sandboxes."""
    
    def __init__(self):
        super().__init__(
            name="install_package",
            description="Install a Python package in a sandbox",
            input_schema={
                "type": "object",
                "properties": {
                    "sandbox_id": {
                        "type": "string",
                        "description": "The ID of the sandbox to install the package in"
                    },
                    "package": {
                        "type": "string",
                        "description": "Package name and version (e.g., 'numpy==1.24.0')"
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Installation timeout in seconds (optional)",
                        "default": 60
                    }
                },
                "required": ["sandbox_id", "package"]
            }
        )
        self.sandbox_manager = SandboxManager(get_config())
    
    async def execute(self, params: ToolInput) -> ToolOutput:
        """Install package in sandbox with error handling."""
        try:
            sandbox_id = params["sandbox_id"]
            package = params["package"]
            timeout = params.get("timeout", 60)
            
            # Validate package input
            if not isinstance(package, str) or not package.strip():
                raise ToolError("Package must be a non-empty string")
            
            # Escape quotes for shell safety
            package = package.replace("'", "'\\''")
            
            # Create installation code with proper error handling
            code = f"""
import subprocess
import sys
try:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '{package}'], 
                         timeout={timeout},
                         capture_output=True,
                         text=True)
    print({{"status": "success", "message": "Package installed successfully"}})
except subprocess.TimeoutExpired:
    print({{"status": "error", "message": "Package installation timed out"}})
    sys.exit(1)
except subprocess.CalledProcessError as e:
    print({{"status": "error", "message": f"Package installation failed: {{e.stderr}}"}})
    sys.exit(1)
"""
            # Execute installation and process output
            result = self.sandbox_manager.execute_code(sandbox_id, code)
            stdout = result["stdout"].strip()
            stderr = result["stderr"].strip()
            
            # Try to parse JSON output
            try:
                if stdout:
                    stdout = json.loads(stdout)
            except json.JSONDecodeError:
                pass  # Keep as string if not valid JSON
            
            return ToolOutput({
                "success": result["exit_code"] == 0,
                "output": stdout,
                "error": stderr if stderr else None,
                "exit_code": result["exit_code"]
            })
            
        except ToolError as e:
            return ToolOutput({"success": False, "error": str(e)})
        except Exception as e:
            return ToolOutput({"success": False, "error": f"Unexpected error: {str(e)}"}) 