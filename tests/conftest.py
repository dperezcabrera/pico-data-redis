import fakeredis
import pytest

import pico_data_redis.factory as factory_module


@pytest.fixture(autouse=True)
def fake_redis(monkeypatch):
    """Every container in the suite talks to an in-process fakeredis.

    Patch from_url ON the real class instead of replacing the module
    attribute: under PEP 649 (py3.14) annotations resolve lazily, so a
    swapped-in class would change the DI key and break resolution.
    """
    server = fakeredis.FakeServer()
    monkeypatch.setattr(
        factory_module.Redis,
        "from_url",
        classmethod(lambda cls, url, **kwargs: fakeredis.FakeRedis(server=server)),
    )
    return server
