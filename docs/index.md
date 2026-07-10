# pico-data-redis

A shared injectable Redis client, and the backend that makes `@cacheable` distributed.

## Install

```bash
pip install pico-data-redis
```

## 30-second example

```yaml
redis:
  url: redis://cache.internal:6379/0
```

```python
from redis import Redis
from pico_ioc import component

@component
class Sessions:
    def __init__(self, redis: Redis):
        self._redis = redis
```

Installed next to pico-caching, every `@cacheable` method transparently caches in Redis instead of process memory.

**See it in context**: the [flagship use case](https://dperezcabrera.github.io/pico-boot/flagship/) wires this module into a full order platform together with the rest of the ecosystem.
