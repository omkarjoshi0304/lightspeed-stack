from utils.common import retrieve_user_id


# TODO(lucasagomes): Implement this test when the retrieve_user_id function is implemented
def test_retrieve_user_id():
    """Test that retrieve_user_id returns a user ID."""
    user_id = retrieve_user_id(None)
    assert user_id == "user_id_placeholder"
