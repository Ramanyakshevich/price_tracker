import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = os.path.join(BASE_DIR, ".env")

class Settings(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DATABASE_URL: str
    TRAVELPAYOUTS_TOKEN: str

    PRIVATE_KEY_PATH: Path = BASE_DIR / "certs" / "private_key.pem"
    PUBLIC_KEY_PATH: Path = BASE_DIR / "certs" / "public_key.pem"

    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    @property
    def private_key(self) -> str:
        return self.PRIVATE_KEY_PATH.read_text()
    @property
    def public_key(self) -> str:
        return self.PUBLIC_KEY_PATH.read_text()

    model_config = SettingsConfigDict(env_file=ENV_PATH, extra="ignore")

settings = Settings()