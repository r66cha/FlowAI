"""Конфигурация БД."""

# -- Imports

from pydantic_settings import BaseSettings, SettingsConfigDict

# -- Exports

__all__ = ["db_url"]

# --


class DB_URL(BaseSettings):
    """
    Класс настроек Pydantic для настройки параметров подключения к базе данных.
    """

    # -- API

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    # --

    dialect: str = "postgresql+asyncpg"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @property
    def get_DB_URL_API(self) -> str:
        """Создайте полную строку URL-адреса подключения к базе данных."""

        return f"{self.dialect}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


db_url = DB_URL()
