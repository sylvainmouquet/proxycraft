# Configuration

ProxyCraft is entirely driven by a JSON config file. Each **endpoint** maps incoming URL paths to a **backend** and optional **upstream** options (proxy, cache, virtual sources).

## Top-level fields

| Field | Description |
|-------|-------------|
| `version` | Config schema version (use `"1.0"`) |
| `name` | Human-readable proxy name |
| `timeout` | Default upstream timeout |
| `ssl` | Enable TLS on the proxy listener |
| `server` | ASGI server type, port, and certificate paths |
| `middlewares` | Global security and performance middleware |
| `endpoints` | List of routed paths and their backends |

## Endpoint anatomy

Every endpoint needs at least a path match and a way to produce a response:

```json
{
  "identifier": "my-api",
  "prefix": "/api",
  "match": "/api/**",
  "weight": 10,
  "backends": {
    "https": {
      "url": "https://api.example.com/v1"
    }
  },
  "upstream": {
    "proxy": { "enabled": true, "timeout_seconds": 60 }
  }
}
```

| Field | Purpose |
|-------|---------|
| `prefix` | URL prefix stripped before forwarding to the backend |
| `match` | Ant-style pattern that selects this endpoint (`**`, `*`, `{id}`) |
| `weight` | Higher weight wins when multiple endpoints match |
| `backends` | Handler that fulfills the request (HTTPS, mock, echo, …) |
| `upstream` | Proxy settings, per-endpoint cache, or virtual sources |
| `transformers` | Find/replace rules on response bodies |

## Backend types

| Type | Use when |
|------|----------|
| `https` | Forward to a remote HTTP/HTTPS service |
| `echo` | Return request metadata (debugging, health checks) |
| `mock` | Serve fixed JSON from path templates |
| `redirect` | HTTP redirect to another URL |
| `command` | Run a shell command and return stdout |

See [Backends](features/backends.md) for examples of each type.

## Global middleware

Apply security and performance rules to all endpoints:

```json
{
  "middlewares": {
    "security": {
      "ip_filter": {
        "enabled": true,
        "blacklist": ["10.0.0.0/8"]
      },
      "bot_filter": {
        "enabled": true,
        "blacklist": [{ "name": "scraper", "user-agent": "*bot*" }]
      }
    },
    "performance": {
      "resource_filter": {
        "enabled": true,
        "skip_paths": ["favicon.ico", "robots.txt", ".well-known/**"]
      },
      "cache": {
        "file": {
          "enabled": true,
          "path": ".cache",
          "ttl": 86400,
          "max_size_mb": 1024
        }
      }
    }
  }
}
```

Per-endpoint cache and transformers override or extend these defaults. See [Caching](features/caching.md) and [Security filtering](features/security.md).

## Multiple HTTPS backends

List backends with weights for future load-balancing; today the first healthy backend is used:

```json
"backends": [
  {
    "https": [
      { "id": "primary", "url": "https://pypi.org/simple", "weight": 10 },
      { "id": "mirror", "url": "https://mirror.example.com/simple", "weight": 5 }
    ]
  }
]
```

## Virtual upstream

Combine several endpoints into one URL — try sources in order until one returns HTTP 200:

```json
{
  "prefix": "/packages",
  "match": "/packages/**",
  "upstream": {
    "virtual": {
      "sources": ["local-packages", "remote-packages"],
      "strategy": "first-match"
    }
  }
}
```

Source names refer to other endpoints' `identifier` fields. See [Virtual upstream](features/virtual-upstream.md).

## Validation

ProxyCraft validates the config at startup. Fix typos in field names or missing required backend URLs before serving traffic.
