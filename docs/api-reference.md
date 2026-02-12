# API Reference - OMCP R Sandbox

The MCP server exposes the following tools:

1. `create_session(timeout: Optional[int] = 300)`
2. `list_sessions()`
3. `close_session(session_id: str)`
4. `execute_in_session(session_id: str, code: str, limits: Optional[dict] = None)`
5. `list_session_files(session_id: str, path: str = ".")`
6. `read_session_file(session_id: str, path: str)`
7. `write_session_file(session_id: str, path: str, content: str)`
8. `install_package(session_id: str, package_name: str, source: str = "CRAN")`

## Standard Response Envelope

### Success
```json
{
  "success": true,
  "...": "tool-specific fields"
}
```

### Error
```json
{
  "success": false,
  "error": {
    "code": "machine_readable_code",
    "message": "human readable message",
    "retryable": false,
    "details": {}
  }
}
```

## `execute_in_session` Limits

`limits` is optional and supports:

- `max_duration_secs` (number, `> 0`)
- `max_output_bytes` (integer, `> 0`)

Example:
```json
{
  "session_id": "session-uuid",
  "code": "print('hello')",
  "limits": {
    "max_duration_secs": 5,
    "max_output_bytes": 20000
  }
}
```

Execution responses include:

- `output`: captured `stdout`/`stderr`
- `result`: textual representation of the final value (on success)
- `meta.elapsed_secs`
- `meta.output_truncated`

## File Path Policy

File tools are restricted to `/sandbox`:

- Relative paths are resolved under `/sandbox`
- Absolute paths must already be under `/sandbox`
- Path traversal outside `/sandbox` is rejected with `error.code = "invalid_path"`
