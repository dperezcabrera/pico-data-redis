"""Provides a shared ``redis.Redis`` client built from ``RedisSettings``."""

from pico_ioc import cleanup, component, factory, provides
from redis import Redis

from .config import RedisSettings


@factory
class RedisFactory:
    @provides(Redis, scope="singleton")
    def create_client(self, settings: RedisSettings) -> Redis:
        return Redis.from_url(settings.url, socket_timeout=settings.socket_timeout_seconds)


@component
class RedisLifecycle:
    """Closes the shared client's connection pool on container shutdown."""

    def __init__(self, client: Redis):
        self._client = client

    @cleanup
    def close(self) -> None:
        self._client.close()
