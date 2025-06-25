from utils.auth import auth_dependency


# TODO(lucasagomes): Implement this test when the auth_dependency function is implemented
async def test_auth_dependency(mocker):
    """Test that auth_dependency does not raise an exception."""
    # Create a mock request with proper headers
    mock_request = mocker.Mock()
    mock_request.headers.get.return_value = "Bearer test_token"

    result = await auth_dependency(mock_request)
    assert result == "test_token"


async def test_auth_dependency_no_auth_header(mocker):
    """Test that auth_dependency returns empty string when no Authorization header."""
    # Create a mock request with no Authorization header
    mock_request = mocker.Mock()
    mock_request.headers.get.return_value = ""

    result = await auth_dependency(mock_request)
    assert result == ""


async def test_auth_dependency_invalid_auth_header(mocker):
    """Test that auth_dependency returns empty string for invalid Authorization header."""
    # Create a mock request with invalid Authorization header
    mock_request = mocker.Mock()
    mock_request.headers.get.return_value = "Invalid header"

    result = await auth_dependency(mock_request)
    assert result == ""
