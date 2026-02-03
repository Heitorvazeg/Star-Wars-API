from typing import Any, Optional
import time


class Cache:
    """Simple in-memory cache with TTL."""

    def __init__(self, ttl: int = 300):
        self.store = {}
        self.ttl = ttl

    def get(self, key) -> Optional[Any]:
        v = self.store.get(key)
        if v is None:
            return None

        value, expires = v
        if expires < time.time():
            del self.store[key]
            return None

        return value

    def set(self, key, value: Any):
        self.store[key] = (value, time.time() + self.ttl)
