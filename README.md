# pico-data-redis

[![PyPI](https://img.shields.io/pypi/v/pico-data-redis.svg)](https://pypi.org/project/pico-data-redis/)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/dperezcabrera/pico-data-redis)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
![CI (tox matrix)](https://github.com/dperezcabrera/pico-data-redis/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/dperezcabrera/pico-data-redis/branch/main/graph/badge.svg)](https://codecov.io/gh/dperezcabrera/pico-data-redis)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=dperezcabrera_pico-data-redis&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=dperezcabrera_pico-data-redis)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=dperezcabrera_pico-data-redis&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=dperezcabrera_pico-data-redis)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=dperezcabrera_pico-data-redis&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=dperezcabrera_pico-data-redis)
[![PyPI Downloads](https://img.shields.io/pypi/dm/pico-data-redis)](https://pypi.org/project/pico-data-redis/)
[![Docs](https://img.shields.io/badge/Docs-pico--data--redis-blue?style=flat&logo=readthedocs&logoColor=white)](https://dperezcabrera.github.io/pico-data-redis/)
[![Interactive Lab](https://img.shields.io/badge/Learn-online-green?style=flat&logo=python&logoColor=white)](https://dperezcabrera.github.io/pico-learn/)

Redis for the [pico ecosystem](https://github.com/dperezcabrera/pico-ioc): a shared injectable client, and a distributed backend that makes `@cacheable` (pico-caching) work across processes. Installing it is opting in.

## Installation

```bash
pip install pico-data-redis
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

Full documentation: https://dperezcabrera.github.io/pico-data-redis/

## AI Coding Skills

Install [Claude Code](https://code.claude.com) or [OpenAI Codex](https://openai.com/index/introducing-codex/) skills for AI-assisted development with pico-data-redis:

```bash
curl -sL https://raw.githubusercontent.com/dperezcabrera/pico-skills/main/install.sh | bash
```

The `pico-conventions` skill teaches the assistant this module's API surface and invariants; `/add-component` and `/add-tests` scaffold components and tests that use it.

## License

MIT
