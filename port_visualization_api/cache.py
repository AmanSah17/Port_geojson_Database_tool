import redis
import os
import json

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

try:
    r = redis.from_url(REDIS_URL, decode_responses=True)
    r.ping()
    print("Connected to Redis")
except redis.ConnectionError:
    print("Could not connect to Redis. Caching disabled.")
    r = None

def get_cached_ports():
    if r:
        cached_data = r.get("all_ports")
        if cached_data:
            return json.loads(cached_data)
    return None

def set_cached_ports(ports_data):
    if r:
        r.set("all_ports", json.dumps(ports_data), ex=3600) # Cache for 1 hour
