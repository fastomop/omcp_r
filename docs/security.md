# Security Model - OMCP R Sandbox

This document describes the security architecture of the OMCP R Sandbox.

## Security Overview

The OMCP R Sandbox is designed for safe, isolated R code execution using Docker containers. The following security measures are enforced:

- **Network Isolation**: Containers run with no network access (`network_mode="none"`).
- **Resource Limits**: Each container is limited in memory and CPU usage.
- **User Isolation**: Containers run as a non-root user (UID 1000).
- **Read-only Filesystem**: The root filesystem is read-only, with limited writable tmpfs mounts for `/tmp` and `/sandbox`.
- **Dropped Capabilities**: All Linux capabilities are dropped (`cap_drop=["ALL"]`).
- **No Privilege Escalation**: Containers are started with `no-new-privileges`.
- **Automatic Cleanup**: Inactive sandboxes are automatically removed after a timeout.
- **Input Validation**: All user input (R code, parameters) is validated before execution.
- **Comprehensive Logging**: All actions and errors are logged for audit and debugging.

## Security Best Practices

- Always keep Docker and system packages up to date.
- Use strong resource limits to prevent abuse.
- Monitor logs for unusual activity.

---

For more details, see the [Implementation Details](implementation.md) and [Configuration Guide](configuration.md). 