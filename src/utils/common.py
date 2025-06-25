"""Common utilities for the project."""

from typing import Any
from logging import Logger


from client import get_llama_stack_client
from models.config import Configuration


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


def register_mcp_servers(logger: Logger, configuration: Configuration) -> None:
    """Register Model Context Protocol (MCP) servers with the LlamaStack client."""
    # Get list of registered tools and extract their toolgroup IDs
    client = get_llama_stack_client(configuration.llama_stack)
    registered_tools = client.tools.list()
    registered_toolgroups = [tool.toolgroup_id for tool in registered_tools]
    logger.debug("Registered toolgroups: %s", set(registered_toolgroups))
    # Register toolgroups for MCP servers if not already registered
    for mcp in configuration.mcp_servers:
        if mcp.name not in registered_toolgroups:  # required
            logger.debug("Registering MCP server: %s, %s", mcp.name, mcp.url)
            client.toolgroups.register(
                toolgroup_id=mcp.name,
                provider_id=mcp.provider_id,
                mcp_endpoint={"uri": mcp.url},
            )
            logger.debug("MCP server %s registered successfully", mcp.name)
