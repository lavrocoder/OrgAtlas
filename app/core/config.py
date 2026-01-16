from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    API_KEY: str = "your_secret_api_key_here"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/orgatlas"
    ENABLE_ADMIN: bool = False


settings = Settings()
