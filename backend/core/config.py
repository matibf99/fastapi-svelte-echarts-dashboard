from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv())


class Settings(BaseSettings):
    DATA_FILE_PATH: Path = Field(
        default=Path(__file__).parent.parent.parent / "data.json"
    )
    API_TITLE: str = "Data Visualization API"
    API_VERSION: str = "1.0.0"

    model_config = SettingsConfigDict(
        env_file=".env",
    )
