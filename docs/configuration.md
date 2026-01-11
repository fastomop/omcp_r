# Configuration Guide - OMCP R Sandbox

The OMCP R Sandbox is configured primarily through environment variables. This guide details all available options.

## Core Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `SANDBOX_TIMEOUT` | int | `300` | Inactivity timeout in seconds before a session is automatically closed. |
| `MAX_SANDBOXES` | int | `10` | Maximum number of concurrent R sessions allowed. |
| `DOCKER_IMAGE` | str | `omcp-r-sandbox:latest` | The name of the Docker image to use for R sessions. |
| `LOG_LEVEL` | str | `INFO` | Logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`). |
| `DOCKER_HOST` | str | `unix://var/run/docker.sock` | Connection string for the Docker daemon. |
| `WORKSPACE_ROOT` | str | `""` | Local absolute path to store persistent session workspaces (e.g. `/tmp/sandboxes`). |

## OMOP/DARWIN Database Settings

These variables are injected into every R session container, allowing R code to access them via `Sys.getenv()`.

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `DB_HOST` | str | `""` | Hostname of the OMOP CDM database. |
| `DB_PORT` | int | `5432` | Port of the database (usually Postgres). |
| `DB_USER` | str | `""` | Database username. |
| `DB_PASSWORD` | str | `""` | Database password. |
| `DB_NAME` | str | `""` | Name of the CDM database. |

## Dependency Management

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `GITHUB_PAT` | str | `""` | Personal Access Token for GitHub. Used inside the sandbox to install OHDSI packages from private or rate-limited repositories. |

## Sample `.env` File

```env
# Server Limits
SANDBOX_TIMEOUT=600
MAX_SANDBOXES=5

# Docker Connectivity
DOCKER_HOST=unix:///var/run/docker.sock
DOCKER_IMAGE=omcp-r-sandbox:latest

# Database Credentials
DB_HOST=postgres.example.org
DB_PORT=5432
DB_USER=ohdsi_user
DB_PASSWORD=secure_password
DB_NAME=omop_cdm

# GitHub Authentication
GITHUB_PAT=ghp_exampleToken123
```

---

For more details on how these settings are applied, see [Implementation Details](implementation.md).