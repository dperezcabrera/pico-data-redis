Read and follow ./AGENTS.md for project conventions.

## Pico Ecosystem Context

pico-data-redis — Redis integration: injectable redis.Redis singleton + distributed CacheBackend for pico-caching. Installing it is opting in. Auto-discovered via the `pico_boot.modules` entry point. See it wired with the whole ecosystem in the flagship use case (pico-boot docs).

## Key Reminders

- pico-ioc dependency: `>= 2.2.0`; redis `>= 5`; pico-caching solo en dev/test
- **NEVER change `version_scheme`** in pyproject.toml. It MUST remain `"post-release"`.
- requires-python >= 3.11
- Commit messages: one line only
