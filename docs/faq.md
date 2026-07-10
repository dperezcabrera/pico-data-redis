# FAQ

## Does installing pico-data-redis force everything through Redis?

Only `@cacheable` switches backend (pico-caching prefers non-in-memory backends automatically). Everything else uses Redis only where you inject the client.

## Why pickle instead of JSON?

`@cacheable` caches arbitrary method results — dataclasses, ORM rows, sets — which JSON cannot represent. The trade-off is documented: the Redis instance must be trusted, exactly like a celery result backend.

## What happens when Redis is down?

Reads return cache misses and writes are dropped, so cached methods keep working at uncached speed. If you need hard failures, wrap the client calls yourself.

## Can I use it for locks or rate limiting?

Inject the shared `redis.Redis` and use redis-py's primitives directly (`client.lock(...)`). Dedicated helpers may come later if there is demand.

## Async support?

The shared client is sync (`redis.Redis`). An `redis.asyncio` variant is a natural follow-up — open an issue if you need it.
