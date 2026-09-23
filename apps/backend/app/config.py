from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "VayuNet Intelligence Backend"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    CORS_ORIGINS: str = "http://localhost:3000"

    GEMINI_API_KEY: str = ""
    GEMINI_SECRET_ID: str = "gemini-api-key"
    GEMINI_MODEL_NAME: str = "gemini-2.5-flash"
    GEMINI_USE_VERTEX_AI: bool = True

    GCP_PROJECT_ID: str = "your-gcp-project-id"
    GOOGLE_CLOUD_PROJECT: str = ""
    GOOGLE_CLOUD_LOCATION: str = "global"

    BIGQUERY_DATASET: str = "vayunet_prod"
    BIGQUERY_OBSERVATIONS_TABLE: str = "observations"

    VERTEX_AI_MODEL_NAME: str = "gemini-2.5-flash"
    EARTH_ENGINE_COLLECTION: str = "COPERNICUS/S5P/NRTI/L3_NO2"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
