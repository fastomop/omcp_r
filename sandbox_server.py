from flask import Flask, request, jsonify
import sys
import io
from contextlib import redirect_stdout, redirect_stderr

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data.get('code', '')
    stdout = io.StringIO()
    stderr = io.StringIO()
    result = None
    error = None
    try:
        with redirect_stdout(stdout), redirect_stderr(stderr):
            # Restricted namespace
            namespace = {}
            exec(code, namespace)
            result = namespace.get('_', None)
    except Exception as e:
        error = str(e)
    output = stdout.getvalue()
    errout = stderr.getvalue()
    if errout:
        error = errout
    return jsonify({
        'result': result,
        'output': output,
        'error': error
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000) 