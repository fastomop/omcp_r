# 🚀 OMCP Python Sandbox Demo Guide

This guide provides step-by-step instructions for demonstrating the OMCP Python Sandbox system to your supervisor or stakeholders.

## 📋 Prerequisites

- Python 3.10+ with `uv` package manager
- Docker running with sudo access
- Node.js and npm (for MCP Inspector)
- Web browser

## 🎯 Demo Options

### Option 1: Automated Showcase (Recommended)
Run the automated showcase script that demonstrates all features:

```bash
cd /home/zoshua/dev/omcp_py
source .venv/bin/activate
python showcase_demo.py
```

### Option 2: Interactive MCP Inspector Demo
Use the web-based MCP Inspector for hands-on tool testing:

```bash
cd /home/zoshua/dev/omcp_py
source .venv/bin/activate

# Terminal 1: Start the FastMCP server
uv run server_fastmcp.py

# Terminal 2: Launch MCP Inspector
npx @modelcontextprotocol/inspector uv run server_fastmcp.py

# Open browser to: http://127.0.0.1:6274
```

### Option 3: Combined Demo (Best for Presentations)
Run both the showcase and open the MCP Inspector for interactive testing.

## 🔧 Step-by-Step Demo Instructions

### Step 1: Environment Setup
```bash
cd /home/zoshua/dev/omcp_py
source .venv/bin/activate
```

### Step 2: Verify Prerequisites
```bash
# Check Docker
sudo docker ps

# Check Python environment
which python
python --version
```

### Step 3: Start the FastMCP Server
```bash
uv run server_fastmcp.py
```

### Step 4: Launch MCP Inspector
In a new terminal:
```bash
cd /home/zoshua/dev/omcp_py
source .venv/bin/activate
npx @modelcontextprotocol/inspector uv run server_fastmcp.py
```

### Step 5: Open Web Interface
Open your browser and go to: **http://127.0.0.1:6274**

### Step 6: Run Automated Showcase
In another terminal:
```bash
cd /home/zoshua/dev/omcp_py
source .venv/bin/activate
python showcase_demo.py
```

## 🌐 MCP Inspector Features

The MCP Inspector provides a web-based interface with:

- **🔧 Interactive Tool Testing**: Test all MCP tools in real-time
- **📊 Request/Response Inspection**: See JSON-RPC messages
- **🐍 Code Execution Testing**: Run Python code in sandboxes
- **📦 Package Installation Testing**: Install packages in sandboxes
- **📝 Sandbox Management**: Create, list, and remove sandboxes
- **🔍 Error Debugging**: View detailed error messages
- **📈 Performance Monitoring**: Track execution times
- **💾 Session Persistence**: Save and load test scenarios

## 🧪 Demo Test Cases

### Test Case 1: Create a Sandbox
1. In MCP Inspector, select `create_sandbox` tool
2. Set timeout to 300 seconds
3. Click "Call Tool"
4. Verify sandbox creation success

### Test Case 2: Execute Python Code
1. Use the sandbox ID from Test Case 1
2. Select `execute_python_code` tool
3. Enter code: `print("Hello from sandbox!")`
4. Click "Call Tool"
5. Verify output

### Test Case 3: Install Package
1. Use the same sandbox ID
2. Select `install_package` tool
3. Enter package: `requests`
4. Click "Call Tool"
5. Verify installation success

### Test Case 4: List Sandboxes
1. Select `list_sandboxes` tool
2. Click "Call Tool"
3. Verify your sandbox appears in the list

### Test Case 5: Remove Sandbox
1. Select `remove_sandbox` tool
2. Enter the sandbox ID
3. Set force to true
4. Click "Call Tool"
5. Verify removal success

## 🔒 Security Features to Highlight

- **🐳 Docker-based isolation**: Each sandbox runs in a separate container
- **👤 User isolation**: Containers run as 'sandboxuser' (non-root)
- **🔒 Read-only filesystem**: Prevents file system modifications
- **🛡️ Dropped Linux capabilities**: Removes dangerous privileges
- **🚫 No privilege escalation**: Containers cannot gain root access
- **🔐 Command injection protection**: Uses proper escaping
- **⚡ Resource limits**: CPU and memory restrictions
- **🌐 Network isolation**: Containers have no network access
- **⏰ Timeout controls**: Automatic cleanup
- **🧹 Auto-cleanup**: Inactive sandboxes are removed

## 📊 System Architecture

```
🖥️  MCP Client (Agent)
     ↓ (JSON-RPC over stdio)
🚀 FastMCP Server (server_fastmcp.py)
     ↓ (Docker API)
🐳 Docker Containers (Python Sandboxes)
     ↓ (Flask HTTP)
🔧 Sandbox Server (sandbox_server.py)
```

## 🎯 Key Talking Points

1. **Security First**: Emphasize the comprehensive security measures
2. **Production Ready**: Show the robust error handling and logging
3. **MCP Standard**: Highlight compliance with Model Context Protocol
4. **Scalable**: Demonstrate the Docker-based architecture
5. **Interactive**: Show the MCP Inspector for easy testing
6. **Maintainable**: Point out the clean code structure

## 🚨 Troubleshooting

### MCP Inspector Not Starting
```bash
# Check if Node.js is installed
node --version

# Install if needed
sudo apt install nodejs npm

# Try running inspector again
npx @modelcontextprotocol/inspector uv run server_fastmcp.py
```

### Docker Permission Issues
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Log out and back in, or run:
newgrp docker
```

### Port Already in Use
```bash
# Check what's using port 6274
ss -tlnp | grep 6274

# Kill the process if needed
sudo kill -9 <PID>
```

## 📹 Screen Recording Tips

1. **Start with showcase script**: Shows all features quickly
2. **Switch to MCP Inspector**: Demonstrate interactive testing
3. **Show security features**: Highlight the security measures
4. **Test error handling**: Show what happens with invalid inputs
5. **Demonstrate cleanup**: Show sandbox removal and cleanup

## 🎉 Success Criteria

The demo is successful when you can demonstrate:

- ✅ FastMCP server starts without errors
- ✅ MCP Inspector web UI loads and connects
- ✅ Sandbox creation works
- ✅ Python code execution works
- ✅ Package installation works
- ✅ Sandbox management (list/remove) works
- ✅ Security features are explained
- ✅ Architecture is understood

## 📞 Support

If you encounter issues during the demo:

1. Check the terminal output for error messages
2. Verify Docker is running: `sudo docker ps`
3. Check server logs for detailed information
4. Restart the server if needed: `pkill -f server_fastmcp.py`

---

**Ready to demonstrate! 🚀** 