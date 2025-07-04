"""Utility functions for endpoint handlers."""

from fastapi import HTTPException, status

from configuration import AppConfig


def check_configuration_loaded(configuration: AppConfig) -> None:
    """Check that configuration is loaded and raise exception when it is not."""
    if configuration is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"response": "Configuration is not loaded"},
        )
