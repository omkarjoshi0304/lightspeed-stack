from app.endpoints.root import root_endpoint_handler


def test_root_endpoint(mocker):
    """Test the root endpoint handler."""
    request = None
    response = root_endpoint_handler(request)
    assert response is not None
