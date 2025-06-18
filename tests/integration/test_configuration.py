"""Integration tests for configuration loading and handling."""

import pytest
from configuration import configuration


@pytest.fixture
def configuration_filename() -> str:
    """Retrieve configuration file name to be used by integration tests."""
    return "tests/configuration/lightspeed-stack.yaml"


def test_default_configuration() -> None:
    """Test that exception is raised when configuration is not loaded."""
    cfg = configuration
    assert cfg is not None
    with pytest.raises(Exception, match="logic error: configuration is not loaded"):
        configuration.configuration


def test_loading_proper_configuration(configuration_filename: str) -> None:
    """Test the configuration loading."""
    cfg = configuration
    cfg.load_configuration(configuration_filename)

    # check if configuration is loaded
    assert cfg is not None

    # check that all configuration sections exist
    assert cfg.configuration is not None
    assert cfg.llama_stack_configuration is not None
    assert cfg.service_configuration is not None
    assert cfg.user_data_collection_configuration is not None

    # check 'configuration' section
    name = cfg.configuration.name
    assert name == "foo bar baz"

    # check 'service' section
    svc_config = cfg.service_configuration
    assert svc_config.host == "localhost"
    assert svc_config.auth_enabled is False
    assert svc_config.workers == 1
    assert svc_config.color_log is True
    assert svc_config.access_log is True

    # check 'llama_stack' section
    ls_config = cfg.llama_stack_configuration
    assert ls_config.use_as_library_client is False
    assert ls_config.url == "http://localhost:8321"
    assert ls_config.api_key == "xyzzy"

    # check 'user_data_collection' section
    udc_config = cfg.user_data_collection_configuration
    assert udc_config.feedback_disabled is False
    assert udc_config.feedback_storage == "/tmp/data/feedback"
