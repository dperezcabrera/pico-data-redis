import sys
import time

from pico_ioc import component
from redis import Redis
from redis import exceptions as redis_exceptions

from pico_data_redis import RedisCacheBackend, RedisSettings
from pico_data_redis.factory import RedisLifecycle

# --- factory + lifecycle ---


def test_client_is_injectable_singleton(make_container):
    container = make_container()
    client = container.get(Redis)
    assert container.get(Redis) is client
    client.set("k", b"v")
    assert client.get("k") == b"v"


def test_client_closed_on_shutdown(make_container):
    container = make_container()
    lifecycle = container.get(RedisLifecycle)
    closed = []
    original = lifecycle._client.close
    lifecycle._client.close = lambda: (closed.append(1), original())
    container.shutdown()
    assert closed == [1]


# --- cache backend ---


def test_set_get_roundtrip(make_container):
    backend = make_container().get(RedisCacheBackend)
    backend.set("k", {"complex": [1, 2, 3]}, ttl_seconds=60)
    hit, value = backend.get("k")
    assert hit is True
    assert value == {"complex": [1, 2, 3]}


def test_miss_returns_false(make_container):
    assert make_container().get(RedisCacheBackend).get("absent") == (False, None)


def test_entries_expire(make_container):
    backend = make_container().get(RedisCacheBackend)
    backend.set("k", "v", ttl_seconds=0.05)
    time.sleep(0.1)
    assert backend.get("k") == (False, None)


def test_delete(make_container):
    backend = make_container().get(RedisCacheBackend)
    backend.set("k", "v", ttl_seconds=60)
    backend.delete("k")
    assert backend.get("k") == (False, None)


def test_clear_only_touches_prefixed_keys(make_container):
    container = make_container()
    backend = container.get(RedisCacheBackend)
    client = container.get(Redis)
    backend.set("k1", "v", ttl_seconds=60)
    backend.set("k2", "v", ttl_seconds=60)
    client.set("unrelated", b"stays")
    backend.clear()
    assert backend.get("k1") == (False, None)
    assert backend.get("k2") == (False, None)
    assert client.get("unrelated") == b"stays"


def test_keys_are_namespaced(make_container):
    container = make_container(config={"redis": {"cache_prefix": "myapp:"}})
    backend = container.get(RedisCacheBackend)
    backend.set("k", "v", ttl_seconds=60)
    assert container.get(Redis).exists("myapp:k") == 1


# --- fail-open on broken redis ---


class _BrokenClient:
    def __getattr__(self, name):
        def boom(*args, **kwargs):
            raise redis_exceptions.ConnectionError("redis down")

        return boom


def _broken_backend():
    return RedisCacheBackend(_BrokenClient(), RedisSettings())


def test_get_fails_open():
    assert _broken_backend().get("k") == (False, None)


def test_writes_are_swallowed():
    backend = _broken_backend()
    backend.set("k", "v", ttl_seconds=60)
    backend.delete("k")
    backend.clear()


# --- integration with pico-caching ---


@component
class Expensive:
    calls = 0

    def __init__(self):
        pass

    from pico_caching import cacheable

    @cacheable(ttl_seconds=60)
    def compute(self, x: int) -> int:
        Expensive.calls += 1
        return x * 2


def test_cacheable_uses_redis_backend(make_container):
    Expensive.calls = 0
    container = make_container("pico_caching", sys.modules[__name__])
    svc = container.get(Expensive)
    assert svc.compute(21) == 42
    assert svc.compute(21) == 42
    assert Expensive.calls == 1

    client = container.get(Redis)
    assert any(k.startswith(b"pico:cache:") for k in client.keys("*"))


def test_clear_with_empty_cache_is_noop(make_container):
    make_container().get(RedisCacheBackend).clear()
