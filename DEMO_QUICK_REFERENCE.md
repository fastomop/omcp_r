# 🚀 OMCP Python Sandbox - Demo Quick Reference

## ⚡ Quick Start Commands

```bash
# 1. Navigate to project
cd /home/zoshua/dev/omcp_py
source .venv/bin/activate

# 2. Start FastMCP server
uv run server_fastmcp.py

# 3. Launch MCP Inspector (new terminal)
npx @modelcontextprotocol/inspector uv run server_fastmcp.py

# 4. Open web UI
# http://127.0.0.1:6274

# 5. Run showcase demo (optional)
python showcase_demo.py
```

## 🌐 MCP Inspector URL
**http://127.0.0.1:6274**

## 🔧 Available Tools in MCP Inspector

1. **create_sandbox** - Create new isolated Python environment
2. **list_sandboxes** - List all active sandboxes  
3. **execute_python_code** - Run Python code in sandbox
4. **install_package** - Install Python packages in sandbox
5. **remove_sandbox** - Remove sandbox containers

## 🧪 Quick Test Sequence

1. **Create Sandbox**: Use `create_sandbox` tool
2. **Execute Code**: Use `execute_python_code` with `print("Hello!")`
3. **Install Package**: Use `install_package` with `requests`
4. **List Sandboxes**: Use `list_sandboxes` to see your sandbox
5. **Remove Sandbox**: Use `remove_sandbox` with force=true

## 🔒 Security Features to Mention

- Docker isolation
- User isolation (sandboxuser)
- Read-only filesystem
- Dropped capabilities
- No privilege escalation
- Command injection protection
- Resource limits
- Network isolation
- Timeout controls
- Auto-cleanup

## 📊 Architecture

```
Agent → FastMCP Server → Docker Containers → Flask Sandbox
```

## 🚨 Troubleshooting

- **Port in use**: `ss -tlnp | grep 6274`
- **Docker issues**: `sudo docker ps`
- **Server not starting**: Check logs in terminal
- **Inspector not loading**: Restart with `npx` command

## Flow

1. Show automated showcase (`python showcase_demo.py`)
2. Open MCP Inspector (http://127.0.0.1:6274)
3. Demonstrate tool testing
4. Highlight security features
5. Show architecture diagram
6. Test error handling

---
