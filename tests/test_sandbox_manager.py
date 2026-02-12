from datetime import datetime
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from omcp_r.errors import SandboxError
from omcp_r.sandbox_manager import SessionManager


def make_manager() -> SessionManager:
    manager = SessionManager.__new__(SessionManager)
    manager.config = SimpleNamespace(
        max_file_write_bytes=16,
        max_file_read_bytes=16,
        max_code_chars=20,
        default_exec_timeout_secs=1.0,
        max_output_bytes=10,
    )
    manager.sessions = {
        "s1": {
            "last_used": datetime.now(),
            "created_at": datetime.now(),
            "host_port": "6311",
            "container": MagicMock(),
            "journal": [],
        }
    }
    return manager


def test_truncate_output_marks_truncated():
    manager = make_manager()
    text, truncated = manager._truncate_output("abcdefghijZ", 10)
    assert truncated is True
    assert text == "abcdefghij"


def test_write_file_rejects_large_content():
    manager = make_manager()
    with pytest.raises(SandboxError) as exc:
        manager.write_file("s1", "file.txt", "x" * 100)
    assert exc.value.code == "file_too_large"


def test_file_operations_reject_path_escape_before_container_call():
    manager = make_manager()
    with pytest.raises(SandboxError) as exc:
        manager.list_files("s1", "../etc")
    assert exc.value.code == "invalid_path"
    manager.sessions["s1"]["container"].exec_run.assert_not_called()


def test_execute_rejects_large_code_before_rserve():
    manager = make_manager()
    with pytest.raises(SandboxError) as exc:
        manager.execute_in_session("s1", "x" * 200)
    assert exc.value.code == "code_too_large"

