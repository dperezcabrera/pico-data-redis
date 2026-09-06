# Architecture

```
RedisSettings (@configured, prefix redis)
        |
RedisFactory (@factory) --@provides(Redis)--> redis.Redis singleton
        |                                          |
RedisLifecycle (@cleanup) -- close() -------------+
        |
RedisCacheBackend (@component)
   structural CacheBackend (pico-caching Protocol) — no import of
   pico-caching; the cache interceptor prefers non-in-memory backends
```

## Design decisions

- **Opt-in by installation**: there is no enable flag. Installing the package
  next to pico-caching switches `@cacheable` to Redis; uninstalling reverts
  to in-memory. The package boundary IS the feature toggle.
- **Structural contract, zero coupling**: `RedisCacheBackend` satisfies
  pico-caching's `CacheBackend` Protocol without importing pico-caching, so
  either package can evolve or be absent independently. The integration test
  in this repo pins the contract.
- **Fail-open**: every backend operation catches `RedisError` and degrades to
  a miss (reads) or a no-op (writes). A cache outage makes the app slower,
  never broken. Hard failures are the caller's choice via the raw client.
- **Pickle, deliberately**: `@cacheable` stores arbitrary Python results, so
  values are pickled. This makes the Redis instance trusted infrastructure —
  documented, same trust model as a celery result backend.
- **Namespaced keys**: everything lives under `redis.cache_prefix`
  (default `pico:cache:`); `clear()` scans and deletes only that namespace,
  so cached entries coexist with your other Redis data.
- **One sync client**: `redis.Redis` with pooling covers the 0.1 scope; an
  `redis.asyncio` variant is a planned follow-up if demand appears.

## Stability and versioning

This module follows the ecosystem policy in [ADR-014: API Stability and Deprecation](https://github.com/dperezcabrera/pico-ioc/blob/main/docs/adr/adr-0014-api-stability-and-deprecation.md). The public API is exactly what `__all__` exports plus the `redis.*` settings keys and their defaults, pinned by `tests/test_exports.py`. Before 1.0 a breaking change ships as a minor release; a deprecated name keeps working, with a `DeprecationWarning` naming its replacement, for at least one minor release and 90 days before removal.
