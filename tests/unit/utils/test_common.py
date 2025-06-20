from utils.common import retrieve_user_id, auth_dependency


# TODO(lucasagomes): Implement this test when the retrieve_user_id function is implemented
def test_retrieve_user_id():
    """Test that retrieve_user_id returns a user ID."""
    user_id = retrieve_user_id(None)
    assert user_id == "user_id_placeholder"


# TODO(lucasagomes): Implement this test when the auth_dependency function is implemented
async def test_auth_dependency(mocker):
    """Test that auth_dependency does not raise an exception."""
    result = await auth_dependency(mocker.Mock())
    assert result is True
