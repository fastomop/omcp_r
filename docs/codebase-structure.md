# Codebase Structure - OMCP R Sandbox

This document describes the organization of the OMCP R Sandbox codebase.

## Directory Layout

```
.
├── docs/                # Documentation
├── src/
│   └── omcp_r/
│       ├── main.py              # FastMCP server for R sandbox
│       ├── sandbox_manager.py   # Docker-based R sandbox manager
│       ├── config.py            # Configuration loader
│       ├── core/                # (Reserved for future core logic)
│       ├── tools/               # (Reserved for future R tools)
│       └── utils/               # (Reserved for future utilities)
├── Dockerfile           # Docker image for the R sandbox
├── docker-compose.yml   # Docker Compose configuration (if used)
├── sample.env           # Example environment configuration
└── README.md            # Project overview and documentation index
```

## Key Files

- **main.py**: Entry point for the FastMCP server, exposes R sandbox tools.
- **sandbox_manager.py**: Manages Docker containers for R sandboxes.
- **config.py**: Loads configuration from environment variables.

## Configuration

- All configuration is environment-based. See [Configuration Guide](configuration.md).

## Extending the Codebase

- Add new R tools in `tools/`.
- Add core logic in `core/` as needed.
- Add utility functions in `utils/`.

---

For more details, see the [Architecture Overview](architecture.md) and [Implementation Details](implementation.md). 