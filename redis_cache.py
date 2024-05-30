import redis
from config import REDIS_URI, REDIS_PORT, REDIS_PASSWORD

REDIS_CACHE = redis.Redis(
  host=REDIS_URI,
  port=REDIS_PORT,
  password=REDIS_PASSWORD
)