from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel
from config import settings

# Local Ollama — no API key needed
_ollama_client = AsyncOpenAI(
    base_url=settings.ollama_base_url,
    api_key="ollama",
)

_groq_client = AsyncOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=settings.groq_api_key,
)

_openrouter_client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.openrouter_api_key,
)

# gemma3:4b — lightweight local model, used for guardrails
ollama_guardrail_model = OpenAIChatCompletionsModel(
    model="gemma3:4b",
    openai_client=_ollama_client,
)

# General-purpose Groq model — tool calling supported
groq_model = OpenAIChatCompletionsModel(
    model="qwen/qwen3-32b",
    openai_client=_groq_client,
)

# OpenRouter general model — structured outputs + tool calling
openrouter_model = OpenAIChatCompletionsModel(
    model="qwen/qwen3-32b",
    openai_client=_openrouter_client,
)

# OpenRouter writer model — gpt-4o-mini supports streaming + json_schema simultaneously
openrouter_writer_model = OpenAIChatCompletionsModel(
    model="openai/gpt-4o-mini",
    openai_client=_openrouter_client,
)
