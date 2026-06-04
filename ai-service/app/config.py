from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "openrecords-ai-service"
    app_version: str = "0.1.0"
    debug: bool = False

    database_url: str = "postgresql://openrecords:openrecords_dev_password@localhost:5432/openrecords"

    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-20250514"

    api_base_url: str = "http://localhost:8080"
    api_service_token: str = ""


settings = Settings()