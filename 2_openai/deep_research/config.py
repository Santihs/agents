from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolve .env from the project root regardless of the working directory
_ENV_FILE = Path(__file__).parent.parent.parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # API keys — required, fail fast at startup if missing
    groq_api_key: str
    openrouter_api_key: str

    # SendGrid — optional: only validated at runtime when deliver=True
    sendgrid_api_key: Optional[str] = None

    # Email delivery config
    from_email: str = "felipe.sanchez2028@gmail.com"
    to_email: str = "santihs.sanchez@gmail.com"

    # Local Ollama
    ollama_base_url: str = "http://localhost:11434/v1"
    guardrail_timeout: float = 10.0  # seconds before failing open

    # Pipeline tuning
    max_searches: int = 5
    max_concurrent_searches: int = 3
    search_max_retries: int = 3
    search_retry_min_wait: int = 1   # seconds
    search_retry_max_wait: int = 10  # seconds


settings = Settings()
