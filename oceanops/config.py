from pprint import pprint
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    API_KEY_ID: str
    API_KEY_TOKEN: str

    model_config = SettingsConfigDict(
        env_file=".env",
    )


if __name__ == "__main__":
    settings = Settings()
    pprint(settings)
