# Implementation Details - OMCP R Sandbox

This document provides a deep dive into the implementation details of the OMCP R Sandbox, including architecture, key components, and core functionality.

## Core Implementation Overview

The OMCP R Sandbox is built around three main components:
1. **FastMCP Server** - MCP protocol implementation for R
2. **Session Manager** - Docker container lifecycle management with Rserve
3. **Configuration System** - Environment-based configuration

## FastMCP Server Implementation

The main server (`src/omcp_r/main.py`) implements the Model Context Protocol using the FastMCP framework. It exposes tools for creating, listing, closing sessions, and executing R code.

### Running the Server

```bash
# Direct execution
python src/omcp_r/main.py

# Or using uv
uv run python src/omcp_r/main.py
```

## Tool Implementation Pattern

All MCP tools follow a consistent implementation pattern:

```python
@mcp.tool()
async def tool_name(param1: str, param2: int = 10) -> Dict[str, Any]:
    """
    Tool description and documentation.
    """
    try:
        # Tool implementation
        result = do_something(param1, param2)
        return {"success": True, "result": result}
    except Exception as e:
        logger.error(f"Tool failed: {e}")
        return {"success": False, "error": str(e)}
```

## R Session Tools

- `create_session`: Creates a new Docker container running Rserve
- `list_sessions`: Lists active sessions with metadata
- `close_session`: Stops and removes a session container
- `execute_in_session`: Executes R code via pyRserve connection

## Session Manager Implementation

The `SessionManager` class (`src/omcp_r/sandbox_manager.py`) manages Docker container lifecycle for R sessions with Rserve.

### Key Features

- **Persistent Sessions**: Each session is a Docker container running Rserve
- **State Preservation**: R environment persists across multiple `execute_in_session` calls
- **Automatic Cleanup**: Inactive sessions are cleaned up based on timeout
- **Resource Limits**: Memory/CPU limits enforced per container

### Example: Creating a Session

```python
def create_session(self) -> str:
    session_id = str(uuid.uuid4())
    env_vars = {
        "DB_HOST": self.config.db_host,
        "DB_PORT": str(self.config.db_port),
        # ... other env vars
    }
    container = self.client.containers.run(
        self.config.docker_image,
        detach=True,
        name=f"omcp-r-session-{session_id}",
        mem_limit="512m",
        cpu_period=100000,
        cpu_quota=50000,
        # ... security options
        ports={'6311/tcp': None}  # Dynamic port mapping for Rserve
    )
    # Get mapped port
    container.reload()
    host_port = container.attrs['NetworkSettings']['Ports']['6311/tcp'][0]['HostPort']
    # ... store session info
    return session_id
```

### Example: Executing R Code

```python
def execute_in_session(self, session_id: str, code: str) -> dict:
    session = self.sessions[session_id]
    host = "localhost"
    port = int(session["host_port"])
    conn = pyRserve.connect(host=host, port=port)
    result = conn.eval(code)
    conn.close()
    return {"success": True, "result": result}
```

## OMOP/DARWIN Support

The sandbox is optimized for OHDSI/DARWIN analytics:
- **Java 17**: Pre-installed for `DatabaseConnector`, `FeatureExtraction`, etc.
- **R Packages**: `CDMConnector`, `DatabaseConnector`, `SqlRender`, `omopgenerics` pre-installed.
- **File Management**: Tools to upload cohort definitions and download results.
- **Output Capturing**: `stdout` and `stderr` are captured and returned with the result, enabling debugging of `print()` statements and OHDSI logs.
- **Persistent Workspaces**: Sessions can mount a host directory (`WORKSPACE_ROOT`) to `/sandbox`, ensuring files persist after the session closes.
- **Auto-Proxying**: Connecting to `localhost` database automatically maps to `host.docker.internal` for seamless local testing.

## Configuration System

Configuration is loaded from environment variables at startup. See `src/omcp_r/config.py`:

```python
class RConfig:
    def __init__(self):
        self.sandbox_timeout = int(os.getenv("SANDBOX_TIMEOUT", 300))
        self.max_sandboxes = int(os.getenv("MAX_SANDBOXES", 10))
        self.docker_image = os.getenv("DOCKER_IMAGE", "omcp-r-sandbox:latest")
        self.log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        # Database connection defaults
        self.db_host = os.getenv("DB_HOST", "")
        self.db_port = int(os.getenv("DB_PORT", 5432))
        self.db_user = os.getenv("DB_USER", "")
        self.db_password = os.getenv("DB_PASSWORD", "")
        self.db_name = os.getenv("DB_NAME", "")
```

## Security Implementation

- **Resource Limits**: Memory and CPU limits per container
- **User Isolation**: Containers run as non-root user (UID 1000)
- **Read-only Filesystem**: Root FS is read-only with limited writable tmpfs mounts
- **Dropped Capabilities**: All Linux capabilities are dropped
- **No Privilege Escalation**: Containers started with `no-new-privileges`
- **Input Validation**: All user input validated before execution
- **Comprehensive Logging**: All actions logged for audit

## Data Structures

- Sessions are tracked by UUID with metadata (`created_at`, `last_used`, `host_port`)
- Tool responses are standardized as dictionaries with `success`, `result`/`output`, `error` fields

---

For more details, see the [Architecture Overview](architecture.md) and [Security Model](security.md).