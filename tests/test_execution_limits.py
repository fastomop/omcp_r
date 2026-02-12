import pytest

from omcp_r.errors import SandboxError
from omcp_r.execution_limits import ExecutionLimits


def test_execution_limits_defaults():
    limits = ExecutionLimits.from_payload(
        None,
        default_duration_secs=12.5,
        default_output_bytes=4096,
    )
    assert limits.max_duration_secs == 12.5
    assert limits.max_output_bytes == 4096


def test_execution_limits_override():
    limits = ExecutionLimits.from_payload(
        {"max_duration_secs": 3, "max_output_bytes": 100},
        default_duration_secs=12.5,
        default_output_bytes=4096,
    )
    assert limits.max_duration_secs == 3.0
    assert limits.max_output_bytes == 100


@pytest.mark.parametrize(
    "payload,expected",
    [
        ("bad", "limits must be an object"),
        ({"max_duration_secs": 0}, "max_duration_secs must be > 0"),
        ({"max_duration_secs": "x"}, "max_duration_secs must be a number"),
        ({"max_output_bytes": 0}, "max_output_bytes must be > 0"),
        ({"max_output_bytes": "x"}, "max_output_bytes must be an integer"),
    ],
)
def test_execution_limits_invalid(payload, expected):
    with pytest.raises(SandboxError) as exc:
        ExecutionLimits.from_payload(
            payload,  # type: ignore[arg-type]
            default_duration_secs=10,
            default_output_bytes=1000,
        )
    assert exc.value.code == "invalid_limits"
    assert expected in exc.value.message

