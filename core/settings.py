from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from .env file."""

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # API Configuration
    SWAPI_URL: str = "https://swapi.dev/api/"

    # JWT Configuration
    JWT_SECRET: str = "secret_key_test"
    JWT_ALGORITHM: str = "HS256"

    # Application Configuration
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"


settings = Settings()
