from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    postgres_user : str
    postgres_password : str

    secret_key : str
    jwt_algorithm : str
    access_token_expire_minutes : int

    model_config = SettingsConfigDict(
        env_file = "~/.env",
        env_file_encoding = 'utf-8'
    )

settings = Settings()