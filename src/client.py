# """LLama stack client retrieval with redaction capabilities."""

# import logging

# from llama_stack.distribution.library_client import LlamaStackAsLibraryClient  # type: ignore
# from llama_stack_client import LlamaStackClient  # type: ignore
# from models.config import LLamaStackConfiguration

# logger = logging.getLogger(__name__)


# # Simple redaction patterns - configure as needed
# REDACTION_PATTERNS = [
#     (r'\bfoo\b', 'deployment'),
#     (r'\bbar\b', 'openshift'),
#     (r'\bpassword\b', '[REDACTED]'),
#     (r'\bsecret\b', '[REDACTED]'),
# ]


# def apply_redaction(text: str, conversation_id: str = "unknown") -> str:
#     """Apply redaction patterns to text."""
#     import re

#     if not text:
#         return text

#     redacted_text = text
#     redactions_made = 0

#     for pattern, replacement in REDACTION_PATTERNS:
#         compiled_pattern = re.compile(pattern, re.IGNORECASE)
#         matches = len(compiled_pattern.findall(redacted_text))
#         if matches > 0:
#             redacted_text = compiled_pattern.sub(replacement, redacted_text)
#             redactions_made += matches

#     if redactions_made > 0:
#         logger.info(f"Applied {redactions_made} redactions for conversation {conversation_id}")

#     return redacted_text


# class RedactionEnabledClient:
#     """Wrapper client that adds redaction capabilities."""

#     def __init__(self, base_client):
#         self.base_client = base_client

#     def apply_redaction(self, query: str, attachments: list, conversation_id: str):
#         """Apply redaction to query and attachments."""
#         # Redact query
#         redacted_query = apply_redaction(query, conversation_id)

#         # Redact attachments
#         redacted_attachments = []
#         if attachments:
#             for attachment in attachments:
#                 redacted_content = apply_redaction(attachment.content, conversation_id)
#                 # Create new attachment with redacted content
#                 redacted_attachment = type(attachment)(
#                     attachment_type=attachment.attachment_type,
#                     content_type=attachment.content_type,
#                     content=redacted_content
#                 )
#                 redacted_attachments.append(redacted_attachment)

#         return redacted_query, redacted_attachments

#     def __getattr__(self, name):
#         """Delegate all other attributes to base client."""
#         return getattr(self.base_client, name)


# def get_llama_stack_client(
#     llama_stack_config: LLamaStackConfiguration,
# ) -> RedactionEnabledClient:
#     """Retrieve Llama stack client with redaction capabilities."""
#     if llama_stack_config.use_as_library_client is True:
#         if llama_stack_config.library_client_config_path is not None:
#             logger.info("Using Llama stack as library client")
#             client = LlamaStackAsLibraryClient(
#                 llama_stack_config.library_client_config_path
#             )
#             client.initialize()
#             return RedactionEnabledClient(client)
#         msg = "Configuration problem: library_client_config_path option is not set"
#         logger.error(msg)
#         raise Exception(msg)  # pylint: disable=broad-exception-raised

#     logger.info("Using Llama stack running as a service")
#     base_client = LlamaStackClient(
#         base_url=llama_stack_config.url, api_key=llama_stack_config.api_key
#     )
#     return RedactionEnabledClient(base_client)

"""LLama stack client retrieval with redaction capabilities."""

import logging

from llama_stack.distribution.library_client import (
    AsyncLlamaStackAsLibraryClient,  # type: ignore
    LlamaStackAsLibraryClient,  # type: ignore
)
from llama_stack_client import AsyncLlamaStackClient, LlamaStackClient  # type: ignore
from models.config import LLamaStackConfiguration

logger = logging.getLogger(__name__)


# Simple redaction patterns - configure as needed
REDACTION_PATTERNS = [
    (r"\bfoo\b", "deployment"),
    (r"\bbar\b", "openshift"),
    (r"\bpassword\b", "omkar123"),
    (r"\bsecret\b", "lightspeed"),
]


def apply_redaction(text: str, conversation_id: str = "unknown") -> str:
    """Apply redaction patterns to text."""
    import re

    if not text:
        return text

    redacted_text = text
    redactions_made = 0

    for pattern, replacement in REDACTION_PATTERNS:
        compiled_pattern = re.compile(pattern, re.IGNORECASE)
        matches = len(compiled_pattern.findall(redacted_text))
        if matches > 0:
            redacted_text = compiled_pattern.sub(replacement, redacted_text)
            redactions_made += matches

    if redactions_made > 0:
        logger.info(
            f"Applied {redactions_made} redactions for conversation {conversation_id}"
        )

    return redacted_text


class MockLlamaStackClient:
    """Mock client for testing redaction when Llama Stack service is not available."""

    def __init__(self):
        logger.warning(
            "Using mock Llama Stack client - Llama Stack service not available"
        )

    def models(self):
        class MockModels:
            def list(self):
                # Return a mock model for testing
                class MockModel:
                    def __init__(self):
                        self.identifier = "mock-model"
                        self.model_type = "llm"
                        self.provider_id = "mock"

                return [MockModel()]

        return MockModels()

    def shields(self):
        class MockShields:
            def list(self):
                return []  # No shields for testing

        return MockShields()


class RedactionEnabledClient:
    """Wrapper client that adds redaction capabilities."""

    def __init__(self, base_client):
        self.base_client = base_client

    def apply_redaction(self, query: str, attachments: list, conversation_id: str):
        """Apply redaction to query and attachments."""
        # Redact query
        redacted_query = apply_redaction(query, conversation_id)

        # Redact attachments
        redacted_attachments = []
        if attachments:
            for attachment in attachments:
                redacted_content = apply_redaction(attachment.content, conversation_id)
                # Create new attachment with redacted content
                redacted_attachment = type(attachment)(
                    attachment_type=attachment.attachment_type,
                    content_type=attachment.content_type,
                    content=redacted_content,
                )
                redacted_attachments.append(redacted_attachment)

        return redacted_query, redacted_attachments

    def __getattr__(self, name):
        """Delegate all other attributes to base client."""
        return getattr(self.base_client, name)


def get_llama_stack_client(
    llama_stack_config: LLamaStackConfiguration,
) -> RedactionEnabledClient:
    """Retrieve Llama stack client with redaction capabilities."""
    if llama_stack_config.use_as_library_client is True:
        if llama_stack_config.library_client_config_path is not None:
            logger.info("Using Llama stack as library client")
            try:
                client = LlamaStackAsLibraryClient(
                    llama_stack_config.library_client_config_path
                )
                client.initialize()
                return RedactionEnabledClient(client)
            except Exception as e:
                logger.error(f"Failed to initialize library client: {e}")
                logger.info("Falling back to mock client for redaction testing")
                return RedactionEnabledClient(MockLlamaStackClient())
        msg = "Configuration problem: library_client_config_path option is not set"
        logger.error(msg)
        raise Exception(msg)  # pylint: disable=broad-exception-raised

    logger.info("Using Llama stack running as a service")
<<<<<<< HEAD
    return LlamaStackClient(
        base_url=llama_stack_config.url, api_key=llama_stack_config.api_key
    )


async def get_async_llama_stack_client(
    llama_stack_config: LLamaStackConfiguration,
) -> AsyncLlamaStackClient:
    """Retrieve Async Llama stack client according to configuration."""
    if llama_stack_config.use_as_library_client is True:
        if llama_stack_config.library_client_config_path is not None:
            logger.info("Using Llama stack as library client")
            client = AsyncLlamaStackAsLibraryClient(
                llama_stack_config.library_client_config_path
            )
            await client.initialize()
            return client
        msg = "Configuration problem: library_client_config_path option is not set"
        logger.error(msg)
        # tisnik: use custom exception there - with cause etc.
        raise Exception(msg)  # pylint: disable=broad-exception-raised
    logger.info("Using Llama stack running as a service")
    return AsyncLlamaStackClient(
        base_url=llama_stack_config.url, api_key=llama_stack_config.api_key
    )
=======
    try:
        base_client = LlamaStackClient(
            base_url=llama_stack_config.url, api_key=llama_stack_config.api_key
        )
        return RedactionEnabledClient(base_client)
    except Exception as e:
        logger.error(f"Failed to connect to Llama stack service: {e}")
        logger.info("Using mock client for redaction testing")
        return RedactionEnabledClient(MockLlamaStackClient())
>>>>>>> c2a7397 (feat(redaction): Add configurable regex-based query and attachment redaction with full test coverag)
