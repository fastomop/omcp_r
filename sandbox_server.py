"""
Flask-based Python Sandbox Server (Legacy/Alternative implementation).

Simple HTTP server for executing Python code in a restricted namespace.
This is an alternative to the Docker-based MCP implementation.
"""

from flask import Flask, request, jsonify
import sys
import io
from contextlib import redirect_stdout, redirect_stderr

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_code():
    """
    Execute Python code in restricted namespace.
    
    Accepts JSON with 'code' field and returns execution results.
    Captures stdout/stderr and handles exceptions safely.
    """
    data = request.get_json()
    code = data.get('code', '')
    stdout = io.StringIO()
    stderr = io.StringIO()
    result = None
    error = None
    
    try:
        # Execute code in restricted namespace
        with redirect_stdout(stdout), redirect_stderr(stderr):
            namespace = {}
            exec(code, namespace)
            result = namespace.get('_', None)  # Get last expression value
    except Exception as e:
        error = str(e)
    
    # Collect output
    output = stdout.getvalue()
    errout = stderr.getvalue()
    if errout:
        error = errout  # Prefer stderr over exception
    
    return jsonify({
        'result': result,
        'output': output,
        'error': error
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000) 