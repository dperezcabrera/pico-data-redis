import fakeredis
import pytest
from pico_ioc import DictSource, configuration, init

import pico_redis.factory as factory_module


@pytest.fixture(autouse=True)
def isolate_from_installed_plugins(monkeypatch):
    monkeypatch.setenv("PICO_BOOT_AUTO_PLUGINS", "false")


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
