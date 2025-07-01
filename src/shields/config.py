"""
Configuration support for redaction shields.
Allows loading patterns from configuration files.
"""

import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


def load_redaction_patterns_from_config(config: Any) -> Optional[List[Dict[str, str]]]:
    """
    Load redaction patterns from application configuration.

    Args:
        config: Application configuration object

    Returns:
        List of redaction patterns as dicts or None if not configured
    """
    try:
        # Case 1: redaction_patterns exist at root level
        if hasattr(config, "redaction_patterns") and config.redaction_patterns:
            # If items are already dicts, return directly
            if isinstance(config.redaction_patterns, list) and isinstance(
                config.redaction_patterns[0], dict
            ):
                return config.redaction_patterns

            # Else assume Pydantic models
            return [pattern.model_dump() for pattern in config.redaction_patterns]

        # Case 2: fallback - patterns under shields
        if hasattr(config, "shields") and hasattr(config.shields, "redaction_patterns"):
            if isinstance(config.shields.redaction_patterns, list) and isinstance(
                config.shields.redaction_patterns[0], dict
            ):
                return config.shields.redaction_patterns

            return [
                pattern.model_dump() for pattern in config.shields.redaction_patterns
            ]

        logger.info("No redaction patterns found in configuration, using defaults")
        return None

    except Exception as e:
        logger.error(f"Error loading redaction patterns from configuration: {e}")
        return None


def create_shield_with_config(config: Any):
    """
    Create a redaction shield with configuration.

    Args:
        config: Application configuration object

    Returns:
        Configured RedactionShield instance
    """
    from .redaction_shield import RedactionShield

    patterns = load_redaction_patterns_from_config(config)
    return RedactionShield(patterns)
