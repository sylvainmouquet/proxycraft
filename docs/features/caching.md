# Caching

Speed up repeated GET requests by storing responses on disk. Caching is configured per endpoint or globally under `middlewares.performance.cache`.

## File cache

```json
"upstream": {
  "proxy": { "enabled": true },
  "cache": {
    "file": {
      "enabled": true,
      "path": ".cache/pypi",
      "ttl": 43200,
      "max_size_mb": 256,
      "max_entries": 2500,
      "include_patterns": ["/pypi-remote/**"],
      "exclude_patterns": ["/health"]
    }
  }
}
```

| Option | Meaning |
|--------|---------|
| `ttl` | Seconds before a cached entry expires |
| `max_size_mb` | Maximum cache directory size |
| `max_entries` | Maximum number of cached responses |
| `include_patterns` / `exclude_patterns` | Limit which paths are cached |

## Global cache defaults

Set defaults once in `middlewares.performance.cache.file` and override per endpoint when needed. Registry mirror presets in the default config enable file caching for PyPI, npm, and Maven endpoints.

## Resource filter

Skip noisy paths so they never hit upstream or cache:

```json
"resource_filter": {
  "enabled": true,
  "skip_paths": [
    "favicon.ico",
    "robots.txt",
    ".well-known/**"
  ]
}
```

## When to use it

- **Air-gapped or slow networks** — cache package index pages and artifacts after the first download
- **Rate-limited APIs** — reduce calls to upstream providers
- **CI runners** — share one on-prem mirror instead of pulling from the public internet on every build

Pair caching with [response transformation](response-transformation.md) on registry mirrors so cached HTML still points at your proxy URL.
