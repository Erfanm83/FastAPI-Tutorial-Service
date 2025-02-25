from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    JWT_SECRET_KEY: str = "test"
    REDIS_URL: str
    SENTRY_DSN: str = "https://1870bf6d3943b1d7c7e126a9e3b9c592@sentry.hamravesh.com/8050"

    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = "no-reply@example.com"
    MAIL_PORT: int = 25
    MAIL_SERVER: str = "smtp4dev"
    MAIL_FROM_NAME: str = "Admin"
    MAIL_STARTTLS: bool = False
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = False
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
