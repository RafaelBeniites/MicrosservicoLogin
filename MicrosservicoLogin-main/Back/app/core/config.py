from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Environment aware settings for the authentication service."""

    sql_database_url: str = Field(
        default="sqlite:///./auth.db", env="AUTH_DATABASE_URL"
    )
    secret_key: str = Field(
        default="super-secret-key-change-me", env="AUTH_SECRET_KEY"
    )
    algorithm: str = Field(default="HS256", env="AUTH_ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=60, env="AUTH_ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    api_prefix: str = Field(default="/auth")
    app_name: str = Field(default="Auth Service")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
