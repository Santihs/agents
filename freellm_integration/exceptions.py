"""
Custom exceptions for FreeLLM integration.
"""


class FreeLLMError(Exception):
    """Base exception for all FreeLLM related errors."""
    pass


class FreeLLMAPIError(FreeLLMError):
    """Exception raised when the FreeLLM API returns an error."""

    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(message)


class FreeLLMConnectionError(FreeLLMError):
    """Exception raised when connection to FreeLLM API fails."""
    pass


class FreeLLMTimeoutError(FreeLLMError):
    """Exception raised when request to FreeLLM API times out."""
    pass


class FreeLLMValidationError(FreeLLMError):
    """Exception raised when request validation fails."""
    pass
