from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from omcp_r.errors import SandboxError


@dataclass(frozen=True)
class ExecutionLimits:
    max_duration_secs: float
    max_output_bytes: int

    @classmethod
    def from_payload(
        cls,
        payload: Optional[Dict[str, Any]],
        *,
        default_duration_secs: float,
        default_output_bytes: int,
    ) -> "ExecutionLimits":
        if payload is None:
            return cls(
                max_duration_secs=default_duration_secs,
                max_output_bytes=default_output_bytes,
            )
        if not isinstance(payload, dict):
            raise SandboxError(
                "invalid_limits",
                "limits must be an object",
                details={"received_type": type(payload).__name__},
            )

        duration = payload.get("max_duration_secs", default_duration_secs)
        output_bytes = payload.get("max_output_bytes", default_output_bytes)

        try:
            duration = float(duration)
        except (TypeError, ValueError):
            raise SandboxError("invalid_limits", "max_duration_secs must be a number")
        if duration <= 0:
            raise SandboxError("invalid_limits", "max_duration_secs must be > 0")

        try:
            output_bytes = int(output_bytes)
        except (TypeError, ValueError):
            raise SandboxError("invalid_limits", "max_output_bytes must be an integer")
        if output_bytes <= 0:
            raise SandboxError("invalid_limits", "max_output_bytes must be > 0")

        return cls(max_duration_secs=duration, max_output_bytes=output_bytes)

