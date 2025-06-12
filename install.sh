#!/bin/bash

# OMCP Python Sandbox Installation Script

set -e

echo "🚀 Installing OMCP Python Sandbox..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    echo "   cd /path/to/omcp_py"
    exit 1
fi

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.10 or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python version: $python_version"

# Check if Docker is running
if ! docker ps > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running or not accessible"
    echo "   Please start Docker and try again"
    exit 1
fi

echo "✅ Docker is running"

# Install the package in development mode
echo "📦 Installing package in development mode..."
if command -v uv > /dev/null 2>&1; then
    echo "   Using uv package manager..."
    uv pip install -e .
else
    echo "   Using pip package manager..."
    pip install -e .
fi

echo "✅ Package installed successfully"

# Test the installation
echo "🧪 Testing installation..."
if python3 -c "import omcp_py; print('✅ omcp_py package imported successfully')" 2>/dev/null; then
    echo "✅ Package import test passed"
else
    echo "❌ Package import test failed"
    echo "   Try running: pip install -e ."
    exit 1
fi

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "To start the FastMCP server:"
echo "  python server_fastmcp.py"
echo ""
echo "To use MCP Inspector:"
echo "  npx @modelcontextprotocol/inspector python server_fastmcp.py"
echo ""
echo "For more information, see README.md"

try:
    import omcp_py
except ImportError:
    print('Run: pip install -e .')
    exit(1) 