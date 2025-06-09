import sys
import io
from contextlib import redirect_stdout, redirect_stderr
from mcp.shared import ServerConfig

def execute_python_code(code: str) -> dict:
    """Execute Python code in a controlled environment and return the result."""
    # Capture stdout and stderr
    stdout = io.StringIO()
    stderr = io.StringIO()
    result = {}
    
    try:
        # Execute in a controlled environment
        with redirect_stdout(stdout), redirect_stderr(stderr):
            # Create a namespace for execution
            namespace = {}
            
            # Execute the code
            exec(code, namespace)
            
            # Get the last expression's value if available
            result["return_value"] = namespace.get("_", None)
    except Exception as e:
        result["error"] = str(e)
    
    result["output"] = stdout.getvalue()
    if stderr.getvalue():
        result["error"] = stderr.getvalue()
    
    return result
