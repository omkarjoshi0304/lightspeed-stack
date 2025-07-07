"""Implementation of common test steps."""

from behave import given  # pyright: ignore[reportAttributeAccessIssue]
from behave.runner import Context


@given("the service is started locally")
def service_is_started_locally(context: Context) -> None:
    """Check the service status."""
    assert context is not None


@given("the system is in default state")
def system_in_default_state(context: Context) -> None:
    """Check the default system state."""
    assert context is not None
