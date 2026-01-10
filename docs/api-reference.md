# API Reference - OMCP R Sandbox

This document provides comprehensive API documentation for all MCP tools available in the OMCP R Sandbox.

## API Overview

The OMCP R Sandbox exposes the following MCP tools for secure, persistent R session management:

1. **create_session** - Create a new persistent R session
2. **list_sessions** - List active R sessions
3. **close_session** - Close and remove an R session
4. **execute_in_session** - Execute R code in a session

## Tool Specifications

### 1. create_session

Creates a new persistent R session backed by a Docker container running Rserve.

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| timeout   | Optional[int] | No | 300 | Session timeout in seconds |

#### Returns
```json
{
    "success": true,
    "session_id": "uuid-string",
    "created_at": "2024-01-01T12:00:00",
    "last_used": "2024-01-01T12:00:00",
    "host_port": "32768"
}
```

#### Error Response
```json
{
    "success": false,
    "error": "Error message describing the failure"
}
```

### 2. list_sessions

Lists all active R sessions.

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| include_inactive | bool | No | false | Whether to include timed-out sessions |

#### Returns
```json
{
    "success": true,
    "sessions": [
        {
            "id": "uuid-string",
            "created_at": "2024-01-01T12:00:00",
            "last_used": "2024-01-01T12:00:00",
            "host_port": "32768"
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

### 3. close_session

Closes and removes an R session.

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| session_id | str | Yes | - | The unique identifier of the session to close |

#### Returns
```json
{
    "success": true,
    "message": "Closed R session uuid-string"
}
```

#### Error Response
```json
{
    "success": false,
    "error": "Error message describing the failure"
}
```

### 4. execute_in_session

Executes R code in a persistent session. State is maintained across multiple calls.

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| session_id | str | Yes | - | The unique identifier of the session |
| code | str | Yes | - | The R code to execute |

#### Returns
```json
{
    "success": true,
    "result": "R evaluation result"
}
```

#### Error Response
```json
{
    "success": false,
    "error": "Error message describing the failure"
}
```

### 5. list_session_files

Lists files in the session's working directory.

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| session_id | str | Yes | - | Session ID |
| path | str | No | "." | Path to list (default: working directory) |

#### Returns
```json
{
    "success": true,
    "files": [
        {"name": "analysis.R", "is_dir": false, "path": "analysis.R"},
        {"name": "output", "is_dir": true, "path": "output"}
    ]
}
```

### 6. read_session_file

Reads a text file from the session.

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| session_id | str | Yes | - | Session ID |
| path | str | Yes | - | Path to file to read |

#### Returns
```json
{
    "success": true,
    "content": "file content here..."
}
```

### 7. write_session_file

Writes content to a file in the session.

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| session_id | str | Yes | - | Session ID |
| path | str | Yes | - | Path where file should be written |
| content | str | Yes | - | Content to write |

#### Returns
```json
{
    "success": true,
    "message": "Successfully wrote to path/to/file.R"
}
```

## Session Lifecycle

1. **Create Session**: Creates a Docker container running Rserve
2. **Execute Code**: Send R code to execute; state persists between calls
3. **Close Session**: Stops and removes the container

## Database Connections

Sessions can connect to databases (e.g., PostgreSQL) using environment variables passed to the container:

```r
library(DBI)
con <- dbConnect(
  RPostgres::Postgres(),
  host = Sys.getenv("DB_HOST"),
  port = as.integer(Sys.getenv("DB_PORT")),
  user = Sys.getenv("DB_USER"),
  password = Sys.getenv("DB_PASSWORD"),
  dbname = Sys.getenv("DB_NAME")
)
```

---

For more details, see the [Implementation Details](implementation.md) and [Configuration Guide](configuration.md).