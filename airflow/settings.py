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

    class Config:
        env_prefix = 'APP_'
        env_file = '.env'


class Postgres(BaseSettings):
    DB: str = 'airflow'
    USER: str = 'airflow'
    PASS: str = 'airflow'
    HOST: str = 'localhost'
    PORT: int = 5432
    URL: str = None

    @validator('URL', pre=True)
    def url(cls, _, values):
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            user=values.get('USER'),
            password=values.get('PASS'),
            host='db',
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
    URL: str = None

    @validator('URL', pre=True)
    def url(cls, _, values):
        return RedisDsn.build(
            scheme='redis',
            password=values.get('PASS'),
            host=values.get('HOST'),
            port=str(values.get('PORT')),
            path=f"/{values.get('DB') or ''}",
        )

    class Config:
        env_prefix = 'REDIS_'
        env_file = '.env'


REDIS = Redis()
APP = App()
# PG = Postgres()
