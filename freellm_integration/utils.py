"""
Utility functions for FreeLLM integration.
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime


def setup_logging(level: int = logging.INFO, format_string: Optional[str] = None) -> None:
    """
    Setup logging configuration for FreeLLM client.

    Args:
        level: Logging level (default: INFO)
        format_string: Custom format string for log messages
    """
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        level=level,
        format=format_string,
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def format_response_for_display(response: Dict[str, Any]) -> str:
    """
    Format API response for human-readable display.

    Args:
        response: Response dictionary from API

    Returns:
        Formatted string
    """
    lines = []
    lines.append("=" * 50)
    lines.append(f"Response at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 50)

    if "response" in response:
        lines.append(f"\n{response['response']}\n")

    if "model" in response and response["model"]:
        lines.append(f"Model: {response['model']}")

    if "usage" in response and response["usage"]:
        lines.append(f"Usage: {response['usage']}")

    lines.append("=" * 50)
    return "\n".join(lines)


def validate_message(message: str, max_length: int = 10000) -> bool:
    """
    Validate that a message is suitable for sending to the API.

    Args:
        message: Message to validate
        max_length: Maximum allowed message length

    Returns:
        True if valid, raises ValueError if not
    """
    if not message or not message.strip():
        raise ValueError("Message cannot be empty")

    if len(message) > max_length:
        raise ValueError(f"Message exceeds maximum length of {max_length} characters")

    return True


def truncate_message(message: str, max_length: int = 1000) -> str:
    """
    Truncate a message to a maximum length.

    Args:
        message: Message to truncate
        max_length: Maximum length

    Returns:
        Truncated message
    """
    if len(message) <= max_length:
        return message

    return message[:max_length - 3] + "..."


def parse_error_response(response_data: Dict[str, Any]) -> str:
    """
    Parse error response from API into human-readable message.

    Args:
        response_data: Error response data

    Returns:
        Formatted error message
    """
    if isinstance(response_data, dict):
        error = response_data.get("error", response_data.get("message", "Unknown error"))
        if isinstance(error, dict):
            return error.get("message", str(error))
        return str(error)
    return str(response_data)
