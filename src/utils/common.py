"""Common utilities for the project."""

from typing import Any

from fastapi import Request


# TODO(lucasagomes): implement this function to retrieve user ID from auth
def retrieve_user_id(auth: Any) -> str:  # pylint: disable=unused-argument
    """Retrieve the user ID from the authentication handler.

    Args:
        auth: The Authentication handler (FastAPI Depends) that will
            handle authentication Logic.

    Returns:
        str: The user ID.
    """
    return "user_id_placeholder"


# TODO(lucasagomes): implement this function to handle authentication
async def auth_dependency(_request: Request) -> bool:
    """Authenticate dependency to ensure the user is authenticated.

    Args:
        request (Request): The FastAPI request object.

    Raises:
        HTTPException: If the user is not authenticated.
    """
    return True
