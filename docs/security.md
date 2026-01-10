# Security Model - OMCP R Sandbox

Security is a primary design goal, ensuring that untrusted R code cannot compromise the host system while still allowing it to perform intensive OMOP analytics.

## 🛡️ Container Isolation

Each R session runs in a dedicated Docker container with the following restrictions:

- **User Isolation**: Containers run as a non-root user (`sandboxuser`, UID 1000).
- **Dropped Capabilities**: All Linux capabilities are dropped (`cap_drop=["ALL"]`).
- **No Privilege Escalation**: Containers are started with `no-new-privileges`.
- **Read-only Filesystem**: The root filesystem is read-only. Writable areas are limited to high-performance `tmpfs` mounts:
  - `/tmp`: 100MB (noexec, nosuid)
  - `/sandbox`: 500MB (noexec, nosuid)
- **Network Isolation**: By default, containers have no network access unless configured via Docker Compose.

## 🧠 Resource Management

To prevent Denial of Service (DoS) attacks:
- **Memory Limits**: Each container is capped at `512MB` of RAM.
- **CPU Limits**: Containers are restricted to `0.5` CPU cores (`cpu_quota=50000`).
- **Auto-Cleanup**: The `SessionManager` monitors activity and removes containers that have been idle past the `SANDBOX_TIMEOUT`.

## 📂 File I/O Security

The server provides tools for reading and writing files. This is handled via the Docker API:
- **Scope Restriction**: File operations are restricted to the container's filesystem.
- **Buffered Transfers**: Files are moved as base64-encoded strings or text, preventing direct filesystem mounting risks.
- **Atomic Operations**: Writing files uses Docker's archive mechanism, which is more secure than simple stream redirection.

## 📝 Audit and Logging

- **FastMCP Logging**: All MCP tool calls are logged with their parameters (excluding sensitive data like passwords).
- **Rserve Logs**: R output and errors are captured and returned to the MCP client.
- **Docker Events**: Container lifecycle events (start/stop) are visible in the host's Docker logs.

## ⚠️ Known Limitations & Best Practices

- **Database Credentials**: Database passwords are passed via environment variables. Ensure the host environment is secure.
- **Network Access**: If `DatabaseConnector` requires network access to hit an external CDM, careful VPC or Docker network rules should be applied.

---

For more information, see the [Configuration Guide](configuration.md).