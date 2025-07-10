# OMCP R Sandbox Server

A secure, MCP-compliant R code execution environment with Docker-based sandboxing. This server implements the Model Context Protocol (MCP) specification for safe, isolated R code execution with enterprise-grade security features.

## Features

- **MCP-Compliant Tools**:
  - `create_sandbox`: Create isolated R environments
  - `list_sandboxes`: List active sandboxes with status
  - `remove_sandbox`: Safely remove sandboxes
  - `execute_r_code`: Run R code in sandbox

- **Security Features**:
  - Docker-based isolation with enhanced security options
  - User isolation (non-root user)
  - Read-only filesystem with temporary writable areas
  - Dropped Linux capabilities (cap_drop=["ALL"])
  - No privilege escalation (no-new-privileges)
  - Resource limits (CPU, memory, execution timeouts)
  - Network isolation (network_mode="none")
  - Input validation and sanitisation
  - Auto-cleanup of inactive sandboxes

- **MCP Integration**:
  - Standard MCP tool interface
  - Proper error handling with timeout support
  - Structured logging
  - Type-safe responses
  - JSON output support

## Prerequisites

- **Python 3.10+** (for MCP server)
- **Docker** (for sandbox isolation)
- **uv** (for dependency management)

## Installation

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/Z0shua/omcp_r.git
   cd omcp_r
   ```

2. **Install Dependencies** (using uv):
   ```sh
   uv pip install -e .
   ```

3. **Environment Setup** (optional):
   Create a `.env` file or edit `sample.env`:
   ```env
   SANDBOX_TIMEOUT=300
   MAX_SANDBOXES=10
   DOCKER_IMAGE=rocker/r-ver:latest
   LOG_LEVEL=INFO
   ```

## Usage

### Starting the Server

```sh
python src/omcp_r/main.py
```

### Using Docker Compose

You can also run the server with Docker Compose:

```sh
docker-compose up --build
```

This will use the `rocker/r-ver:latest` image for R code execution inside sandboxes.

### Tool Examples

1. **Create a Sandbox**:
   ```python
   result = await mcp.create_sandbox()
   sandbox_id = result["sandbox_id"]
   ```

2. **Execute R Code**:
   ```python
   result = await mcp.execute_r_code(
       sandbox_id=sandbox_id,
       code="cat(mean(c(1,2,3,4,5)))",
       timeout=30
   )
   print(result["output"])
   ```

3. **List Sandboxes**:
   ```python
   sandboxes = await mcp.list_sandboxes(include_inactive=False)
   ```

4. **Remove a Sandbox**:
   ```python
   await mcp.remove_sandbox(
       sandbox_id=sandbox_id,
       force=False
   )
   ```

## Security

- Each sandbox runs in a Docker container with strict isolation.
- Non-root user, read-only filesystem, dropped capabilities, and no network access.
- Resource limits and automatic cleanup of inactive sandboxes.
- Input validation and error handling throughout.

## Project Structure

```
omcp_r/
├── src/
│   └── omcp_r/
│       ├── main.py              # FastMCP server for R sandbox
│       ├── sandbox_manager.py   # Docker-based R sandbox manager
│       └── config.py            # Configuration loader
├── docs/                       # Documentation
├── Dockerfile                  # Docker image for the R sandbox
├── docker-compose.yml          # Docker Compose configuration
├── sample.env                  # Example environment configuration
├── pyproject.toml              # Project metadata and dependencies
└── README.md                   # Project overview and documentation index
```

## License
MIT
