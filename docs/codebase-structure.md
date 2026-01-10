# Codebase Structure - OMCP R Sandbox

This document describes the organization of the OMCP R Sandbox codebase.

## Directory Layout

```
.
├── docs/                # Technical documentation
├── src/
│   └── omcp_r/
│       ├── main.py              # FastMCP server (tools & routing)
│       ├── sandbox_manager.py   # Lifecycle & Rserve management
│       ├── config.py            # Configuration loader
│       ├── core/                # (Reserved for future core logic)
│       ├── tools/               # (Reserved for future R tools)
│       └── utils/               # (Reserved for future utilities)
├── Dockerfile           # Dockerfile for the Python MCP server
├── Dockerfile.r-sandbox # Specialized Dockerfile for OMOP/DARWIN R sessions
├── docker-compose.yml   # Multi-service build and run configuration
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Build system and Python metadata
├── sample.env           # Example environment configuration
└── README.md            # Project overview and entry point
```

## Key Files

- **`src/omcp_r/main.py`**: The primary entry point. It defines the MCP tools and delegates sandbox operations to the `SessionManager`.
- **`src/omcp_r/sandbox_manager.py`**: Contains the `SessionManager` class which handles Docker container creation, Rserve connections via `pyRserve`, and file archiving.
- **`Dockerfile.r-sandbox`**: Defines the environment where R code actually runs. It is built on `rocker/tidyverse` and adds Java, OHDSI tools, and Rserve.
- **`docker-compose.yml`**: Orchestrates the build of the specialized R image and the execution of the MCP server.

## Configuration

All configuration is environment-based. See the [Configuration Guide](configuration.md) for a full list of variables like `DB_HOST` and `SANDBOX_TIMEOUT`.

## Extending the Codebase

- **Adding MCP Tools**: Modify `src/omcp_r/main.py` and `sandbox_manager.py`.
- **Adding R Libraries**: Add `install.packages()` calls to `Dockerfile.r-sandbox` and rebuild.
- **Core Logic**: Use the `src/omcp_r/core/` directory for heavy computational or analytical logic shared across tools.

---

For more details, see the [Architecture Overview](architecture.md) and [Implementation Details](implementation.md).