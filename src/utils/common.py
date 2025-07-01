"""Common utilities for the project."""

from typing import Any, List, cast
from logging import Logger

from llama_stack_client import LlamaStackClient

from llama_stack.distribution.library_client import (
    LlamaStackAsLibraryClient,
    AsyncLlamaStackAsLibraryClient,
)

from client import get_llama_stack_client
from models.config import Configuration, ModelContextProtocolServer


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


async def register_mcp_servers_async(
    logger: Logger, configuration: Configuration
) -> None:
    """Register Model Context Protocol (MCP) servers with the LlamaStack client (async)."""
    # Skip MCP registration if no MCP servers are configured
    if not configuration.mcp_servers:
        logger.debug("No MCP servers configured, skipping registration")
        return

    if configuration.llama_stack.use_as_library_client:
        # Library client - use async interface
        # config.py validation ensures library_client_config_path is not None
        # when use_as_library_client is True
        config_path = cast(str, configuration.llama_stack.library_client_config_path)
        client = LlamaStackAsLibraryClient(config_path)
        await client.async_client.initialize()

        await _register_mcp_toolgroups_async(
            client.async_client, configuration.mcp_servers, logger
        )
    else:
        # Service client - use sync interface
        client = get_llama_stack_client(configuration.llama_stack)

        _register_mcp_toolgroups_sync(client, configuration.mcp_servers, logger)


async def _register_mcp_toolgroups_async(
    client: AsyncLlamaStackAsLibraryClient,
    mcp_servers: List[ModelContextProtocolServer],
    logger: Logger,
) -> None:
    """Async logic for registering MCP toolgroups."""
    # Get registered tools
    registered_tools = await client.tools.list()
    registered_toolgroups = [tool.toolgroup_id for tool in registered_tools]
    logger.debug("Registered toolgroups: %s", set(registered_toolgroups))

    # Register toolgroups for MCP servers if not already registered
    for mcp in mcp_servers:
        if mcp.name not in registered_toolgroups:
            logger.debug("Registering MCP server: %s, %s", mcp.name, mcp.url)

            registration_params = {
                "toolgroup_id": mcp.name,
                "provider_id": mcp.provider_id,
                "mcp_endpoint": {"uri": mcp.url},
            }

            await client.toolgroups.register(**registration_params)
            logger.debug("MCP server %s registered successfully", mcp.name)


def _register_mcp_toolgroups_sync(
    client: LlamaStackClient,
    mcp_servers: List[ModelContextProtocolServer],
    logger: Logger,
) -> None:
    """Sync logic for registering MCP toolgroups."""
    # Get registered tools
    registered_tools = client.tools.list()
    registered_toolgroups = [tool.toolgroup_id for tool in registered_tools]
    logger.debug("Registered toolgroups: %s", set(registered_toolgroups))

    # Register toolgroups for MCP servers if not already registered
    for mcp in mcp_servers:
        if mcp.name not in registered_toolgroups:
            logger.debug("Registering MCP server: %s, %s", mcp.name, mcp.url)

            registration_params = {
                "toolgroup_id": mcp.name,
                "provider_id": mcp.provider_id,
                "mcp_endpoint": {"uri": mcp.url},
            }

            client.toolgroups.register(**registration_params)
            logger.debug("MCP server %s registered successfully", mcp.name)
