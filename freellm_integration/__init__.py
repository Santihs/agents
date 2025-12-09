"""
FreeLLM Integration Package

This package provides a client for interacting with the apifreellm.com API,
following patterns similar to the OpenAI integration.
"""

from .client import FreeLLMClient
from .models import ChatMessage, ChatRequest, ChatResponse
from .exceptions import FreeLLMError, FreeLLMAPIError, FreeLLMConnectionError

__all__ = [
    "FreeLLMClient",
    "ChatMessage",
    "ChatRequest",
    "ChatResponse",
    "FreeLLMError",
    "FreeLLMAPIError",
    "FreeLLMConnectionError",
]
