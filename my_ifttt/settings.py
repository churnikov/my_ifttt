from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    telegram_api_id: str
    telegram_api_hash: str
    readwise_api_token: str
    debug: bool = False

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')

