from app.settings import REDIS

broker_url = f'redis://:{REDIS.PASS}@{REDIS.HOST}:{REDIS.PORT}/0'
result_backend = f'redis://:{REDIS.PASS}@{REDIS.HOST}:{REDIS.PORT}/0'

timezone = 'Asia/Almaty'
enable_utc = True
