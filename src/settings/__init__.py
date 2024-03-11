from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    api_prefix: str = "/api"

    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_reload: bool = True

    # DB settings
    postgres_db: str
    postgres_user: str
    postgres_host: str
    postgres_port: str
    postgres_password: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
