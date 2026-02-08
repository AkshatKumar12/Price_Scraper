import time
from config import Config

cache_store = {}

def get_cache(key):
    if key in cache_store:
        data, timestamp = cache_store[key]
        if time.time() - timestamp < Config.CACHE_TTL:
            return data
    return None

def set_cache(key, value):
    cache_store[key] = (value, time.time())
