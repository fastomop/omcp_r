from mcp import Tool, ToolInput, ToolOutput
from ..core.sandbox import SandboxManager
from ..utils.config import get_config

class ExecutePythonTool(Tool):
    """Tool for executing Python code in a sandbox."""
    
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
                    }
                },
                "required": ["sandbox_id", "code"]
            }
        )
        self.sandbox_manager = SandboxManager(get_config())
    
    async def execute(self, params: ToolInput) -> ToolOutput:
        """Execute the Python code in the specified sandbox."""
        sandbox_id = params["sandbox_id"]
        code = params["code"]
        
        try:
            result = self.sandbox_manager.execute_code(sandbox_id, code)
            return ToolOutput({
                "success": True,
                "output": result["stdout"],
                "error": result["stderr"],
                "exit_code": result["exit_code"]
            })
        except Exception as e:
            return ToolOutput({
                "success": False,
                "error": str(e)
            })
