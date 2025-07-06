# Configuration Guide - OMCP R Sandbox

This document describes the configuration options for the OMCP R Sandbox.

## Environment Variables

| Variable            | Type   | Default                | Description                                 |
|---------------------|--------|------------------------|---------------------------------------------|
| SANDBOX_TIMEOUT     | int    | 300                    | Sandbox timeout in seconds                  |
| MAX_SANDBOXES       | int    | 10                     | Maximum number of concurrent sandboxes      |
| DOCKER_IMAGE        | str    | rocker/r-base:latest   | Docker image for R sandboxes                |
| LOG_LEVEL           | str    | INFO                   | Logging level                               |
| DOCKER_HOST         | str    | unix://var/run/docker.sock | Docker daemon connection URL           |

## Sample .env File

```
SANDBOX_TIMEOUT=300
MAX_SANDBOXES=10
DOCKER_IMAGE=rocker/r-base:latest
LOG_LEVEL=INFO
DOCKER_HOST=unix://var/run/docker.sock
```

## Configuration Loading

Configuration is loaded from environment variables at startup. See `src/omcp_r/config.py` for implementation details.

---

For more details, see the [Implementation Details](implementation.md) and [Security Model](security.md). 