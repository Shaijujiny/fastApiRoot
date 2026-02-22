import os

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV = os.getenv("ENVIRONMENT", "development")


class Settings(BaseSettings):
    """Application configuration settings."""

    # -----------------------------
    # Pydantic Config
    # -----------------------------
    model_config = SettingsConfigDict(
        env_file=f".env.{ENV}",  # dynamic env file
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )
    # ==========================================
    # Application Settings
    # ==========================================
    APP_NAME: str = "My FastAPI Application"
    PROJECT_NAME: str = "my_fastapi_project"  # Used for JWT issuer
    API_VERSION: str = "1.0.0"
    DESCRIPTION: str = "This is a sample FastAPI application."
    IS_SWAGGER_ENABLED: bool = True
    ROOT_PATH: str = ""
    FASTAPI_DEBUG: bool = True
    DEBUG: bool = True

    # -----------------------------
    # APP
    # -----------------------------
    APP_NAME: str = "FastAPI Base"
    ENVIRONMENT: str = ENV

    # -----------------------------
    # JWT
    # -----------------------------
    JWT_SECRET_KEY: str = "secret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    # -----------------------------
    # POSTGRES
    # -----------------------------
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "postgres"

    # -----------------------------
    # MYSQL (Optional)
    # -----------------------------
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "admin@123"
    MYSQL_DB: str = "fastapi"

    # -----------------------------
    # MONGO (Optional)
    # -----------------------------
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB: str = "Test"

    # ==========================================
    # Redis Settings
    # ==========================================
    REDIS_DB_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASS: str = "YOURPASSWORD"
    SSL_CA_CERTS: str | None = None

    # ==========================================
    # JWT Settings
    # ==========================================
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    APP_JWT_PRIVATE_KEY: str = ""
    APP_JWT_PUBLIC_KEY: str = ""


settings = Settings()
