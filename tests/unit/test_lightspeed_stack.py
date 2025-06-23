"""Unit tests for functions defined in src/lightspeed_stack.py."""

from lightspeed_stack import create_argument_parser


def test_create_argument_parser():
    """Test for create_argument_parser function."""
    arg_parser = create_argument_parser()
    # nothing more to test w/o actual parsing is done
    assert arg_parser is not None
