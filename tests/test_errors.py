from omcp_r.errors import error_payload


def test_error_payload_shape():
    payload = error_payload("invalid_path", "bad path", retryable=False, details={"path": "../x"})
    assert payload["success"] is False
    assert payload["error"]["code"] == "invalid_path"
    assert payload["error"]["message"] == "bad path"
    assert payload["error"]["retryable"] is False
    assert payload["error"]["details"]["path"] == "../x"

