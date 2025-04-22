from pydantic_settings import BaseSettings  # , SettingsConfigDict


class Settings(BaseSettings):
    # Configurações gerais
    SUMMARY: str = "API para blog pessoal."
    APP_NAME: str = "DIO blog API"
    APP_VERSION: str = "1.2.0"
    DEBUG: bool = True
    ISS: str = "curso-fastapi.com.br"
    AUD: str = "curso-fastapi"
    ENVIRONMENT: str | None = None

    # Configurações do banco de dados
    DATABASE_URL: str = "sqlite:///./blog.db"

    # Configurações de segurança
    SECRET_KEY: str = "default-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SCHEME: str = "Bearer"

    # model_config = SettingsConfigDict(
    #     env_file=".env", extra="ignore", env_file_encoding="utf-8"
    # )
    class Config:
        env_file = ".env"  # Carregar variáveis de ambiente de um arquivo .env


# Instância global das configurações
settings = Settings()
