# CONTRIBUTING

<!-- the following line is used by tool to autogenerate Table of Content when the document is changed -->
<!-- vim-markdown-toc GFM -->

* [TLDR;](#tldr)
* [Prerequisities](#prerequisities)
    * [Tooling installation](#tooling-installation)
* [Setting up your development environment](#setting-up-your-development-environment)
* [Definition of Done](#definition-of-done)
    * [A deliverable is to be considered “done” when](#a-deliverable-is-to-be-considered-done-when)
* [Automation](#automation)
    * [Pre-commit hook settings](#pre-commit-hook-settings)
    * [Code coverage measurement](#code-coverage-measurement)
    * [Type hints checks](#type-hints-checks)
    * [Linters](#linters)
    * [Security checks](#security-checks)
* [Testing](#testing)
    * [Tips and hints for developing unit tests](#tips-and-hints-for-developing-unit-tests)
        * [Patching](#patching)
        * [Verifying that some exception is thrown](#verifying-that-some-exception-is-thrown)
        * [Checking what was printed and logged to stdout or stderr by the tested code](#checking-what-was-printed-and-logged-to-stdout-or-stderr-by-the-tested-code)
* [Code style](#code-style)
    * [Docstrings style](#docstrings-style)

<!-- vim-markdown-toc -->

## TLDR;

1. Create your own fork of the repo
2. Make changes to the code in your fork
3. Run unit tests and integration tests
4. Check the code with linters
5. Submit PR from your fork to main branch of the project repo


## Prerequisities

- git
- Python 3.12 or 3.13
- pip

The development requires at least [Python 3.12](https://docs.python.org/3/whatsnew/3.12.html) due to significant improvement on performance, optimizations which benefit modern ML, AI, LLM, NL stacks, and improved asynchronous processing capabilities. It is also possible to use Python 3.13.



### Tooling installation

1. `pip install --user pdm`
1. `pdm --version` -- should return no error



## Setting up your development environment

```bash
# clone your fork
git clone https://github.com/YOUR-GIT-PROFILE/lightspeed-stack.git

# move into the directory
cd lightspeed-stack

# setup your devel environment with pdm
pdm install -G dev

# Now you can run test commands trough make targets, or prefix the rest of commands with `pdm run`, eg. `pdm run make test`

# run unit tests
make unit-tests

# run integration tests
make integration-tests

# code formatting
# (this is also run automatically as part of pre-commit hook if configured)
make format

# code style and docstring style
# (this is also run automatically as part of pre-commit hook if configured)
make verify

# check type hints
# (this is also run automatically as part of pre-commit hook)
make check-types
```

Happy hacking!


## Definition of Done

### A deliverable is to be considered “done” when

* Code is complete, commented, and merged to the relevant release branch
* User facing documentation written (where relevant)
* Acceptance criteria in the related Jira ticket (where applicable) are verified and fulfilled
* Pull request title+commit includes Jira number
* Changes are covered by unit tests that run cleanly in the CI environment (where relevant)
* Changes are covered by integration tests that run cleanly in the CI environment (where relevant)
* Changes are covered by E2E tests that run cleanly in the CI environment (where relevant)
* All linters are running cleanly in the CI environment
* Code changes reviewed by at least one peer
* Code changes acked by at least one project owner

## Automation

### Pre-commit hook settings

It is possible to run formatters and linters automatically for all commits. You just need
to copy file `hooks/pre-commit` into subdirectory `.git/hooks/`. It must be done manually
because the copied file is an executable script (so from GIT point of view it is unsafe
to enable it automatically).


### Code coverage measurement

During testing, code coverage is measured. If the coverage is below defined threshold (see `pyproject.toml` settings for actual value stored in section `[tool.coverage.report]`), tests will fail. We measured and checked code coverage in order to be able to develop software with high quality.

Code coverage reports are generated in JSON and also in format compatible with [_JUnit_ test automation framework](https://junit.org/junit5/). It is also possible to start `make coverage-report` to generate code coverage reports in the form of interactive HTML pages. These pages are stored in the `htmlcov` subdirectory. Just open the index page from this subdirectory in your web browser.

### Type hints checks

It is possible to check if type hints added into the code are correct and whether assignments, function calls etc. use values of the right type. This check is invoked by following command:

```
make check-types
```

Please note that type hints check might be very slow on the first run.
Subsequent runs are much faster thanks to the cache that Mypy uses. This check
is part of a CI job that verifies sources.


### Linters

_Black_, _Ruff_, Pyright, and _Pylint_ tools are used as linters. There are a bunch of linter rules enabled for this repository. All of them are specified in `pyproject.toml`, such us in sections `[tool.ruff]` and `[tool.pylint."MESSAGES CONTROL"]`. Some specific rules can be disabled using `ignore` parameter (empty now).

List of all _Ruff_ rules recognized by Ruff can be retrieved by:


```
ruff linter
```

Description of all _Ruff_ rules are available on https://docs.astral.sh/ruff/rules/

Ruff rules can be disabled in source code (for given line or block) by using special `noqa` comment line. For example:

```python
# noqa: E501
```

List of all _Pylint_ rules can be retrieved by:

```
pylint --list-msgs
```

Description of all rules are available on https://pylint.readthedocs.io/en/latest/user_guide/checkers/features.html

To disable _Pylint_ rule in source code, the comment line in following format can be used:

```python
# pylint: disable=C0415
```



### Security checks

Static security check is performed by _Bandit_ tool. The check can be started by using:

```
make security-check
```
## Testing

Two groups of software tests are used in this repository, each group from the test suite having different granularity. These groups are designed to represent three layers:

1. Unit Tests
1. Integration Tests

Unit tests followed by integration and e2e tests can be started by using the following command:

```
make test
```

It is also possible to run just one selected group of tests:

```
make test-unit                 Run the unit tests
make test-integration          Run integration tests tests
make test-e2e                  Run end to end tests
```

All tests are based on the [Pytest framework](https://docs.pytest.org/en/) and code coverage is measured by the plugin [pytest-cov](https://github.com/pytest-dev/pytest-cov). For mocking and patching, the [unittest framework](https://docs.python.org/3/library/unittest.html) is used.

Currently code coverage threshold for integration tests is set to 60%. This value is specified directly in Makefile, because the coverage threshold is different from threshold required for unit tests.

As specified in Definition of Done, new changes need to be covered by tests.



### Tips and hints for developing unit tests

#### Patching

**WARNING**:
Since tests are executed using Pytest, which relies heavily on fixtures,
we discourage use of `patch` decorators in all test code, as they may interact with one another.

It is possible to use patching inside the test implementation as a context manager:

```python
def test_xyz():
    with patch("ols.config", new=Mock()):
        ...
        ...
        ...
```

- `new=` allow us to use different function or class
- `return_value=` allow us to define return value (no mock will be called)


#### Verifying that some exception is thrown

Sometimes it is needed to test whether some exception is thrown from a tested function or method. In this case `pytest.raises` can be used:


```python
def test_conversation_cache_wrong_cache(invalid_cache_type_config):
    """Check if wrong cache env.variable is detected properly."""
    with pytest.raises(ValueError):
        CacheFactory.conversation_cache(invalid_cache_type_config)
```

It is also possible to check if the exception is thrown with the expected message. The message (or its part) is written as regexp:

```python
def test_constructor_no_provider():
    """Test that constructor checks for provider."""
    # we use bare Exception in the code, so need to check
    # message, at least
    with pytest.raises(Exception, match="ERROR: Missing provider"):
        load_llm(provider=None)
```

#### Checking what was printed and logged to stdout or stderr by the tested code

It is possible to capture stdout and stderr by using standard fixture `capsys`:

```python
def test_foobar(capsys):
    """Test the foobar function that prints to stdout."""
    foobar("argument1", "argument2")

    # check captured log output
    captured_out = capsys.readouterr().out
    assert captured_out == "Output printed by foobar function"
    captured_err = capsys.readouterr().err
    assert captured_err == ""
```

Capturing logs:

```python
@patch.dict(os.environ, {"LOG_LEVEL": "INFO"})
def test_logger_show_message_flag(mock_load_dotenv, capsys):
    """Test logger set with show_message flag."""
    logger = Logger(logger_name="foo", log_level=logging.INFO, show_message=True)
    logger.logger.info("This is my debug message")

    # check captured log output
    # the log message should be captured
    captured_out = capsys.readouterr().out
    assert "This is my debug message" in captured_out

    # error output should be empty
    captured_err = capsys.readouterr().err
    assert captured_err == ""
```


## Code style

### Docstrings style
We are using [Google's docstring style](https://google.github.io/styleguide/pyguide.html).

Here is simple example:
```python
def function_with_pep484_type_annotations(param1: int, param2: str) -> bool:
    """Example function with PEP 484 type annotations.
    
    Args:
        param1: The first parameter.
        param2: The second parameter.
    
    Returns:
        The return value. True for success, False otherwise.
    
    Raises:
        ValueError: If the first parameter does not contain proper model name
    """
```

For further guidance, see the rest of our codebase, or check sources online. There are many, eg. [this one](https://gist.github.com/redlotus/3bc387c2591e3e908c9b63b97b11d24e).


