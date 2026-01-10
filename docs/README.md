# OMCP R Sandbox - Technical Documentation

Welcome to the technical documentation for the OMCP R Sandbox, a specialized environment for secure OMOP CDM and DARWIN EU® analytics.

## 📚 Documentation Structure

### Core Documentation
- **[Architecture Overview](architecture.md)** - High-level system design including the Rserve session model.
- **[Implementation Details](implementation.md)** - Deep dive into specialized R tools and sandbox management.
- **[Security Model](security.md)** - Isolation strategies, resource limits, and file I/O security.

### Usage Documentation
- **[API Reference](api-reference.md)** - Complete documentation for session and file management tools.
- **[Configuration Guide](configuration.md)** - Details on environment variables (Database, Docker, GITHUB_PAT).
- **[Deployment Guide](deployment.md)** - Instructions for building and running via Docker Compose.

## 🏗️ Project Overview

The OMCP R Sandbox transforms a generic R environment into a powerful tool for observational health research. By providing persistent, containerized sessions pre-loaded with OHDSI HADES tools, it enables AI agents to perform complex data characterization and cohort studies safely.

### Key Components

1. **FastMCP Server** (`src/omcp_r/main.py`) - The entry point that translates MCP requests into sandbox actions.
2. **Session Manager** (`src/omcp_r/sandbox_manager.py`) - Handles the lifecycle of Rserve-enabled Docker containers.
3. **R Sandbox Image** (`Dockerfile.r-sandbox`) - A specialized image containing Java 17 and DARWIN R packages.

## 🚀 Getting Started

1. Ensure Docker is running.
2. Build the images: `docker-compose build`.
3. Launch the server: `docker-compose up`.

---
*For general project information, see the root [README.md](../README.md).*