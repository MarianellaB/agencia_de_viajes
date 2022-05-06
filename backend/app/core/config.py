from typing import Optional
from functools import lru_cache
from pydantic import BaseSettings 


class Settings(BaseSettings):
    DATABASE_USERNAME: str = 'postgres'
    DATABASE_PASSWORD: str = '1234'
    DATABASE_HOST: str = 'localhost'
    DATABASE_NAME: str = 'airnorthsouth'

    DATABASE_URI: Optional[str] = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:5434/{DATABASE_NAME}"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 5
    JWT_SECRET: str = "nBlLp3w5gofo65RXJvRGM0sIliDDCsT0MkH01t0Ydf8Imks6su"
    ALGORITHM: str = "HS512"

    class Config:
        case_sensitive: bool = True
    
@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()