# FreeLLM Integration

A professional Python client for interacting with the [apifreellm.com](https://apifreellm.com) API, designed following OpenAI library patterns and best practices.

## Features

- **Async/await support**: Built with modern Python async patterns
- **Type safety**: Full Pydantic model validation
- **Error handling**: Comprehensive exception hierarchy
- **Conversation history**: Built-in context management
- **Configuration**: Environment-based configuration
- **Logging**: Structured logging support
- **Context managers**: Proper resource management

## Installation

This package is part of the agents-mcp project. No additional installation required.

## Quick Start

### Basic Usage

```python
import asyncio
from freellm_integration import FreeLLMClient

async def main():
    # Create a client
    async with FreeLLMClient() as client:
        # Send a simple message
        response = await client.chat("Hello AI!")
        print(response.response)

asyncio.run(main())
```

### With Conversation History

```python
async def conversation_example():
    async with FreeLLMClient() as client:
        # First message
        response1 = await client.chat_with_context("My name is Alice")
        print(response1.response)

        # Follow-up (remembers context)
        response2 = await client.chat_with_context("What's my name?")
        print(response2.response)

        # Clear history when needed
        client.clear_history()

asyncio.run(conversation_example())
```

### Advanced Configuration

```python
from freellm_integration import FreeLLMClient
from freellm_integration.config import FreeLLMConfig

# Custom configuration
config = FreeLLMConfig(
    base_url="https://apifreellm.com",
    timeout=60.0,
    max_retries=5,
    default_temperature=0.8,
)

client = FreeLLMClient(
    base_url=config.base_url,
    timeout=config.timeout,
    max_retries=config.max_retries,
)

response = await client.chat(
    message="Explain quantum computing",
    temperature=0.7,
    max_tokens=500,
)
```

## Architecture

### Package Structure

```
freellm_integration/
├── __init__.py          # Package exports
├── client.py            # Main FreeLLMClient class
├── models.py            # Pydantic data models
├── config.py            # Configuration management
├── exceptions.py        # Custom exception hierarchy
├── utils.py             # Utility functions
└── README.md            # This file
```

### Key Components

#### FreeLLMClient

The main client class following async patterns:

- `chat()`: Send a single message
- `chat_with_context()`: Send message with conversation history
- `clear_history()`: Clear conversation context
- `close()`: Clean up resources

#### Models

Type-safe data models using Pydantic:

- `ChatRequest`: Request parameters
- `ChatResponse`: API response
- `ChatMessage`: Individual message
- `ConversationHistory`: Context management

#### Exceptions

Hierarchical exception structure:

- `FreeLLMError`: Base exception
- `FreeLLMAPIError`: API-level errors
- `FreeLLMConnectionError`: Network errors
- `FreeLLMTimeoutError`: Timeout errors
- `FreeLLMValidationError`: Input validation errors

## Environment Configuration

Set these environment variables in your `.env` file:

```bash
# Optional: Override default API URL
FREELLM_BASE_URL=https://apifreellm.com

# Optional: Request timeout in seconds
FREELLM_TIMEOUT=30.0

# Optional: Maximum retry attempts
FREELLM_MAX_RETRIES=3

# Optional: Default model to use
FREELLM_DEFAULT_MODEL=gpt-4

# Optional: Default temperature
FREELLM_DEFAULT_TEMPERATURE=0.7

# Optional: Default max tokens
FREELLM_DEFAULT_MAX_TOKENS=1000

# Optional: Maximum conversation history size
FREELLM_MAX_HISTORY=10
```

## Error Handling

```python
from freellm_integration import (
    FreeLLMClient,
    FreeLLMAPIError,
    FreeLLMConnectionError,
    FreeLLMTimeoutError,
)

async def robust_example():
    client = FreeLLMClient(timeout=10.0)

    try:
        response = await client.chat("Hello!")
        print(response.response)

    except FreeLLMTimeoutError:
        print("Request timed out")
    except FreeLLMConnectionError:
        print("Could not connect to API")
    except FreeLLMAPIError as e:
        print(f"API error: {e}")
    finally:
        await client.close()
```

## Integration with Agents SDK

This client is designed to work seamlessly with the Agents SDK:

```python
from agents import Agent, Runner
from freellm_integration import FreeLLMClient

async def agent_integration():
    async with FreeLLMClient() as client:
        # Use FreeLLM for specific tasks
        response = await client.chat("Generate a creative story")

        # Pass to agent for further processing
        agent = Agent(
            name="story_editor",
            instructions="Edit and improve the story",
        )

        result = await Runner.run(agent, response.response)
        print(result.final_output)
```

## Best Practices

1. **Use async context managers**: Always use `async with` to ensure proper cleanup
2. **Handle exceptions**: Catch specific exceptions for better error handling
3. **Validate inputs**: Use Pydantic models for type safety
4. **Configure via environment**: Use `.env` files for configuration
5. **Clear history**: Call `clear_history()` when starting new conversations
6. **Set timeouts**: Configure appropriate timeouts for your use case

## API Reference

### FreeLLMClient

```python
class FreeLLMClient:
    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        headers: Optional[Dict[str, str]] = None,
    )

    async def chat(
        self,
        message: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        save_to_history: bool = False,
    ) -> ChatResponse

    async def chat_with_context(
        self,
        message: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> ChatResponse

    def clear_history(self) -> None
    async def close(self) -> None
```

## Testing

See the example notebook in `freellm_integration/examples/usage_example.ipynb` for interactive examples.

## Contributing

This integration follows these architectural principles:

1. **Separation of Concerns**: Models, client logic, and configuration are separate
2. **Dependency Injection**: Configuration can be injected for testing
3. **Single Responsibility**: Each module has a clear, focused purpose
4. **Open/Closed**: Extensible without modifying core code
5. **Interface Segregation**: Clean, minimal public API

## License

Part of the agents-mcp project.
