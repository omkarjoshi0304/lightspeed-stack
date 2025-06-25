"""Authentication handling."""

from fastapi import Request


# TODO(lucasagomes): implement this function to handle authentication
async def auth_dependency(_request: Request) -> str:
    """Authenticate dependency to ensure the user is authenticated.

    Args:
        request (Request): The FastAPI request object.

    Raises:
        HTTPException: If the user is not authenticated.
    """
    return extract_access_token(_request)


def extract_access_token(request: Request) -> str:
    """Extract access token from the Authorization header.

    Args:
        request: The FastAPI request object

    Returns:
        The access token string, or empty string if not found
    """
    authorization_header = request.headers.get("Authorization", "")
    if authorization_header.startswith("Bearer "):
        return authorization_header[7:]  # Remove "Bearer " prefix
    return ""
