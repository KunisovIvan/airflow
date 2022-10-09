import json
from typing import Union

import aioredis

from app.settings import REDIS


class AsyncRedisConnector:

    connection = None

    async def connect(self):
        self.connection = await aioredis.from_url("redis://localhost", password=REDIS.PASS, db=REDIS.DB)

    async def get_key(self, key: str) -> Union[dict, None]:
        result = await self.connection.get(key)
        if not result:
            return
        return json.loads(result)

    async def set_key(self, key: str, value: str, ttl: int = None):
        if ttl:
            await self.connection.setex(key, ttl, value)
        else:
            await self.connection.set(key, value)

    async def delete(self, key):
        is_delete = await self.connection.delete(key)
        return is_delete
