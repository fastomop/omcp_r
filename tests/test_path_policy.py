import pytest

from omcp_r.path_policy import normalize_session_path, to_user_path


@pytest.mark.parametrize(
    "value,expected",
    [
        (".", "/sandbox"),
        ("foo/bar.txt", "/sandbox/foo/bar.txt"),
        ("/sandbox/foo", "/sandbox/foo"),
    ],
)
def test_normalize_session_path_valid(value, expected):
    assert normalize_session_path(value) == expected


@pytest.mark.parametrize("value", ["../etc/passwd", "/etc/passwd", "", "   "])
def test_normalize_session_path_rejects_escape(value):
    with pytest.raises(ValueError):
        normalize_session_path(value)


def test_to_user_path():
    assert to_user_path("/sandbox") == "."
    assert to_user_path("/sandbox/data/file.csv") == "data/file.csv"
    assert to_user_path("/other/path") == "/other/path"

