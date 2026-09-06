# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `__all__` declares the public API and `tests/test_exports.py` pins it, per the ecosystem stability policy (ADR-014 in pico-ioc).

### Documentation
- `docs/architecture.md` links the ADR-014 stability and deprecation policy.

## [0.1.0] - 2026-07-10

### Added

- `RedisFactory`: injectable singleton `redis.Redis` built from `redis.url`; pool closed on container shutdown.
- `RedisCacheBackend`: distributed pico-caching backend (structural `CacheBackend`), pickled values with TTL, namespaced keys, fail-open on Redis errors.
- Settings under the `redis` prefix: `url`, `socket_timeout_seconds`, `cache_prefix` (zero-config).
- Auto-discovery via the `pico_boot.modules` entry point.
