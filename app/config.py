from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = f"sqlite:///{Path(__file__).resolve().parent.parent / 'data' / 'tnved.db'}"
    app_title: str = "ТН ВЭД API"
    app_description: str = "API для поиска информации по коду ТН ВЭД"
    app_version: str = "1.0.0"
    search_limit: int = 50

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
