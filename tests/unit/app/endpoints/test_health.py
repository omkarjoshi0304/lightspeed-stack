from app.endpoints.health import readiness_probe_get_method, liveness_probe_get_method


def test_readiness_probe(mocker):
    """Test the readiness endpoint handler."""
    response = readiness_probe_get_method()
    assert response is not None
    assert response.ready is True
    assert response.reason == "service is ready"


def test_liveness_probe(mocker):
    """Test the liveness endpoint handler."""
    response = liveness_probe_get_method()
    assert response is not None
    assert response.alive is True
