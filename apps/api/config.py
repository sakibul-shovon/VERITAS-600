from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """VERITAS-600 Application Settings with Pydantic v2 validation."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # General
    ENVIRONMENT: str = "development"
    PORT: int = 8000
    NEXT_PUBLIC_API_URL: str = "http://localhost:8000"

    # PostgreSQL Database
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "veritas"
    POSTGRES_PASSWORD: str = "veritas_secret_change_me"
    POSTGRES_DB: str = "trade_finance"

    @property
    def postgres_dsn(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # Zetaris Federated Data Layer
    ZETARIS_BASE_URL: str = "https://api.zetaris.cloud/v1"
    ZETARIS_API_KEY: str = ""
    ZETARIS_EXECUTION_MODE: Literal["AUTO", "FORCE_LIVE", "FORCE_FALLBACK"] = "AUTO"

    # Meterless Gateway & Memory Router
    METERLESS_BASE_URL: str = "https://api.meterless.ai/v1"
    METERLESS_API_KEY: str = ""

    # NVIDIA NIM Inference Layer
    NVIDIA_BASE_URL: str = "https://integrate.api.nvidia.com/v1"
    NVIDIA_API_KEY: str = ""
    NEMOTRON_VISION_MODEL: str = "nvidia/nemotron-3.5-super-vl-120b-a12b"
    NEMOTRON_REASONING_MODEL: str = "nvidia/llama-3.3-nemotron-super-49b-v1"
    NEMOTRON_FAST_MODEL: str = "nvidia/llama-3.1-nemotron-nano-8b-v1"
    NIM_RATE_LIMIT_RPM: int = 25
    ENABLE_RESPONSE_CACHE: bool = True

    # Security
    SECRET_KEY: str = "veritas_default_secret_key_change_in_production"
    ZTRV_HMAC_SECRET: str = "veritas_zero_trust_runtime_hmac_secret"
    EXAMINER_API_KEY: str = ""  # If set, enforced on human-in-the-loop sign-off


@lru_cache
def get_settings() -> Settings:
    """Return cached singleton instance of Settings."""
    return Settings()
