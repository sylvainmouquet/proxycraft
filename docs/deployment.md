# Deployment

Run ProxyCraft on a laptop, in Docker, or behind a load balancer. Everything is controlled by your JSON config file.

## Run with Python

```python
from proxycraft import ProxyCraft

ProxyCraft(config_file="/etc/proxycraft/proxy.json").serve(host="0.0.0.0", port=8080)
```

Or pass `host` and `port` in code; config `server.port` is used when `serve()` is called without arguments.

## Docker

```bash
docker build -t proxycraft -f dockerfiles/proxycraft.Dockerfile .
docker run -d \
  -p 8080:8080 \
  -v /etc/proxycraft/proxy.json:/app/proxy.json:ro \
  -v /var/cache/proxycraft:/app/.cache \
  --name proxycraft \
  proxycraft
```

For registry mirrors, persist the cache volume. Mount your config read-only.

## ASGI servers

| `server.type` | Best for |
|---------------|----------|
| `gunicorn` | Production Linux, multiple workers |
| `uvicorn` | Simple deployments, development |
| `hypercorn` | HTTP/2 and built-in TLS |

Example:

```json
{
  "server": {
    "type": "gunicorn",
    "port": 8080,
    "workers": 4
  }
}
```

## HTTPS

```json
{
  "ssl": true,
  "server": {
    "type": "hypercorn",
    "port": 443,
    "certfile": "/etc/ssl/certs/proxycraft.pem",
    "keyfile": "/etc/ssl/private/proxycraft.key"
  }
}
```

Place TLS termination at ProxyCraft or at an external load balancer — both work. If the load balancer handles TLS, run ProxyCraft on HTTP internally.

## Production tips

- **Config** — keep `proxy.json` in version control; inject secrets via env or sidecar files if needed
- **Cache** — use a dedicated disk for `.cache/` on mirror instances
- **Security** — enable [IP filtering](features/security.md) on internal-only mirrors
- **Timeouts** — set `timeout_seconds` per endpoint for slow upstreams (registries, large artifacts)
- **Logging** — ProxyCraft uses structured logs; forward stdout to your log aggregator

## Upgrade

```bash
pip install -U proxycraft
```

Review [Changelog](changelog.md) before upgrading in production.
