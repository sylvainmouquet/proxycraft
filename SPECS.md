# ProxyCraft — Product Specification

ProxyCraft is a config-driven HTTP/HTTPS reverse proxy built on Starlette. It routes requests by path pattern to pluggable upstream backends, applies security and performance middleware, and supports multi-server ASGI deployment.

## High impact, relatively simple

### 1. HTTP/HTTPS reverse proxy

**Status:** Done

Forward HTTP requests to remote HTTPS backends with prefix-based URL rewriting.

- [x] Starlette ASGI application with catch-all routing
- [x] HTTPS upstream forwarding via aiohttp
- [x] Content-Length normalization on proxied responses

**Key files:** `proxycraft/proxycraft.py`, `proxycraft/upstreams/backends/http/https.py`, `proxycraft/protocols/https_aiohttp.py`

### 2. JSON-driven configuration

**Status:** Done

Load proxy behavior from a JSON config file with typed models and validation.

- [x] Pydantic/dataclass config models
- [x] File loader with defaults
- [x] Example registry-mirror presets (PyPI, npm, Maven, GitHub, Alpine)

**Key files:** `proxycraft/config/models.py`, `proxycraft/config/loader.py`, `proxycraft/default.json`

### 3. Path-based endpoint routing

**Status:** Done

Match incoming requests to endpoints using Ant-style path patterns with weight ordering.

- [x] Ant path matcher integration
- [x] Weight-sorted endpoint selection
- [x] Prefix stripping before upstream dispatch

**Key files:** `proxycraft/networking/routing/routing_selector.py`

### 4. Upstream backend handlers

**Status:** Done

Pluggable handlers selected by backend type in endpoint configuration.

- [x] HTTPS backend
- [x] Echo backend
- [x] Mock backend
- [x] Redirect backend
- [x] Command backend (OS-specific command execution)

**Key files:** `proxycraft/proxycraft.py`, `proxycraft/upstreams/backends/http/https.py`, `proxycraft/upstreams/backends/http/echo.py`, `proxycraft/upstreams/backends/http/mock.py`, `proxycraft/upstreams/backends/http/redirect.py`, `proxycraft/upstreams/backends/system/command.py`

### 5. Virtual upstream aggregation

**Status:** Done

Resolve requests by trying multiple source endpoints until one returns HTTP 200.

- [x] `first-match` strategy
- [x] Internal httpx ASGI loop for virtual resolution

**Key files:** `proxycraft/proxycraft.py`

### 6. Security middleware (IP and bot filtering)

**Status:** Done

Filter requests by client IP and User-Agent using Ant-style blacklist and whitelist patterns.

- [x] IP filter middleware
- [x] Bot filter middleware

**Key files:** `proxycraft/middlewares/security/ip_filter.py`, `proxycraft/middlewares/security/bot_filter.py`

### 7. Performance middleware (resource filter and in-file cache)

**Status:** Done

Skip noisy static paths and cache GET responses to disk.

- [x] Resource filter middleware (skip paths)
- [x] In-file response caching with TTL and size limits

**Key files:** `proxycraft/middlewares/performance/resource_filter.py`, `proxycraft/middlewares/performance/caching/in_file.py`

### 8. Response transformation

**Status:** Done

Apply text replacements to upstream response bodies per endpoint.

- [x] Configurable find/replace rules
- [x] Registry mirror URL rewriting presets

**Key files:** `proxycraft/middlewares/transformer/response_transform.py`

### 9. Connection pooling and request tracing

**Status:** Done

Share aiohttp TCP connectors across requests with lifecycle trace hooks.

- [x] Shared connector on app startup/shutdown
- [x] Trace handlers for connection events
- [x] Multiple connector strategies (singleton, thread-local, event-loop, context)

**Key files:** `proxycraft/networking/connection_pooling/connection_pooling.py`, `proxycraft/networking/connection_pooling/http_client.py`, `proxycraft/networking/connection_pooling/connectors/`, `proxycraft/networking/connection_pooling/tracing/default_trace_handler.py`

### 10. Multi-server ASGI deployment

**Status:** Done

Run the proxy under common ASGI servers with optional TLS termination.

- [x] Gunicorn (default)
- [x] Uvicorn
- [x] Hypercorn
- [x] Server TLS via certificate and key paths

**Key files:** `proxycraft/proxycraft.py`

---

## Medium impact — broadens scope

### 11. In-memory response caching

**Status:** Planned

Middleware is registered but caching logic is currently disabled.

- [ ] Enable in-memory cache with TTL and size limits
- [ ] Wire `MemoryCacheConfig` from endpoint middleware settings

**Potential files:** `proxycraft/middlewares/performance/caching/in_memory.py`

### 12. Response compression

**Status:** Planned

Compression middleware exists but config field mapping needs alignment with the config model.

- [ ] Fix `min_size` / `types` config mapping
- [ ] Support gzip and brotli per endpoint

**Potential files:** `proxycraft/middlewares/performance/compression.py`

### 13. Circuit breaker middleware

**Status:** Planned

Full middleware implementation exists but is not registered in the application stack.

- [ ] Register circuit breaker in middleware stack
- [ ] Expose threshold and window settings from config

**Potential files:** `proxycraft/middlewares/performance/circuit_breaker.py`

### 14. Load balancing and health checks

**Status:** Planned

Config models support weighted backends and health checks; runtime currently selects the first HTTPS backend.

- [ ] Weighted backend selection
- [ ] Periodic health check probes
- [ ] Sticky session support

**Potential files:** `proxycraft/config/models.py`, `proxycraft/upstreams/backends/http/https.py`

### 15. Automatic retry on upstream failure

**Status:** Planned

`RetryConfig` is defined on HTTPS backends but not applied during upstream requests.

- [ ] Retry failed requests with configurable delay and status codes
- [ ] Respect per-backend retry limits

**Potential files:** `proxycraft/config/models.py`, `proxycraft/upstreams/backends/http/https.py`

### 16. Outbound authentication (Basic, JWT)

**Status:** Planned

Header providers exist for Basic and JWT auth but endpoint auth config is not enforced on outbound requests.

- [ ] Apply endpoint `auth` config to HTTPS upstream calls
- [ ] Support credential rotation from config

**Potential files:** `proxycraft/security/authentication/basic_auth.py`, `proxycraft/security/authentication/jwt_auth.py`, `proxycraft/upstreams/backends/http/https.py`

### 17. WebSocket proxying

**Status:** Planned

WebSocket route accepts connections but backend forwarding is not implemented.

- [ ] Bidirectional WebSocket proxy to configured upstream
- [ ] Frame size and ping interval from config

**Potential files:** `proxycraft/proxycraft.py`, `proxycraft/protocols/websocket.py`

### 18. File-system static backend

**Status:** Planned

File backend handler and async reader exist but factory wiring and config placement need fixes.

- [ ] Fix handler constructor and factory registration
- [ ] Align config schema (`backends.file` vs `upstream.file`)

**Potential files:** `proxycraft/upstreams/backends/file_system/file.py`, `proxycraft/files/reader/io_async_reader.py`

### 19. Cron scheduler service

**Status:** Planned

Scheduler service and job history storage exist; HTTP handler returns placeholders and lifespan wiring is incomplete.

- [ ] Start scheduler on application lifespan
- [ ] Expose job status over HTTP

**Potential files:** `proxycraft/upstreams/backends/system/scheduler.py`

### 20. SOCKS, TCP, TLS, and UDP protocol clients

**Status:** Planned

Low-level protocol clients exist as libraries but are not integrated into the main proxy flow.

- [ ] Wire SOCKS5 client into upstream proxy path
- [ ] Expose TCP/TLS/UDP tunnel endpoints
- [ ] Add E2E tests for protocol clients

**Potential files:** `proxycraft/protocols/socks.py`, `proxycraft/protocols/tcp.py`, `proxycraft/protocols/tls.py`, `proxycraft/protocols/udp.py`

### 21. Metrics and health endpoints

**Status:** Planned

Prometheus integration and `/health` route are stubbed or commented out.

- [ ] Prometheus metrics export
- [ ] Liveness and readiness health routes
- [ ] Wire `Monitoring` config from endpoints

**Potential files:** `proxycraft/proxycraft.py`, `proxycraft/config/models.py`

### 22. Alternative ASGI servers (Granian, Robyn)

**Status:** Planned

Server branches exist but need correct app mounting and production readiness.

- [ ] Fix Granian app reference
- [ ] Mount Starlette app under Robyn

**Potential files:** `proxycraft/proxycraft.py`

---

## Polish & UX

### 23. Content-Length normalization

**Status:** Done

Ensure valid Content-Length headers on all proxied responses.

- [x] Always-on middleware in application stack

**Key files:** `proxycraft/middlewares/content_length_middleware.py`

### 24. Structured logging

**Status:** Done

Structured logging via structlog with a project-wide logger factory.

- [x] Configurable log levels
- [x] Null handler on package import

**Key files:** `proxycraft/logger.py`

### 25. Registry mirror presets

**Status:** Done

Ready-made endpoint configurations for common package registries.

- [x] PyPI, npm, Maven, GitHub, and Alpine mirror examples in default config

**Key files:** `proxycraft/default.json`

### 26. Docker deployment

**Status:** Done

Container image and run instructions for production deployment.

- [x] Dockerfile
- [x] README quick-start examples

**Key files:** `dockerfiles/pyprox.Dockerfile`, `README.md`

### 27. Request transformer middleware

**Status:** Planned

Middleware exists as a pass-through and is not registered in the application stack.

- [ ] Header and body transformation on inbound requests
- [ ] Register middleware per endpoint config

**Potential files:** `proxycraft/middlewares/transformer/request_transform.py`

---

## New Opportunities

### 28. Inbound authentication (Digest, NTLM, Kerberos)

**Status:** Planned

README advertises multiple auth methods; only outbound Basic and JWT helpers exist today.

- [ ] Digest authentication
- [ ] NTLM authentication
- [ ] Kerberos authentication

**Potential files:** `proxycraft/security/authentication/`

### 29. IP rotation for scraping

**Status:** Planned (Long Term)

Rotate outbound public IP addresses across upstream proxy pools.

- [ ] Proxy pool rotation policy
- [ ] Session-aware IP stickiness

### 30. Geo-targeting proxy routing

**Status:** Planned (Long Term)

Route requests through proxies in specific geographic regions.

- [ ] Region tags on upstream backends
- [ ] Client-aware routing rules

### 31. GraphQL upstream

**Status:** Planned

Config model exists; no runtime handler.

- [ ] GraphQL schema and resolver loading
- [ ] Optional playground endpoint

**Potential files:** `proxycraft/config/models.py`

### 32. Serverless function upstream

**Status:** Planned

Config model exists; no runtime handler.

- [ ] Function runtime dispatch (Python handler loading)
- [ ] Timeout and memory limits from config

**Potential files:** `proxycraft/config/models.py`

### 33. Service mesh integration

**Status:** Planned (Long Term)

Config model for service mesh metadata; no runtime integration.

- [ ] Service discovery via mesh sidecar
- [ ] Protocol and metadata propagation

**Potential files:** `proxycraft/config/models.py`

### 34. CORS middleware

**Status:** Planned

`CORS` model on endpoints; no middleware implementation.

- [ ] Per-endpoint CORS headers
- [ ] Preflight request handling

**Potential files:** `proxycraft/config/models.py`, `proxycraft/middlewares/`

### 35. Failover policies

**Status:** Planned

`Failover` model defined; no runtime failover logic.

- [ ] Automatic backend failover on errors
- [ ] Configurable failover thresholds

**Potential files:** `proxycraft/config/models.py`, `proxycraft/upstreams/backends/http/https.py`

### 36. Rate limiting

**Status:** Planned

`RateLimit` model on HTTPS backends; not enforced at runtime.

- [ ] Per-backend request rate limits
- [ ] Burst handling

**Potential files:** `proxycraft/config/models.py`, `proxycraft/upstreams/backends/http/https.py`

### 37. Long-form documentation site

**Status:** Planned

Project rules require a `docs/` directory with architecture, development, and testing guides.

- [x] Product specification (`SPECS.md`)
- [ ] Architecture documentation (`docs/architecture.md`)
- [ ] Development and testing guides
- [ ] GitHub Pages publishing workflow

**Potential files:** `docs/`, `.github/workflows/`

---

## Recommended Roadmap

### Phase 1 — Close config/runtime gaps

1. Enable load balancing and health checks on HTTPS backends
2. Wire retry, rate limiting, and outbound auth from config models
3. Fix and enable compression, in-memory cache, and circuit breaker middleware
4. Repair file backend wiring and scheduler lifespan integration

### Phase 2 — Protocol and observability

1. Implement WebSocket proxying end to end
2. Integrate SOCKS/TCP/TLS clients into the proxy server
3. Expose Prometheus metrics and health endpoints
4. Stabilize Granian and Robyn deployment paths

### Phase 3 — Advanced routing and auth

1. Inbound authentication (Basic, Digest, NTLM, Kerberos)
2. CORS and request transformation middleware
3. Failover policies and geo-targeting
4. GraphQL and serverless upstream handlers

### Phase 4 — Ecosystem and docs

1. Complete `docs/` with architecture and decision records
2. Publish documentation via GitHub Pages
3. IP rotation and service mesh integration (long term)

---

## Architecture notes

### System overview

ProxyCraft is a Starlette ASGI application. At startup it loads a JSON config, builds a middleware stack, registers catch-all HTTP routes, and creates a shared aiohttp connector for upstream HTTPS calls.

### Major components

| Component | Role |
|---|---|
| `proxycraft/proxycraft.py` | Application bootstrap, routing, middleware registration, server entry |
| `proxycraft/config/` | Config models, validation, and file loading |
| `proxycraft/networking/routing/` | Ant-style path matching and endpoint selection |
| `proxycraft/networking/connection_pooling/` | Shared aiohttp connectors and trace handlers |
| `proxycraft/upstreams/backends/` | Pluggable upstream handlers (HTTPS, echo, mock, redirect, command, file, scheduler) |
| `proxycraft/middlewares/` | Security, performance, and transformation middleware |
| `proxycraft/protocols/` | Low-level HTTP, WebSocket, SOCKS, TCP, TLS, and UDP clients |
| `proxycraft/security/authentication/` | Outbound auth header providers |

### Request flow

```text
Client
  → ASGI server (Gunicorn / Uvicorn / Hypercorn)
  → Middleware stack (content-length, cache, filters, compression, transformers)
  → Catch-all route handler
  → RoutingSelector (path match + weight)
  → Upstream dispatch
      → proxy: ProxyHandlerFactory → backend handler (e.g. HTTPS via aiohttp)
      → virtual: internal httpx loop over source endpoints (first-match)
  → Response back through middleware stack
```

### Dependencies

- **Starlette** — ASGI framework and routing
- **aiohttp** — upstream HTTPS client with connection pooling
- **httpx** — virtual upstream internal requests
- **Pydantic** — config validation
- **structlog** — structured logging
- **Gunicorn / Uvicorn / Hypercorn** — production ASGI servers

### Known limitations

- HTTPS upstream handler selects the first backend; load balancing config is not applied
- Several middleware modules are registered or implemented but disabled or incomplete
- Protocol clients (SOCKS, TCP, TLS, UDP) are library-level only and not exposed on the main server
- README feature list is broader than current runtime capabilities; see feature statuses above
