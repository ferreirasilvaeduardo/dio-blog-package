from pydantic_settings import (
    BaseSettings,
)  # Certifique-se de que está importando do pacote correto


class Settings(BaseSettings):
    # Configurações gerais
    APP_NAME: str = "DIO BLOG"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ISS: str = "curso-fastapi.com.br"
    AUD: str = "curso-fastapi"

    # Configurações do banco de dados
    DATABASE_URL: str = "sqlite:///./blog.db"

    # Configurações de segurança
    SECRET_KEY: str = "default-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SCHEME: str = "Bearer"

    class Config:
        env_file = ".env"  # Carregar variáveis de ambiente de um arquivo .env
        # env_file = None  # Desabilitar o carregamento do arquivo .env
        # quando desabilitado, sera necessario criar variavel de ambiente
        # export APP_NAME="DIO BLOG"
        # export APP_VERSION="1.0.0"
        # export DEBUG="True"
        # export DATABASE_URL="sqlite:///./blog.db"
        # export SECRET_KEY="my-super-secret-key"
        # export ALGORITHM="HS256"
        # export ACCESS_TOKEN_EXPIRE_MINUTES="30"


# Instância global das configurações
settings = Settings()
