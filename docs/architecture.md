# ProxyCraft Architecture

## Overview

ProxyCraft is a config-driven HTTP/HTTPS reverse proxy built on Starlette. Code is organized by **business capability** (feature) rather than technical layer.

## Package layout

```text
proxycraft/
├── app/                    # Composition root (ProxyCraft bootstrap, CLI)
├── features/               # Capability-owned code (config, routing, backends, middleware, …)
└── shared/                 # Cross-cutting infrastructure reused by multiple features
    ├── infrastructure/     # Logging
    ├── networking/         # Connection pooling, HTTP client connectors
    ├── persistence/        # Async file I/O helpers
    └── utilities/          # Generic helpers
```

## Major components

| Area | Location | Responsibility |
|------|----------|----------------|
| App | `proxycraft/app/` | Wire features into a runnable ASGI application |
| Configuration | `proxycraft/features/configuration/` | JSON config models and loader |
| Routing | `proxycraft/features/routing/` | Path-based endpoint selection |
| Upstream backends | `proxycraft/features/upstream_backends/` | Pluggable handler implementations |
| Security filtering | `proxycraft/features/security_filtering/` | IP and bot middleware |
| Performance | `proxycraft/features/performance/` | Caching, compression, resource filter |
| Transformation | `proxycraft/features/transformation/` | Request/response body transforms |
| Authentication | `proxycraft/features/authentication/` | Outbound auth providers |
| Protocols | `proxycraft/features/protocols/` | Low-level protocol clients |
| Connection pooling | `proxycraft/shared/networking/connection_pooling/` | Shared aiohttp connectors and tracing |

## Data flow

```text
Client → Starlette app → middleware stack → routing → upstream backend → response
```

Virtual upstream resolution retries multiple configured endpoints until one returns HTTP 200.

## Migration status

Migration to `features/` + `shared/` + `app/` is complete. Legacy layer folders (`middlewares/`, `networking/connection_pooling/`, `upstreams/`, etc.) have been removed. `proxycraft/proxycraft.py` remains a thin re-export of `proxycraft.app.proxycraft.ProxyCraft` for backward compatibility.

## Planned locations (not yet implemented)

| Capability | Future path |
|------------|-------------|
| Load balancing | `features/routing/load_balancing/` |
| Automatic retry | `features/routing/retrying/` |
| Authorization | `features/authentication/authorization/` |
| TCP upstream backend | `features/upstream_backends/tcp/` |

## Dependencies

- **Starlette** — ASGI application and middleware
- **aiohttp** — HTTPS upstream forwarding and connection pooling
- **httpx** — Virtual upstream internal loop
- **Pydantic** — Configuration models
- **structlog** — Structured logging

## Related documents

- [ADR 0001: Feature-based architecture](decisions/0001-feature-based-architecture.md)
- [Product specification](../SPECS.md) — Feature status and roadmap (contributors)
