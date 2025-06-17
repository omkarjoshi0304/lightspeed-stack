"""Unit tests for functions defined in src/configuration.py."""

import pytest
from configuration import AppConfig


def test_default_configuration() -> None:
    cfg = AppConfig()
    assert cfg is not None

    # configuration is not loaded
    with pytest.raises(Exception, match="logic error: configuration is not loaded"):
        # try to read property
        cfg.configuration

    with pytest.raises(Exception, match="logic error: configuration is not loaded"):
        # try to read property
        cfg.llama_stack_configuration

    with pytest.raises(Exception, match="logic error: configuration is not loaded"):
        # try to read property
        cfg.user_data_collection_configuration


def test_configuration_is_singleton() -> None:
    cfg1 = AppConfig()
    cfg2 = AppConfig()
    assert cfg1 == cfg2


def test_init_from_dict() -> None:
    config_dict = {
        "name": "foo",
        "service": {
            "host": "localhost",
            "port": 8080,
            "auth_enabled": False,
            "workers": 1,
            "color_log": True,
            "access_log": True,
        },
        "llama_stack": {
            "api_key": "xyzzy",
            "url": "http://x.y.com:1234",
            "use_as_library_client": False,
        },
        "user_data_collection": {
            "feedback_disabled": True,
        },
    }
    cfg = AppConfig()
    cfg.init_from_dict(config_dict)

    # check for all subsections
    assert cfg.configuration is not None
    assert cfg.llama_stack_configuration is not None
    assert cfg.service_configuration is not None
    assert cfg.user_data_collection_configuration is not None

    # check for configuration subsection
    assert cfg.configuration.name == "foo"

    # check for llama_stack_configuration subsection
    assert cfg.llama_stack_configuration.api_key == "xyzzy"
    assert cfg.llama_stack_configuration.url == "http://x.y.com:1234"
    assert cfg.llama_stack_configuration.use_as_library_client is False

    # check for service_configuration subsection
    assert cfg.service_configuration.host == "localhost"
    assert cfg.service_configuration.port == 8080
    assert cfg.service_configuration.auth_enabled is False
    assert cfg.service_configuration.workers == 1
    assert cfg.service_configuration.color_log is True
    assert cfg.service_configuration.access_log is True

    # check for user data collection subsection
    assert cfg.user_data_collection_configuration.feedback_disabled is True


def test_load_proper_configuration(tmpdir) -> None:
    cfg_filename = tmpdir / "config.yaml"
    with open(cfg_filename, "w") as fout:
        fout.write(
            """
name: foo bar baz
service:
  host: localhost
  port: 8080
  auth_enabled: false
  workers: 1
  color_log: true
  access_log: true
llama_stack:
  use_as_library_client: false
  url: http://localhost:8321
  api_key: xyzzy
user_data_collection:
  feedback_disabled: true
        """
        )

    cfg = AppConfig()
    cfg.load_configuration(cfg_filename)
    assert cfg.configuration is not None
    assert cfg.llama_stack_configuration is not None
    assert cfg.service_configuration is not None
    assert cfg.user_data_collection_configuration is not None
