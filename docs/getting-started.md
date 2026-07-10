# Getting Started

## Prerequisites

- Python >= 3.11
- pico-ioc >= 2.2.0 (pico-boot recommended for auto-discovery)
- redis-py >= 5 (installed automatically)
- pico-caching only if you want the distributed `@cacheable` backend

## Install

```bash
pip install pico-data-redis
```

## Key concepts

| Piece | What it does |
|---|---|
| `RedisFactory` | Provides a singleton `redis.Redis` for injection |
| `RedisCacheBackend` | pico-caching backend: `@cacheable` results stored in Redis |
| `redis.url` | Connection URL (default `redis://localhost:6379/0`) |
| `redis.cache_prefix` | Key namespace for cached entries (default `pico:cache:`) |

## Semantics

- **Opt-in by installation**: pico-boot discovers the module; the client and backend activate with defaults. Uninstall it and `@cacheable` falls back to in-memory.
- **Fail-open**: Redis down means cache misses (methods recompute), never request failures. Writes are silently dropped while the outage lasts.
- **Pickled values**: `@cacheable` caches arbitrary Python objects, so entries are pickled. Anyone with write access to the Redis instance can execute code in consumers — use a private, trusted instance.
- **Namespace hygiene**: `clear()` deletes only `cache_prefix`-keyed entries; your other Redis data is untouched.

## Configuration

```yaml
redis:
  url: redis://cache.internal:6379/0
  socket_timeout_seconds: 5
  cache_prefix: "myapp:cache:"
```

## Testing

Use fakeredis and patch the factory's client class, or register your own `@provides(Redis)` in a test module.
