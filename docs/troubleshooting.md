# Troubleshooting

## @cacheable still caches in memory

- Is pico-data-redis installed in the same venv as pico-caching?
- With plain pico-ioc (no pico-boot), list the module:
  `init(modules=["pico_caching", "pico_data_redis", ...])`.
- A user-provided `CacheBackend` component competes with this one; the
  interceptor picks the first non-in-memory backend it finds.

## Redis is down and nothing failed

By design (fail-open): reads miss, writes drop, methods recompute. Watch the
Redis side with your own monitoring; if you need hard failures, use the
injected client directly.

## My cached values disappear on restart

Check you are actually on the Redis backend (see first entry) and that the
TTL (`@cacheable(ttl_seconds=...)`) is what you think — entries expire
server-side via `PX`.

## clear() did not delete my other keys

Correct: it only deletes `redis.cache_prefix`-prefixed keys. Flush anything
else explicitly with the injected client.

## Unpickling errors after a deploy

Cached objects from the previous code version may not unpickle into the new
classes. Bump `redis.cache_prefix` (or flush the namespace) on deploys that
change cached types.
