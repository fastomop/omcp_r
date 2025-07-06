# Implementation Details - OMCP R Sandbox

This document provides a deep dive into the implementation details of the OMCP R Sandbox, including algorithms, data structures, and core functionality.

## Core Implementation Overview

The OMCP R Sandbox is built around three main components:
1. **FastMCP Server** - MCP protocol implementation for R
2. **Sandbox Manager** - Docker container lifecycle management for R
3. **Configuration System** - Environment-based configuration

## FastMCP Server Implementation

- The main server (`src/omcp_r/main.py`) implements the Model Context Protocol using the FastMCP framework.
- Exposes tools for creating, listing, removing sandboxes, and executing R code.

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

## R Sandbox Tools

- `create_sandbox`: Creates new isolated R environments
- `list_sandboxes`: Lists and manages active sandboxes
- `remove_sandbox`: Safely removes sandboxes
- `execute_r_code`: Runs R code in isolated containers

## Sandbox Manager Implementation

- The `SandboxManager` class (`src/omcp_r/sandbox_manager.py`) manages Docker container lifecycle for R sandboxes.
- Handles creation, execution, and cleanup of containers with security restrictions and resource limits.

### Example: Creating a Sandbox

```python
def create_sandbox(self) -> str:
    # ...
    container = self.client.containers.run(
        self.config.docker_image,
        command=["sleep", "infinity"],
        detach=True,
        name=f"omcp-r-sandbox-{sandbox_id}",
        network_mode="none",
        mem_limit="512m",
        cpu_period=100000,
        cpu_quota=50000,
        remove=True,
        user=1000,
        read_only=True,
        cap_drop=["ALL"],
        security_opt=["no-new-privileges"],
        tmpfs={
            "/tmp": "rw,noexec,nosuid,size=100M",
            "/sandbox": "rw,noexec,nosuid,size=500M"
        }
    )
    # ...
```

### Example: Executing R Code

```python
def execute_code(self, sandbox_id: str, code: str):
    # ...
    exec_result = container.exec_run([
        "Rscript", "-e", code
    ])
    # ...
```

## Configuration System

- Loads configuration from environment variables (see [Configuration Guide](configuration.md)).
- Supports timeouts, resource limits, Docker image selection, and logging.

## Security Implementation

- Network isolation, resource limits, user isolation, read-only filesystem, dropped capabilities, and no privilege escalation.
- Input validation and error handling throughout.

## Data Structures

- Sandboxes are tracked by UUID with metadata (`created_at`, `last_used`).
- Tool responses are standardized as dictionaries with `success`, `output`, `error`, and other fields as appropriate.

---

For more details, see the [Architecture Overview](architecture.md) and [Security Model](security.md). 