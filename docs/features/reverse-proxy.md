# Reverse proxy

Forward HTTP and HTTPS requests from clients to remote services. ProxyCraft rewrites paths, preserves headers, and normalizes response `Content-Length` automatically.

## Basic HTTPS upstream

```json
{
  "prefix": "/posts",
  "match": "/posts/**",
  "backends": {
    "https": {
      "url": "https://jsonplaceholder.typicode.com/posts"
    }
  },
  "upstream": {
    "proxy": {
      "enabled": true,
      "timeout_seconds": 30
    }
  }
}
```

A request to `GET /posts/1` is sent to `https://jsonplaceholder.typicode.com/posts/1`.

## Path prefix stripping

The `prefix` value is removed before the request hits the backend. Use this when your public URL layout differs from the upstream API:

| Client requests | Upstream receives |
|-----------------|-------------------|
| `/api/users/42` with `prefix: "/api"` | `/users/42` appended to backend base URL |

## Streaming mode

For large or long-lived responses, set `mode: "stream"` on the HTTPS backend:

```json
"https": {
  "url": "https://httpbun.com",
  "ssl": true,
  "mode": "stream"
}
```

## When to use it

- Expose an internal or third-party API on your own host and port
- Add a single entry point in front of microservices
- Terminate TLS at ProxyCraft and speak plain HTTP to legacy backends behind your network

See [API gateway](../use-cases/api-gateway.md) for a full walkthrough.
