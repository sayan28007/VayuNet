from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "VayuNet Intelligence Backend"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    GEMINI_API_KEY: str = ""
    GCP_PROJECT_ID: str = "your-gcp-project-id"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
