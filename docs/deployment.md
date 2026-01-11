# Deployment Guide - OMCP R Sandbox

This document provides instructions for deploying the OMCP R Sandbox in development and production-like environments.

## Prerequisites

- **Docker**: Engine version 20.10+
- **Docker Compose**: V2 recommended
- **Python 3.10+**: Required only if running the server outside Docker.

## Deployment Model

The project uses a **multi-service model** defined in `docker-compose.yml`:

1.  **`omcp-r-sandbox-builder`**: A helper service that builds the specialized R sandbox image (`omcp-r-sandbox:latest`) containing Java and OHDSI tools.
2.  **`omcp-r-server`**: The Python MCP server that manages the R sessions.

## Quick Start

### 1. Build the Specialized Image
The R sandbox image contains many large dependencies (Java, Tidyverse). It must be built locally or pulled from a registry.
```bash
docker-compose build
```

### 2. Configure Environment
Create a `.env` file from `sample.env`:
```bash
cp sample.env .env
# Edit .env with your database credentials
```

### 3. Start the Environment
```bash
docker-compose up -d
```
The server will be available as an MCP host. If you are using it with a client (like Claude or a custom agent), point the client to the running server.

## Production Considerations

### Persistent Workspace Setup
To enable persistent data across sessions:
1.  Create a directory on your host (e.g., `./workspaces`).
2.  Set `WORKSPACE_ROOT=/path/to/workspaces` in your `.env`.
3.  The server will create a unique subdirectory for each session ID within that root.

### Docker Socket Security
The server requires access to `/var/run/docker.sock` to manage sessions. In production, ensure that the user running the server has the minimum necessary permissions. Consider using a Docker socket proxy for enhanced security.

### Customizing the R Image
If your research requires specific OHDSI packages not included in the default `Dockerfile.r-sandbox`, you can:
1.  Add `install.packages()` calls to `Dockerfile.r-sandbox`.
2.  Install them at runtime via `mcp.execute_in_session(session_id, "install.packages(...)")` (requires `GITHUB_PAT` and network access).

### Resource Scaling
The `MAX_SANDBOXES` setting should be tuned based on your host's CPU and Memory capacity. Each session consumes up to 512MB RAM.

---

For API details, see the [API Reference](api-reference.md).