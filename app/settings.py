import os
from typing import List

from dotenv import load_dotenv
from pydantic import BaseSettings, validator, PostgresDsn, IPvAnyInterface, RedisDsn

load_dotenv(verbose=True)


class App(BaseSettings):
    HOST: IPvAnyInterface = os.getenv('APP_HOST')
    PORT: int = os.getenv('APP_PORT')
    PROVIDER_URLS: List[str] = ['http://localhost:8000', 'http://localhost:8001']
    CURRENCY_URL: str = os.getenv('CURRENCY_URL')
    ALLOW_ORIGINS: List[str] = ['*']


class Postgres(BaseSettings):
    DB: str = os.getenv('PG_DB')
    USER: str = os.getenv('PG_USER')
    PASS: str = os.getenv('PG_PASS')
    HOST: str = os.getenv('PG_HOST')
    PORT: int = os.getenv('PG_PORT')
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
    HOST: str = os.getenv('REDIS_HOST')
    PORT: int = os.getenv('REDIS_PORT')
    DB: int = os.getenv('REDIS_DB')
    PASS: str = os.getenv('REDIS_PASS')


REDIS = Redis()
APP = App()
PG = Postgres()
