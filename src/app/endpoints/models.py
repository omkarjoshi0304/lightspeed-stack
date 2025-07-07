"""Handler for REST API call to provide info."""

import logging
from typing import Any

from llama_stack_client import APIConnectionError
from fastapi import APIRouter, HTTPException, Request, status

from client import get_llama_stack_client
from configuration import configuration
from models.responses import ModelsResponse
from utils.endpoints import check_configuration_loaded

logger = logging.getLogger(__name__)
router = APIRouter(tags=["models"])


models_responses: dict[int | str, dict[str, Any]] = {
    200: {
        "models": [
            {
                "identifier": "all-MiniLM-L6-v2",
                "metadata": {"embedding_dimension": 384},
                "api_model_type": "embedding",
                "provider_id": "ollama",
                "provider_resource_id": "all-minilm:latest",
                "type": "model",
                "model_type": "embedding",
            },
            {
                "identifier": "llama3.2:3b-instruct-fp16",
                "metadata": {},
                "api_model_type": "llm",
                "provider_id": "ollama",
                "provider_resource_id": "llama3.2:3b-instruct-fp16",
                "type": "model",
                "model_type": "llm",
            },
        ]
    },
    503: {"description": "Connection to Llama Stack is broken"},
}


@router.get("/models", responses=models_responses)
def models_endpoint_handler(_request: Request) -> ModelsResponse:
    """Handle requests to the /models endpoint."""
    check_configuration_loaded(configuration)

    llama_stack_configuration = configuration.llama_stack_configuration
    logger.info("LLama stack config: %s", llama_stack_configuration)

    try:
        # try to get Llama Stack client
        client = get_llama_stack_client(llama_stack_configuration)
        # retrieve models
        models = client.models.list()
        m = [dict(m) for m in models]
        return ModelsResponse(models=m)
    # connection to Llama Stack server
    except APIConnectionError as e:
        logger.error("Unable to connect to Llama Stack: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "response": "Unable to connect to Llama Stack",
                "cause": str(e),
            },
        ) from e
    # any other exception that can occur during model listing
    except Exception as e:
        logger.error("Unable to retrieve list of models: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "response": "Unable to retrieve list of models",
                "cause": str(e),
            },
        ) from e
