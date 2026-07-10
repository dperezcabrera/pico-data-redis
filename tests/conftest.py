import fakeredis
import pytest
from pico_ioc import DictSource, configuration, init

import pico_redis.factory as factory_module


@pytest.fixture(autouse=True)
def isolate_from_installed_plugins(monkeypatch):
    monkeypatch.setenv("PICO_BOOT_AUTO_PLUGINS", "false")


@pytest.fixture(autouse=True)
def fake_redis(monkeypatch):
    """Every container in the suite talks to an in-process fakeredis."""
    server = fakeredis.FakeServer()

    class FakeRedisFromUrl(fakeredis.FakeRedis):
        @classmethod
        def from_url(cls, url, **kwargs):
            return cls(server=server)

    monkeypatch.setattr(factory_module, "Redis", FakeRedisFromUrl)
    return server


@pytest.fixture
def make_container():
    created = []

    def _make(*modules, config=None):
        cfg = configuration(DictSource(config or {}))
        container = init(modules=["pico_redis", *modules], config=cfg)
        created.append(container)
        return container

    yield _make
    for c in reversed(created):
        c.shutdown()
