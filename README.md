# OMCP Python Sandbox Server

A secure, MCP-compliant Python code execution environment with Docker-based sandboxing. This server implements the Model Context Protocol (MCP) specification for safe, isolated Python code execution with enterprise-grade security features.

## Features

- **MCP-Compliant Tools**:
  - `create_sandbox`: Create isolated Python environments
  - `list_sandboxes`: List active sandboxes with status
  - `remove_sandbox`: Safely remove sandboxes
  - `execute_python_code`: Run Python code in sandbox
  - `install_package`: Install Python packages in sandbox

- **Enterprise Security Features**:
  - Docker-based isolation with enhanced security options
  - User isolation (sandboxuser instead of root)
  - Read-only filesystem with temporary writable areas
  - Dropped Linux capabilities (cap_drop=["ALL"])
  - No privilege escalation (no-new-privileges)
  - Command injection protection (shlex.quote)
  - Resource limits (CPU, memory, execution timeouts)
  - Network isolation (network_mode="none")
  - Input validation and sanitization
  - Auto-cleanup of inactive sandboxes

- **MCP Integration**:
  - Standard MCP tool interface
  - Proper error handling with timeout support
  - Structured logging
  - Type-safe responses
  - JSON output support
  - FastMCP implementation available

## Prerequisites

- **Python 3.10+** (for MCP server)
- **Docker** (for sandbox isolation)
- **uv** (for dependency management)

## Installation

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/fastomop/omcp_py.git
   cd omcp_py
   ```

2. **Install Dependencies**:
   ```sh
   uv pip install -r requirements.txt
   ```

3. **Environment Setup** (optional):
   Create a `.env` file:
   ```env
   SANDBOX_TIMEOUT=300
   MAX_SANDBOXES=10
   DOCKER_IMAGE=python:3.11-slim
   DEBUG=false
   LOG_LEVEL=INFO
   ```

## Usage

### Starting the Server

**Standard MCP Server:**
```sh
python server.py
```

**FastMCP Server (Enhanced):**
```sh
python server_fastmcp.py
```

The server will start and expose the following MCP tools:

### Tool Examples

1. **Create a Sandbox**:
   ```python
   result = await mcp.create_sandbox()
   sandbox_id = result["sandbox_id"]
   ```

2. **Install a Package**:
   ```python
   await mcp.install_package(
       sandbox_id=sandbox_id,
       package="numpy==1.24.0",
       timeout=60
   )
   ```

3. **Execute Code**:
   ```python
   result = await mcp.execute_python_code(
       sandbox_id=sandbox_id,
       code="""
       import numpy as np
       arr = np.array([1, 2, 3])
       print({"sum": arr.sum()})
       """,
       timeout=30
   )
   ```

4. **List Sandboxes**:
   ```python
   sandboxes = await mcp.list_sandboxes(include_inactive=False)
   ```

5. **Remove a Sandbox**:
   ```python
   await mcp.remove_sandbox(
       sandbox_id=sandbox_id,
       force=False
   )
   ```

### Tool Specifications

#### `create_sandbox`
- **Input**: Optional timeout (default: 300s)
- **Output**: `{sandbox_id, created_at, last_used}`

#### `execute_python_code`
- **Input**: 
  - `sandbox_id` (required)
  - `code` (required)
  - `timeout` (optional, default: 30s)
- **Output**: `{success, output, error, exit_code}`

#### `install_package`
- **Input**:
  - `sandbox_id` (required)
  - `package` (required, e.g., "numpy==1.24.0")
  - `timeout` (optional, default: 60s)
- **Output**: `{success, output, error, exit_code}`

#### `list_sandboxes`
- **Input**: `include_inactive` (optional, default: false)
- **Output**: `{sandboxes: [...], count: N}`

#### `remove_sandbox`
- **Input**:
  - `sandbox_id` (required)
  - `force` (optional, default: false)
- **Output**: `{success, message}`

## Security

### Container Security
Each sandbox runs in a Docker container with:
- **User isolation**: Runs as `sandboxuser` instead of root
- **Read-only filesystem**: Prevents file system modifications
- **Dropped capabilities**: Removes all Linux capabilities
- **No privilege escalation**: Prevents privilege escalation attacks
- **Temporary filesystems**: Secure tmpfs mounts for `/tmp` and `/sandbox`
- **No network access**: Complete network isolation
- **Resource limits**: CPU, memory, and execution time limits

### Code Execution Security
- **Command injection protection**: Uses `shlex.quote` for proper escaping
- **List-form commands**: Prevents shell injection attacks
- **Timeout handling**: Configurable execution timeouts
- **Input validation**: Comprehensive input sanitization
- **Error isolation**: Errors don't affect other sandboxes

### Resource Management
- **Maximum sandboxes limit**: Prevents resource exhaustion
- **Timeout-based cleanup**: Automatic removal of inactive sandboxes
- **Force removal option**: Manual cleanup when needed
- **Memory limits**: 512MB per sandbox
- **CPU limits**: Restricted CPU usage

## Implementation Options

### Standard MCP Server (`server.py`)
- Full MCP specification compliance
- Explicit tool schemas
- Comprehensive error handling
- Production-ready implementation

### FastMCP Server (`server_fastmcp.py`)
- Simplified syntax with decorators
- Enhanced security features
- Better timeout handling
- Faster development workflow

## Development

### Project Structure
```
omcp_py/
├── src/
│   └── omcp_py/
│       ├── core/
│       │   └── sandbox.py      # Enhanced sandbox management
│       ├── tools/
│       │   ├── execution_tools.py
│       │   └── sandbox_tools.py
│       └── utils/
│           └── config.py       # Configuration
├── server.py                   # Standard MCP server
├── server_fastmcp.py           # FastMCP server (enhanced)
├── Dockerfile                  # UV-based Docker build
├── requirements.txt
└── pyproject.toml
```

### Testing
```sh
uv pip install -r requirements.txt[dev]
pytest
```

### Logging
- Logs to stderr (MCP convention)
- Configurable levels (INFO, DEBUG, etc.)
- Structured format with security events

## Recent Updates

### v0.2.0 - Enhanced Security & FastMCP
- **Enhanced Docker Security**: User isolation, read-only filesystem, dropped capabilities
- **FastMCP Implementation**: Alternative server with simplified syntax
- **Command Injection Protection**: shlex.quote for proper command escaping
- **Timeout Handling**: Specific timeout error handling
- **UV Package Manager**: Faster package management in Docker
- **Improved Error Handling**: Better timeout and security error handling

### v0.1.0 - Initial Release
- Basic MCP server implementation
- Docker-based sandboxing
- Core tool functionality
- Resource management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License
MIT