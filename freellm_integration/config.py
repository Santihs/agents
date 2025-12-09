"""
Configuration for FreeLLM client.
"""

from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv(override=True)


class FreeLLMConfig(BaseModel):
    """Configuration settings for FreeLLM client."""

    base_url: str = Field(
        default="https://apifreellm.com",
        description="Base URL for the FreeLLM API",
    )

    timeout: float = Field(
        default=30.0,
        ge=1.0,
        description="Request timeout in seconds",
    )

    max_retries: int = Field(
        default=3,
        ge=0,
        description="Maximum number of retry attempts",
    )

    default_model: Optional[str] = Field(
        default=None,
        description="Default model to use if not specified",
    )

    default_temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Default temperature for requests",
    )

    default_max_tokens: Optional[int] = Field(
        default=None,
        gt=0,
        description="Default maximum tokens to generate",
    )

    max_conversation_history: int = Field(
        default=10,
        ge=1,
        description="Maximum number of messages to keep in history",
    )

    @classmethod
    def from_env(cls) -> "FreeLLMConfig":
        """
        Create configuration from environment variables.

        Environment variables:
            FREELLM_BASE_URL: Base URL for the API
            FREELLM_TIMEOUT: Request timeout in seconds
            FREELLM_MAX_RETRIES: Maximum retry attempts
            FREELLM_DEFAULT_MODEL: Default model name
            FREELLM_DEFAULT_TEMPERATURE: Default temperature
            FREELLM_DEFAULT_MAX_TOKENS: Default max tokens
            FREELLM_MAX_HISTORY: Maximum conversation history size
        """
        return cls(
            base_url=os.getenv("FREELLM_BASE_URL", "https://apifreellm.com"),
            timeout=float(os.getenv("FREELLM_TIMEOUT", "30.0")),
            max_retries=int(os.getenv("FREELLM_MAX_RETRIES", "3")),
            default_model=os.getenv("FREELLM_DEFAULT_MODEL"),
            default_temperature=float(os.getenv("FREELLM_DEFAULT_TEMPERATURE", "0.7")),
            default_max_tokens=int(os.getenv("FREELLM_DEFAULT_MAX_TOKENS")) if os.getenv("FREELLM_DEFAULT_MAX_TOKENS") else None,
            max_conversation_history=int(os.getenv("FREELLM_MAX_HISTORY", "10")),
        )
