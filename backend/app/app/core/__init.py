from ast import Str
from pydantic import BaseSettings
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_USERNAME: Str = 'postgres'
    DATABASE_PASSWORD: str = '1234'
    DATABASE_HOST: Str = 'localhost'
    DATABASE_NAME: str = 'mydb'
    DATABASE_URI: str = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"
    
    class config:
        case_sensitive: bool=True
        
        
@lru_cache
def get_settings()-> Settings:
    return Settings

Settings= get_settings()