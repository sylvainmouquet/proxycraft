# API gateway

Put one stable URL in front of third-party or internal HTTP APIs. ProxyCraft handles routing, timeouts, and optional caching without application code.

## Problem

Your frontend or partner integrations need a fixed base URL, but backends live on different hosts, paths, or TLS setups. You want path-based routing and consistent timeouts without deploying a full API management suite.

## Solution

Define one endpoint per upstream API. Clients only talk to ProxyCraft.

## Single upstream

```json
{
  "version": "1.0",
  "name": "API gateway",
  "endpoints": [
    {
      "prefix": "/github",
      "match": "/github/**",
      "backends": {
        "https": { "url": "https://api.github.com", "ssl": true }
      },
      "upstream": { "proxy": { "enabled": true, "timeout_seconds": 30 } },
      "transformers": {
        "response": {
          "enabled": true,
          "textReplacements": [
            {
              "oldvalue": "https://api.github.com",
              "newvalue": "https://gateway.example.com/github"
            }
          ]
        }
      }
    },
    {
      "prefix": "/weather",
      "match": "/weather/**",
      "backends": {
        "https": { "url": "https://api.weather.example.com/v2" }
      },
      "upstream": { "proxy": { "enabled": true } }
    }
  ]
}
```

| Public URL | Upstream |
|------------|----------|
| `https://gateway.example.com/github/repos/...` | GitHub REST API |
| `https://gateway.example.com/weather/...` | Weather API v2 |

## Multiple services on one port

Use [path routing](../features/routing.md) weights to keep a catch-all while giving specific paths higher priority:

```json
{ "prefix": "/admin", "match": "/admin/**", "weight": 100, "backends": { ... } },
{ "prefix": "/", "match": "**/*", "weight": 0, "backends": { ... } }
```

## TLS termination

Terminate HTTPS at ProxyCraft and forward to HTTP backends inside your VPC:

```json
{
  "ssl": true,
  "server": {
    "type": "hypercorn",
    "port": 443,
    "certfile": "/etc/ssl/gateway.crt",
    "keyfile": "/etc/ssl/gateway.key"
  }
}
```

## When this fits

- BFF (backend-for-frontend) layer in front of a few REST services
- Partner-facing facade with one DNS name
- Gradual cutover — swap `url` in config instead of redeploying clients

## Related

- [Reverse proxy](../features/reverse-proxy.md)
- [Security filtering](../features/security.md)
