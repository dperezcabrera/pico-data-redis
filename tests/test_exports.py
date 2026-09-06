"""The public API is exactly what ``__all__`` declares (stability contract)."""

import pico_data_redis


def test_public_api_is_declared_and_importable():
    assert set(pico_data_redis.__all__) == {"RedisCacheBackend", "RedisFactory", "RedisSettings"}
    for name in pico_data_redis.__all__:
        assert getattr(pico_data_redis, name) is not None
