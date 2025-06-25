"""Code to be called before and after certain events during testing.

Currently four events have been registered:
1. before_all
2. before_feature
3. before_scenario
4. after_scenario
"""

from behave.model import Scenario
from behave.runner import Context

try:
    import os  # noqa: F401
except ImportError as e:
    print("Warning: unable to import module:", e)


def before_all(context: Context) -> None:
    """Run before and after the whole shooting match."""


def before_scenario(context: Context, scenario: Scenario) -> None:
    """Run before each scenario is run."""
    if "skip" in scenario.effective_tags:
        scenario.skip("Marked with @skip")
        return
    if "local" in scenario.effective_tags and not context.local:
        scenario.skip("Marked with @local")
        return


def after_scenario(context: Context, scenario: Scenario) -> None:
    """Run after each scenario is run."""


def before_feature(context: Context, feature: Scenario) -> None:
    """Run before each feature file is exercised."""
