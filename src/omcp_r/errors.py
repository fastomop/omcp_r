from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SandboxError(Exception):
    code: str
    message: str
    retryable: bool = False
    details: Optional[Dict[str, Any]] = None

    def __str__(self) -> str:
        return self.message


def error_payload(
    code: str,
    message: str,
    *,
    retryable: bool = False,
    details: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "retryable": retryable,
        },
    }
    if details:
        payload["error"]["details"] = details
    return payload

