# Deployment Guide - OMCP R Sandbox

This document describes how to deploy the OMCP R Sandbox.

## Prerequisites

- Docker installed and running
- Python 3.10+ installed
- (Optional) .env file with configuration

## Quick Start

1. Build or pull the R sandbox Docker image (default: `rocker/r-base:latest`).
2. Set environment variables as needed (see [Configuration Guide](configuration.md)).
3. Start the MCP server:

```bash
python src/omcp_r/main.py
```

## Docker Compose (Optional)

If you use Docker Compose, ensure your `docker-compose.yml` references only the R sandbox service and image.

## Health Check

- Ensure the server starts without errors and can create R sandboxes.
- Check logs for any issues.

---

For more details, see the [Configuration Guide](configuration.md) and [Security Model](security.md). 