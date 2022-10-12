import os
from typing import List

from dotenv import load_dotenv
from pydantic import BaseSettings, validator, PostgresDsn, IPvAnyInterface

load_dotenv(verbose=True)


class App(BaseSettings):
    HOST: IPvAnyInterface
    PORT: int
    PROVIDER_URLS: List[str] = ['http://localhost:8000', 'http://localhost:8001']
    CURRENCY_URL: str = os.getenv('CURRENCY_URL')
    ALLOW_ORIGINS: List[str] = ['*']

    class Config:
        env_prefix = 'APP_'
        env_file = '.env'


class Postgres(BaseSettings):
    DB: str
    USER: str
    PASS: str
    HOST: str
    PORT: int
    URL: str = None

    @validator('URL', pre=True)
    def url(cls, _, values):
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            user=values.get('USER'),
            password=values.get('PASS'),
            host=values.get('HOST'),
            port=str(values.get('PORT')),
            path=f"/{values.get('DB') or ''}",
        )

    class Config:
        env_prefix = 'PG_'
        env_file = '.env'


class Redis(BaseSettings):
    HOST: str
    PORT: int
    DB: int
    PASS: str

    class Config:
        env_prefix = 'REDIS_'
        env_file = '.env'


REDIS = Redis()
APP = App()
PG = Postgres()
