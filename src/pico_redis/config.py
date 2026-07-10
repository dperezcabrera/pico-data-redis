"""Settings for pico-redis (prefix ``redis``, zero-config)."""

from dataclasses import dataclass

from pico_ioc import configured


@configured(target="self", prefix="redis", mapping="tree")
@dataclass
class RedisSettings:
    """Installing pico-redis opts the app into Redis: the client and the
    cache backend activate with these defaults."""

    url: str = "redis://localhost:6379/0"
    socket_timeout_seconds: float = 5.0
    cache_prefix: str = "pico:cache:"
