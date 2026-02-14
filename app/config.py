"""
AlvGolf Agentic Analytics Engine - Configuration Management

Loads environment variables from .env file using pydantic-settings.
All sensitive data (API keys) must be in .env, never hardcoded.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Environment variables are loaded from .env file automatically.
    """

    # ============ Anthropic (Claude) ============
    anthropic_api_key: str

    # ============ Pinecone Vector Database ============
    pinecone_api_key: str
    pinecone_index_name: str = "alvgolf-rag"
    pinecone_environment: str = "us-east-1"

    # ============ Application ============
    env: Literal["local", "development", "production"] = "local"
    log_level: str = "INFO"

    # ============ API Configuration ============
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


# Singleton instance
settings = Settings()


# Validation on load
def validate_settings():
    """
    Validate critical settings on app startup.
    Raises error if something is misconfigured.
    """
    assert settings.anthropic_api_key.startswith("sk-ant-"), \
        "Invalid Anthropic API key format"

    assert settings.pinecone_api_key.startswith("pcsk_"), \
        "Invalid Pinecone API key format"

    assert len(settings.pinecone_index_name) > 0, \
        "Pinecone index name cannot be empty"

    print("[OK] Configuration validated successfully")


if __name__ == "__main__":
    # Test config loading
    print("Testing configuration...")
    print(f"Environment: {settings.env}")
    print(f"Pinecone Index: {settings.pinecone_index_name}")
    print(f"API Key (Anthropic): {settings.anthropic_api_key[:20]}...")
    print(f"API Key (Pinecone): {settings.pinecone_api_key[:20]}...")

    validate_settings()
