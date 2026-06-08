from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Enterprise LLM Security Gateway"
    DEBUG: bool = False
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "security_gateway"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()