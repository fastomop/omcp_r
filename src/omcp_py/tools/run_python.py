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
                    "python_code": {
                        "type": "string", 
                        "description": "Python code to execute"
                    }
                },
                "required": ["python_code"]
            }
        )
    
    async def execute(self, params: ToolInput) -> ToolOutput:
        # Retrieve the code from the key 'python_code'
        code = params.get("python_code")
        result = execute_python_code(code)
        return ToolOutput({
            "result": result.get("return_value"),
            "output": result.get("output"),
            "error": result.get("error")
        })
