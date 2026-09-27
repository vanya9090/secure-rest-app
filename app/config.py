from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./app.db"
    jwt_secret: SecretStr = Field(min_length=64)
    access_token_minutes: int = Field(default=30, ge=1, le=24*60)

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


def get_settings() -> Settings:
    return Settings()
