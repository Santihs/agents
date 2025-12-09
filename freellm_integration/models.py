"""
Data models for FreeLLM API requests and responses.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator


class ChatMessage(BaseModel):
    """Represents a chat message."""

    role: str = Field(description="Role of the message sender (e.g., 'user', 'assistant', 'system')")
    content: str = Field(description="Content of the message")

    @field_validator('role')
    @classmethod
    def validate_role(cls, v: str) -> str:
        """Validate that role is one of the allowed values."""
        allowed_roles = {'user', 'assistant', 'system'}
        if v not in allowed_roles:
            raise ValueError(f"Role must be one of {allowed_roles}")
        return v


class ChatRequest(BaseModel):
    """Request model for chat API."""

    message: str = Field(description="The message to send to the AI")
    model: Optional[str] = Field(default=None, description="Optional model to use")
    temperature: Optional[float] = Field(default=None, ge=0.0, le=2.0, description="Sampling temperature")
    max_tokens: Optional[int] = Field(default=None, gt=0, description="Maximum tokens to generate")

    @field_validator('temperature')
    @classmethod
    def validate_temperature(cls, v: Optional[float]) -> Optional[float]:
        """Validate temperature is in valid range."""
        if v is not None and not (0.0 <= v <= 2.0):
            raise ValueError("Temperature must be between 0.0 and 2.0")
        return v


class ChatResponse(BaseModel):
    """Response model from chat API."""

    response: str = Field(description="The AI's response")
    model: Optional[str] = Field(default=None, description="Model used for generation")
    usage: Optional[Dict[str, int]] = Field(default=None, description="Token usage information")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")

    class Config:
        extra = "allow"  # Allow additional fields from API response


class ConversationHistory(BaseModel):
    """Manages conversation history for chat sessions."""

    messages: List[ChatMessage] = Field(default_factory=list, description="List of messages in the conversation")
    max_history: int = Field(default=10, description="Maximum number of messages to keep")

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation history."""
        message = ChatMessage(role=role, content=content)
        self.messages.append(message)

        # Keep only the last max_history messages
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]

    def get_context(self) -> str:
        """Get conversation context as a formatted string."""
        return "\n".join([f"{msg.role}: {msg.content}" for msg in self.messages])

    def clear(self) -> None:
        """Clear conversation history."""
        self.messages = []
