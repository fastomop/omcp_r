# OMCP R Sandbox Server

A secure, MCP-compliant R code execution environment specialized for **OMOP CDM** and **DARWIN EU®** analytics. This server implements the Model Context Protocol (MCP) for safe, isolated, and stateful R session management.

## 🌟 Key Features

- **OMOP/DARWIN Specialized**: Pre-configured with OHDSI HADES and DARWIN R packages (`CDMConnector`, `DatabaseConnector`, `SqlRender`, etc.) and Java 17.
- **Persistent R Sessions**: Maintain state across multiple code executions using Docker-based Rserve containers.
- **File Management**: Built-in tools to upload cohort definitions, list sandbox files, and retrieve analysis results (CSVs, figures, etc.).
- **Enterprise-Grade Security**: 
  - Docker isolation with non-root user (UID 1000).
  - Read-only root filesystem with limited writable `tmpfs`.
  - Dropped Linux capabilities and no privilege escalation.
  - Network isolation (configurable) and resource limits (CPU/Memory).
- **Standardized Connectivity**: Ready for PostgreSQL/OMOP CDM databases with environment-based configuration.

## 🛠️ MCP Tools

The server exposes the following tools to any MCP client:

| Tool | Description |
|------|-------------|
| `create_session` | Start a new persistent R session (Docker container). |
| `execute_in_session` | Run R code in a session. State (variables, libraries) persists. |
| `list_sessions` | List all active R sessions and their metadata. |
| `close_session` | Safely stop and remove an R session. |
| `list_session_files` | List files in the session's workspace. |
| `read_session_file` | Read the content of a file (e.g., analysis results). |
| `write_session_file` | Upload a file to the sandbox (e.g., JSON cohort). |

## 🚀 Quick Start

### Prerequisites
- **Docker** and **Docker Compose**
- **Python 3.10+**
- **uv** (recommended for Python dependency management)

### 1. Installation
```sh
git clone https://github.com/Z0shua/omcp_r.git
cd omcp_r
uv pip install -e .
```

### 2. Environment Setup
Copy `sample.env` to `.env` and configure your database and Docker settings:
```env
DOCKER_IMAGE=omcp-r-sandbox:latest
SANDBOX_TIMEOUT=300
DB_HOST=your-postgres-host
DB_NAME=cdm_database
# ... see sample.env for all options
```

### 3. Build & Run
Use Docker Compose to build the specialized R sandbox image and start the MCP server:
```sh
docker-compose up --build
```

## 📖 Documentation

For detailed guides, please refer to the [docs/](docs/README.md) directory:
- [Architecture Overview](docs/architecture.md)
- [API Reference](docs/api-reference.md)
- [Implementation Details](docs/implementation.md)
- [Security Model](docs/security.md)
- [Configuration Guide](docs/configuration.md)
- [Deployment Guide](docs/deployment.md)

## ⚖️ License
MIT
