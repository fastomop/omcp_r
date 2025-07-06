# API Reference - OMCP R Sandbox

This document provides comprehensive API documentation for all MCP tools available in the OMCP R Sandbox.

## API Overview

The OMCP R Sandbox exposes the following MCP tools for secure R code execution:

1. **create_sandbox** - Create new isolated R environments
2. **list_sandboxes** - List and manage active sandboxes
3. **remove_sandbox** - Safely remove sandboxes
4. **execute_r_code** - Run R code in isolated containers

## Tool Specifications

### 1. create_sandbox

Creates a new isolated R sandbox environment.

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| timeout   | Optional[int] | No | 300 | Sandbox timeout in seconds |

#### Returns
```json
{
    "success": true,
    "sandbox_id": "uuid-string",
    "created_at": "2024-01-01T12:00:00",
    "last_used": "2024-01-01T12:00:00"
}
```

#### Error Response
```json
{
    "success": false,
    "error": "Error message describing the failure"
}
```

### 2. list_sandboxes

Lists all active R sandboxes.

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| include_inactive | bool | No | false | Whether to include inactive sandboxes |

#### Returns
```json
{
    "success": true,
    "sandboxes": [
        {
            "id": "uuid-string",
            "created_at": "2024-01-01T12:00:00",
            "last_used": "2024-01-01T12:00:00"
        }
    ],
    "count": 1
}
```

#### Error Response
```json
{
    "success": false,
    "error": "Error message describing the failure"
}
```

### 3. remove_sandbox

Removes an R sandbox.

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| sandbox_id | str | Yes | - | The unique identifier of the sandbox to remove |
| force | bool | No | false | Whether to force removal of active sandboxes |

#### Returns
```json
{
    "success": true,
    "message": "Sandbox uuid-string removed successfully"
}
```

#### Error Response
```json
{
    "success": false,
    "error": "Error message describing the failure"
}
```

### 4. execute_r_code

Runs R code in an isolated sandbox.

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| sandbox_id | str | Yes | - | The unique identifier of the sandbox |
| code | str | Yes | - | The R code to execute |
| timeout | Optional[int] | No | 30 | Code execution timeout in seconds |

#### Returns
```json
{
    "success": true,
    "output": "R code output",
    "exit_code": 0
}
```

#### Error Response
```json
{
    "success": false,
    "error": "Error message describing the failure"
}
```

---

For more details, see the [Implementation Details](implementation.md) and [Configuration Guide](configuration.md). 