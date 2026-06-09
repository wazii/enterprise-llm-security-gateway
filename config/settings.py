from pydantic_settings import BaseSettings
from config.validators import validate_log_level


class Settings(BaseSettings):
    APP_NAME: str = "Enterprise LLM Security Gateway"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str = "change_me"

    class Config:
        env_file = ".env"


settings = Settings()
validate_log_level(settings.LOG_LEVEL)