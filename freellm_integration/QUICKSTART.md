# FreeLLM Integration - Quick Start Guide

## 📁 Project Structure

```
freellm_integration/
├── __init__.py              # Package initialization & exports
├── client.py                # Main FreeLLMClient implementation
├── models.py                # Pydantic data models
├── config.py                # Configuration management
├── exceptions.py            # Custom exception hierarchy
├── utils.py                 # Utility functions
├── test_client.py           # Test suite
├── usage_example.ipynb      # Interactive examples
├── requirements.txt         # Dependencies
├── README.md                # Full documentation
└── QUICKSTART.md           # This file
```

## 🚀 Installation

The package uses the following dependencies (already in your project):

```bash
pip install httpx pydantic python-dotenv
```

Or install from requirements:

```bash
cd freellm_integration
pip install -r requirements.txt
```

## 💡 Simple Usage

### 1. Basic Example (30 seconds)

```python
import asyncio
from freellm_integration import FreeLLMClient

async def main():
    async with FreeLLMClient() as client:
        response = await client.chat("Hello AI!")
        print(response.response)

asyncio.run(main())
```

### 2. With Jupyter Notebook

```python
from freellm_integration import FreeLLMClient

# In Jupyter, you can use await directly
async with FreeLLMClient() as client:
    response = await client.chat("Hello AI!")
    print(response.response)
```

### 3. One-Liner Test

```python
import asyncio
from freellm_integration import FreeLLMClient

# Test the API in one line
asyncio.run(FreeLLMClient().chat("Test").__await__().__next__().response)
```

## 🎯 Common Use Cases

### Simple Question & Answer

```python
async with FreeLLMClient() as client:
    response = await client.chat("What is Python?")
    print(response.response)
```

### Creative Writing

```python
async with FreeLLMClient() as client:
    response = await client.chat(
        "Write a haiku about coding",
        temperature=0.9  # Higher = more creative
    )
    print(response.response)
```

### Conversation with Memory

```python
async with FreeLLMClient() as client:
    # First message
    r1 = await client.chat_with_context("My name is Alice")

    # Second message (remembers context)
    r2 = await client.chat_with_context("What's my name?")
    print(r2.response)  # Should mention "Alice"
```

### Error Handling

```python
from freellm_integration import FreeLLMAPIError

async with FreeLLMClient() as client:
    try:
        response = await client.chat("Hello")
        print(response.response)
    except FreeLLMAPIError as e:
        print(f"Error: {e}")
```

## 🧪 Testing

Run the test suite:

```bash
cd freellm_integration
python test_client.py
```

## 📚 Examples

### Run the Interactive Notebook

```bash
cd freellm_integration
jupyter notebook usage_example.ipynb
```

The notebook includes 8 complete examples:
1. Basic chat
2. Chat with parameters
3. Conversation with context
4. Error handling
5. Custom configuration
6. Agents SDK integration
7. Batch processing
8. API connection testing

## 🔧 Configuration (Optional)

Create a `.env` file in your project root:

```bash
# Optional: Override defaults
FREELLM_BASE_URL=https://apifreellm.com
FREELLM_TIMEOUT=30.0
FREELLM_MAX_RETRIES=3
FREELLM_DEFAULT_TEMPERATURE=0.7
```

Load configuration:

```python
from freellm_integration.config import FreeLLMConfig

config = FreeLLMConfig.from_env()
client = FreeLLMClient(
    base_url=config.base_url,
    timeout=config.timeout
)
```

## 🏗️ Architecture Overview

### Design Patterns Used

1. **Async/Await Pattern**: Modern async Python for efficient I/O
2. **Context Managers**: Proper resource cleanup with `async with`
3. **Dependency Injection**: Configuration can be injected for testing
4. **Single Responsibility**: Each module has one clear purpose
5. **Type Safety**: Pydantic models for runtime validation
6. **Error Hierarchy**: Specific exceptions for different error types

### Key Components

```python
FreeLLMClient        # Main client (like openai.OpenAI)
ChatRequest          # Request model (like OpenAI's messages)
ChatResponse         # Response model (like OpenAI's completion)
FreeLLMConfig        # Configuration (like OpenAI's settings)
FreeLLMError         # Base exception (like OpenAI's APIError)
```

## 🔗 Integration Examples

### With Agents SDK

```python
from agents import Agent, Runner
from freellm_integration import FreeLLMClient

async def workflow():
    async with FreeLLMClient() as llm:
        # Step 1: Generate with FreeLLM
        response = await llm.chat("Generate project ideas")

        # Step 2: Process with Agent
        agent = Agent(name="analyzer", instructions="Analyze ideas")
        result = await Runner.run(agent, response.response)

        return result
```

### With MCP Server Pattern

The client follows the same patterns as the MCP examples in `6_mcp/`:

- `accounts_client.py` → Shows MCP client pattern
- `accounts_server.py` → Shows MCP server pattern
- `freellm_integration/` → Shows REST API client pattern

## 📊 API Reference

### FreeLLMClient

```python
class FreeLLMClient:
    def __init__(
        base_url: str = "https://apifreellm.com",
        timeout: float = 30.0,
        max_retries: int = 3
    )

    async def chat(
        message: str,
        model: str = None,
        temperature: float = None,
        max_tokens: int = None
    ) -> ChatResponse

    async def chat_with_context(
        message: str,
        ...
    ) -> ChatResponse

    def clear_history() -> None
    async def close() -> None
```

## 🆘 Troubleshooting

### Import Error

```python
# Make sure you're in the right directory
import sys
sys.path.append('..')  # If in a subfolder
```

### Connection Error

```python
# Check if API is accessible
from freellm_integration import FreeLLMClient

async with FreeLLMClient(timeout=10.0) as client:
    response = await client.chat("Test")
    print("✅ Connected!")
```

### Module Not Found

```bash
# Install dependencies
pip install httpx pydantic python-dotenv
```

## 📖 Next Steps

1. ✅ Run `test_client.py` to verify everything works
2. ✅ Open `usage_example.ipynb` for interactive examples
3. ✅ Read `README.md` for complete documentation
4. ✅ Try integrating with your existing code

## 🤝 Following Best Practices

This implementation follows senior-level software engineering practices:

- ✅ Type hints everywhere
- ✅ Pydantic validation
- ✅ Async/await patterns
- ✅ Context managers
- ✅ Custom exceptions
- ✅ Comprehensive documentation
- ✅ Test coverage
- ✅ Configuration management
- ✅ Clean separation of concerns
- ✅ OpenAI-like API design

---

**Ready to use?** Start with the basic example above or open `usage_example.ipynb`!
