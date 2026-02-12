from __future__ import annotations

import posixpath


SANDBOX_ROOT = "/sandbox"


def normalize_session_path(path: str) -> str:
    if not isinstance(path, str) or not path.strip():
        raise ValueError("path must be a non-empty string")

    cleaned = path.strip()
    candidate = cleaned if cleaned.startswith("/") else f"{SANDBOX_ROOT}/{cleaned}"
    normalized = posixpath.normpath(candidate)

    if normalized == SANDBOX_ROOT or normalized.startswith(f"{SANDBOX_ROOT}/"):
        return normalized
    raise ValueError("path must resolve under /sandbox")


def to_user_path(absolute_path: str) -> str:
    if absolute_path == SANDBOX_ROOT:
        return "."
    if absolute_path.startswith(f"{SANDBOX_ROOT}/"):
        return absolute_path[len(SANDBOX_ROOT) + 1 :]
    return absolute_path

