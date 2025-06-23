from utils.auth import auth_dependency


# TODO(lucasagomes): Implement this test when the auth_dependency function is implemented
async def test_auth_dependency(mocker):
    """Test that auth_dependency does not raise an exception."""
    result = await auth_dependency(mocker.Mock())
    assert result is True
