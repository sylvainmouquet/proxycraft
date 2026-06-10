# ProxyCraft

ProxyCraft is a config-driven HTTP/HTTPS reverse proxy. Point it at a JSON file, run one command, and route traffic to remote APIs, package registries, or local files — with caching, filtering, and URL rewriting built in.

## What you can do

| Goal | How ProxyCraft helps |
|------|----------------------|
| Mirror PyPI, npm, Maven, or Alpine packages on your network | Ready-made registry endpoints with disk cache and URL rewriting |
| Put a stable URL in front of a third-party API | HTTPS reverse proxy with path-based routing |
| Serve a fake API while a backend is not ready | Mock backend with path templates and JSON responses |
| Try local packages first, then fall back to a remote registry | Virtual upstream with `first-match` strategy |
| Block bots or unwanted client IPs | IP and User-Agent filters with Ant-style patterns |
| Speed up repeated GET requests | Per-endpoint file cache with TTL and size limits |

## Quick start

```bash
pip install proxycraft
```

Create `proxy.json`:

```json
{
  "version": "1.0",
  "name": "My proxy",
  "endpoints": [
    {
      "prefix": "/",
      "match": "**/*",
      "backends": {
        "https": {
          "url": "https://jsonplaceholder.typicode.com/posts"
        }
      },
      "upstream": {
        "proxy": { "enabled": true }
      }
    }
  ]
}
```

Run it:

```python
from proxycraft import ProxyCraft

ProxyCraft(config_file="proxy.json").serve(host="0.0.0.0", port=8091)
```

Requests to `http://localhost:8091/1` are forwarded to the upstream API.

## Next steps

- [Getting started](getting-started.md) — installation, first config, Docker
- [Configuration](configuration.md) — endpoints, backends, middleware
- [Package registry mirror](use-cases/registry-mirror.md) — PyPI, npm, Maven presets
- [Features](features/reverse-proxy.md) — everything ProxyCraft can do today
