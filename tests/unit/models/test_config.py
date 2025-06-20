"""Unit tests for functions defined in src/models/config.py."""

import json
import pytest

from models.config import (
    Configuration,
    LLamaStackConfiguration,
    ServiceConfiguration,
    UserDataCollection,
)


def test_service_configuration_constructor() -> None:
    """Test the ServiceConfiguration constructor."""
    s = ServiceConfiguration()
    assert s is not None

    assert s.host == "localhost"
    assert s.port == 8080
    assert s.auth_enabled is False
    assert s.workers == 1
    assert s.color_log is True
    assert s.access_log is True


def test_service_configuration_port_value() -> None:
    """Test the ServiceConfiguration port value validation."""
    with pytest.raises(ValueError, match="Port value should not be negative"):
        ServiceConfiguration(port=-1)

    with pytest.raises(ValueError, match="Port value should be less than 65536"):
        ServiceConfiguration(port=100000)


def test_service_configuration_workers_value() -> None:
    """Test the ServiceConfiguration workers value validation."""
    with pytest.raises(ValueError, match="Workers must be set to at least 1"):
        ServiceConfiguration(workers=-1)


def test_llama_stack_configuration_constructor() -> None:
    """Test the LLamaStackConfiguration constructor."""
    llama_stack_configuration = LLamaStackConfiguration(
        use_as_library_client=True, library_client_config_path="foo"
    )
    assert llama_stack_configuration is not None

    llama_stack_configuration = LLamaStackConfiguration(
        use_as_library_client=False, url="http://localhost"
    )
    assert llama_stack_configuration is not None

    llama_stack_configuration = LLamaStackConfiguration(url="http://localhost")
    assert llama_stack_configuration is not None

    llama_stack_configuration = LLamaStackConfiguration(
        use_as_library_client=False, url="http://localhost", api_key="foo"
    )
    assert llama_stack_configuration is not None


def test_llama_stack_wrong_configuration_constructor_no_url() -> None:
    """Test the LLamaStackConfiguration constructor."""
    with pytest.raises(
        ValueError,
        match="LLama stack URL is not specified and library client mode is not specified",
    ):
        LLamaStackConfiguration()


def test_llama_stack_wrong_configuration_constructor_library_mode_off() -> None:
    """Test the LLamaStackConfiguration constructor."""
    with pytest.raises(
        ValueError,
        match="LLama stack URL is not specified and library client mode is not enabled",
    ):
        LLamaStackConfiguration(use_as_library_client=False)


def test_llama_stack_wrong_configuration_no_config_file() -> None:
    """Test the LLamaStackConfiguration constructor."""
    with pytest.raises(
        ValueError,
        match="LLama stack library client mode is enabled but a configuration file path is not specified",
    ):
        LLamaStackConfiguration(use_as_library_client=True)


def test_user_data_collection_feedback_enabled() -> None:
    """Test the UserDataCollection constructor for feedback."""
    # correct configuration
    cfg = UserDataCollection(feedback_disabled=True, feedback_storage=None)
    assert cfg is not None
    assert cfg.feedback_disabled is True
    assert cfg.feedback_storage is None


def test_user_data_collection_feedback_disabled() -> None:
    """Test the UserDataCollection constructor for feedback."""
    # incorrect configuration
    with pytest.raises(
        ValueError,
        match="feedback_storage is required when feedback is enabled",
    ):
        UserDataCollection(feedback_disabled=False, feedback_storage=None)


def test_user_data_collection_transcripts_enabled() -> None:
    """Test the UserDataCollection constructor for transcripts."""
    # correct configuration
    cfg = UserDataCollection(transcripts_disabled=True, transcripts_storage=None)
    assert cfg is not None


def test_user_data_collection_transcripts_disabled() -> None:
    """Test the UserDataCollection constructor for transcripts."""
    # incorrect configuration
    with pytest.raises(
        ValueError,
        match="transcripts_storage is required when transcripts is enabled",
    ):
        UserDataCollection(transcripts_disabled=False, transcripts_storage=None)


def test_dump_configuration(tmp_path) -> None:
    """Test the ability to dump configuration."""
    cfg = Configuration(
        name="test_name",
        service=ServiceConfiguration(),
        llama_stack=LLamaStackConfiguration(
            use_as_library_client=True, library_client_config_path="foo"
        ),
        user_data_collection=UserDataCollection(
            feedback_disabled=True, feedback_storage=None
        ),
    )
    assert cfg is not None
    dump_file = tmp_path / "test.json"
    cfg.dump(dump_file)

    with open(dump_file, "r", encoding="utf-8") as fin:
        content = json.load(fin)
        assert content is not None
        assert "name" in content
        assert "service" in content
        assert "llama_stack" in content
        assert "user_data_collection" in content
