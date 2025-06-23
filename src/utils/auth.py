"""Authentication handling."""

from fastapi import Request


# TODO(lucasagomes): implement this function to handle authentication
async def auth_dependency(_request: Request) -> bool:
    """Authenticate dependency to ensure the user is authenticated.

    Args:
        request (Request): The FastAPI request object.

    Raises:
        HTTPException: If the user is not authenticated.
    """
    return True
