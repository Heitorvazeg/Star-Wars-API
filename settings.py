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
    swapi_api_url: str = "https://swapi.dev/api/"

    # JWT Configuration
    jwt_secret: str = "secret_key_test"
    jwt_algorithm: str = "HS256"

    # Application Configuration
    debug: bool = False
    log_level: str = "INFO"


settings = Settings()
