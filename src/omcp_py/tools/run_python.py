from mcp import Tool, ToolInput, ToolOutput
from ..utils.omcp_py import execute_python_code   # Updated import path

class RunPythonTool(Tool):
    def __init__(self):
        super().__init__(
            name="run_python_code",
            description="Run Python code in a sandbox environment",
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
    
    async def execute(self, params: ToolInput) -> ToolOutput:
        code = params.get("code")
        result = execute_python_code(code)
        return ToolOutput({
            "result": result.get("return_value"),
            "output": result.get("output"),
            "error": result.get("error")
        })
