from cachetools import TTLCache

question_cache = TTLCache(maxsize=25, ttl=180)