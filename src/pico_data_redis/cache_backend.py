"""Distributed cache backend for pico-caching.

Satisfies pico-caching's ``CacheBackend`` Protocol structurally — no
import of pico-caching needed. Installing pico-data-redis next to
pico-caching makes ``@cacheable`` distributed: the interceptor prefers
any non-in-memory backend it finds in the container.

Values are pickled: ``@cacheable`` caches arbitrary Python results.
That makes the cache trusted storage — anyone who can write to Redis
can execute code in consumers. Keep it on a private instance, as with
celery result backends.
"""

import pickle
from typing import Any, Tuple

from pico_ioc import component
from redis import Redis
from redis import exceptions as redis_exceptions

from .config import RedisSettings


@component
class RedisCacheBackend:
    def __init__(self, client: Redis, settings: RedisSettings):
        self._client = client
        self._prefix = settings.cache_prefix

    def _key(self, key: str) -> str:
        return self._prefix + key

    def get(self, key: str) -> Tuple[bool, Any]:
        try:
            raw = self._client.get(self._key(key))
        except redis_exceptions.RedisError:
            # Fail-open: an unreachable Redis degrades to a cache miss so
            # @cacheable methods keep working (slower, not broken).
            return False, None
        if raw is None:
            return False, None
        return True, pickle.loads(raw)

    def set(self, key: str, value: Any, ttl_seconds: float) -> None:
        try:
            self._client.set(self._key(key), pickle.dumps(value), px=max(1, int(ttl_seconds * 1000)))
        except redis_exceptions.RedisError:
            pass

    def delete(self, key: str) -> None:
        try:
            self._client.delete(self._key(key))
        except redis_exceptions.RedisError:
            pass

    def clear(self) -> None:
        try:
            keys = list(self._client.scan_iter(match=self._prefix + "*"))
            if keys:
                self._client.delete(*keys)
        except redis_exceptions.RedisError:
            pass
