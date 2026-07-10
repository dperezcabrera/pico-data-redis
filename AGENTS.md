# pico-data-redis

Redis integration: injectable redis.Redis singleton + distributed CacheBackend for pico-caching. Installing it is opting in.

## Commands

```bash
pip install -e ".[dev]"
pytest tests/ -v
pytest --cov=pico_data_redis --cov-report=term-missing tests/
mkdocs serve -f mkdocs.yml
```

## Project Structure

```
src/pico_data_redis/
  __init__.py       # Public API
  factory.py        # RedisFactory (@provides Redis) + RedisLifecycle (@cleanup)
  cache_backend.py  # RedisCacheBackend (structural pico-caching CacheBackend)
  config.py         # RedisSettings (prefix "redis")
```

## Key Concepts

- Structural contract: satisfies pico-caching's CacheBackend Protocol WITHOUT importing pico-caching.
- Fail-open: RedisError -> miss on reads, no-op on writes; an outage slows the app, never breaks it.
- Values are pickled -> the Redis instance is trusted infrastructure (same model as a celery backend).
- Keys namespaced under redis.cache_prefix; clear() only touches that namespace.
- Tests: patch from_url ON the real Redis class (PEP 649: swapping the class changes the DI key on py3.14).

## Boundaries

- PyPI name is pico-data-redis (pico-redis collides ultranormalized with picoredis)
- Sync client only (redis.asyncio variant = future work on demand)
- Do not modify `_version.py`
