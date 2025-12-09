"""
FreeLLM API Client

A Python client for interacting with the apifreellm.com API.
Follows patterns similar to OpenAI's client library.
"""

import httpx
import logging
from typing import Optional, Dict, Any, AsyncIterator
from contextlib import asynccontextmanager

from .models import ChatRequest, ChatResponse, ConversationHistory
from .exceptions import (
    FreeLLMAPIError,
    FreeLLMConnectionError,
    FreeLLMTimeoutError,
    FreeLLMValidationError,
)


logger = logging.getLogger(__name__)


class FreeLLMClient:
    """
    Client for interacting with the FreeLLM API.

    This client provides both synchronous and asynchronous methods
    for making requests to the apifreellm.com chat API.

    Example:
        >>> client = FreeLLMClient()
        >>> response = await client.chat("Hello AI!")
        >>> print(response.response)
    """

    BASE_URL = "https://apifreellm.com"
    CHAT_ENDPOINT = "/api/chat"
    DEFAULT_TIMEOUT = 30.0

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = 3,
        headers: Optional[Dict[str, str]] = None,
    ):
        """
        Initialize the FreeLLM client.

        Args:
            base_url: Base URL for the API (defaults to https://apifreellm.com)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts for failed requests
            headers: Additional headers to include in requests
        """
        self.base_url = base_url or self.BASE_URL
        self.timeout = timeout
        self.max_retries = max_retries
        self.default_headers = {
            "Content-Type": "application/json",
            **(headers or {}),
        }
        self._client: Optional[httpx.AsyncClient] = None
        self._conversation_history = ConversationHistory()

    @asynccontextmanager
    async def _get_client(self) -> AsyncIterator[httpx.AsyncClient]:
        """Get or create an async HTTP client."""
        if self._client is None:
            async with httpx.AsyncClient(
                timeout=self.timeout,
                headers=self.default_headers,
                follow_redirects=True,
            ) as client:
                yield client
        else:
            yield self._client

    async def __aenter__(self):
        """Async context manager entry."""
        self._client = httpx.AsyncClient(
            timeout=self.timeout,
            headers=self.default_headers,
            follow_redirects=True,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()
            self._client = None

    def _build_request_data(self, request: ChatRequest) -> Dict[str, Any]:
        """
        Build request data dictionary from ChatRequest model.

        Args:
            request: ChatRequest object

        Returns:
            Dictionary suitable for JSON serialization
        """
        data = {"message": request.message}

        # Add optional parameters if provided
        if request.model:
            data["model"] = request.model
        if request.temperature is not None:
            data["temperature"] = request.temperature
        if request.max_tokens is not None:
            data["max_tokens"] = request.max_tokens

        return data

    def _parse_response(self, response_data: Dict[str, Any]) -> ChatResponse:
        """
        Parse API response into ChatResponse model.

        Args:
            response_data: Raw response data from API

        Returns:
            ChatResponse object
        """
        # The API returns a simple response, adapt as needed
        # Based on the curl example, we expect a JSON response
        return ChatResponse(
            response=response_data.get("response", response_data.get("message", str(response_data))),
            model=response_data.get("model"),
            usage=response_data.get("usage"),
            metadata=response_data.get("metadata"),
        )

    async def chat(
        self,
        message: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        save_to_history: bool = False,
    ) -> ChatResponse:
        """
        Send a chat message to the FreeLLM API.

        Args:
            message: The message to send
            model: Optional model to use
            temperature: Sampling temperature (0.0 to 2.0)
            max_tokens: Maximum tokens to generate
            save_to_history: Whether to save this message to conversation history

        Returns:
            ChatResponse object containing the AI's response

        Raises:
            FreeLLMValidationError: If request parameters are invalid
            FreeLLMConnectionError: If connection to API fails
            FreeLLMTimeoutError: If request times out
            FreeLLMAPIError: If API returns an error
        """
        try:
            request = ChatRequest(
                message=message,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        except Exception as e:
            raise FreeLLMValidationError(f"Invalid request parameters: {e}")

        url = f"{self.base_url}{self.CHAT_ENDPOINT}"
        request_data = self._build_request_data(request)

        logger.debug(f"Sending request to {url}: {request_data}")

        try:
            async with self._get_client() as client:
                response = await client.post(url, json=request_data)

                # Check for HTTP errors
                if response.status_code >= 400:
                    error_msg = f"API returned error status {response.status_code}"
                    try:
                        error_data = response.json()
                        error_msg = f"{error_msg}: {error_data}"
                    except Exception:
                        error_msg = f"{error_msg}: {response.text}"

                    raise FreeLLMAPIError(
                        error_msg,
                        status_code=response.status_code,
                        response_data=response.json() if response.text else None,
                    )

                response_data = response.json()
                logger.debug(f"Received response: {response_data}")

                chat_response = self._parse_response(response_data)

                # Save to conversation history if requested
                if save_to_history:
                    self._conversation_history.add_message("user", message)
                    self._conversation_history.add_message("assistant", chat_response.response)

                return chat_response

        except httpx.TimeoutException as e:
            raise FreeLLMTimeoutError(f"Request timed out after {self.timeout}s: {e}")
        except httpx.ConnectError as e:
            raise FreeLLMConnectionError(f"Failed to connect to API: {e}")
        except FreeLLMAPIError:
            raise
        except Exception as e:
            raise FreeLLMAPIError(f"Unexpected error during API request: {e}")

    async def chat_with_context(
        self,
        message: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> ChatResponse:
        """
        Send a chat message with conversation history context.

        This method automatically includes previous conversation context
        and saves the new message to history.

        Args:
            message: The message to send
            model: Optional model to use
            temperature: Sampling temperature (0.0 to 2.0)
            max_tokens: Maximum tokens to generate

        Returns:
            ChatResponse object containing the AI's response
        """
        # Build message with context
        context = self._conversation_history.get_context()
        full_message = f"{context}\nuser: {message}" if context else message

        return await self.chat(
            message=full_message,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            save_to_history=True,
        )

    def clear_history(self) -> None:
        """Clear the conversation history."""
        self._conversation_history.clear()

    def get_history(self) -> ConversationHistory:
        """Get the current conversation history."""
        return self._conversation_history

    async def close(self) -> None:
        """Close the HTTP client connection."""
        if self._client:
            await self._client.aclose()
            self._client = None
