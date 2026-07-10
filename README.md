# pico-redis

[![PyPI version](https://img.shields.io/pypi/v/pico-redis.svg)](https://pypi.org/project/pico-redis/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/dperezcabrera/pico-redis/actions/workflows/ci.yml/badge.svg)](https://github.com/dperezcabrera/pico-redis/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/dperezcabrera/pico-redis/branch/main/graph/badge.svg)](https://codecov.io/gh/dperezcabrera/pico-redis)
[![Docs](https://img.shields.io/badge/docs-mkdocs-blue)](https://dperezcabrera.github.io/pico-redis/)

Redis for the [pico ecosystem](https://github.com/dperezcabrera/pico-ioc): a shared injectable client, and a distributed backend that makes `@cacheable` (pico-caching) work across processes. Installing it is opting in.

## Installation

```bash
pip install pico-redis
```

## Quick start

```yaml
redis:
  url: redis://cache.internal:6379/0
```

Inject the shared client anywhere:

```python
from redis import Redis
from pico_ioc import component

@component
class Sessions:
    def __init__(self, redis: Redis):
        self._redis = redis
```

With pico-caching installed, `@cacheable` methods automatically use Redis instead of process memory — no code changes, the interceptor prefers any non-in-memory backend:

```python
from pico_caching import cacheable

@component
class Reports:
    @cacheable(ttl_seconds=300)
    def heavy_query(self, day: str) -> dict: ...
```

Notes:

- Cached values are pickled — treat the Redis instance as trusted, private infrastructure.
- The backend fails open: an unreachable Redis degrades to cache misses, never to errors.
- Keys are namespaced under `redis.cache_prefix` (default `pico:cache:`); `clear()` only touches that namespace.
- The client's pool closes on container shutdown.

## Documentation

Full documentation: https://dperezcabrera.github.io/pico-redis/

## License

MIT
