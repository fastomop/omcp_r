# OMCP R Sandbox - Technical Documentation

Welcome to the technical documentation for the OMCP R Sandbox project. This documentation provides comprehensive information about the codebase architecture, implementation details, and usage patterns for the R sandbox.

## 📚 Documentation Structure

### Core Documentation
- **[Architecture Overview](architecture.md)** - High-level system architecture and design principles for the R sandbox
- **[Codebase Structure](codebase-structure.md)** - Detailed breakdown of the R sandbox codebase organization
- **[Implementation Details](implementation.md)** - Deep dive into key components and their implementation
- **[Security Model](security.md)** - Security architecture and threat mitigation strategies

### Usage Documentation
- **[API Reference](api-reference.md)** - Complete API documentation for all MCP tools
- **[Configuration Guide](configuration.md)** - Environment variables and configuration options
- **[Deployment Guide](deployment.md)** - Production deployment and operational considerations

## 🏗️ Project Overview

The OMCP R Sandbox is a secure, Model Context Protocol (MCP) compliant R code execution environment that provides isolated, containerized R environments for safe code execution. Built with enterprise-grade security features, it enables AI agents and applications to execute R code without compromising system security.

### Key Components

1. **FastMCP Server** (`src/omcp_r/main.py`) - Main MCP server implementation using FastMCP framework for R
2. **Sandbox Manager** (`src/omcp_r/sandbox_manager.py`) - Docker container lifecycle management for R sandboxes
3. **Configuration System** (`src/omcp_r/config.py`) - Environment-based configuration management for R sandboxes

## 🚀 Quick Start

1. Ensure Docker is installed and running.
2. Configure environment variables as needed (see [Configuration Guide](configuration.md)).
3. Start the MCP server:

```bash
python src/omcp_r/main.py
```

4. Use the MCP tools to create, manage, and execute R code in sandboxes.

## 🛡️ Security

The R sandbox uses Docker-based isolation, resource limits, and strict security options to ensure safe code execution. See [Security Model](security.md) for details.

## 🧪 Testing

Testing instructions and examples are provided in the documentation. 