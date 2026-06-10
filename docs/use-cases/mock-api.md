# Mock API for development

Ship frontend and integration tests before the real backend exists. ProxyCraft's **mock** backend returns JSON from path templates with no upstream server.

## Problem

The UI team needs `/users` and `/users/{id}` responses today. The API team will not have endpoints ready until next sprint. Spinning up a separate mock server adds another deployment to maintain.

## Solution

Add a mock endpoint next to your real API routes in the same `proxy.json`:

```json
{
  "identifier": "mock",
  "prefix": "/mock",
  "match": "/mock/**",
  "backends": {
    "mock": {
      "enabled": true,
      "path_templates": {
        "/users": {
          "status_code": 200,
          "content_type": "application/json",
          "body": {
            "users": [
              { "id": 1, "name": "John Doe" },
              { "id": 2, "name": "Jane Smith" }
            ]
          }
        },
        "/users/{id}": {
          "status_code": 200,
          "content_type": "application/json",
          "body": {
            "id": "${path.id}",
            "name": "User ${path.id}",
            "email": "user${path.id}@example.com"
          }
        }
      },
      "default_response": {
        "status_code": 404,
        "body": { "error": "Resource not found" }
      }
    }
  },
  "upstream": { "proxy": { "enabled": true } }
}
```

## Try it

```bash
curl http://localhost:8091/mock/users
curl http://localhost:8091/mock/users/42
curl http://localhost:8091/mock/unknown   # returns 404 default
```

## Path variables

Use `${path.id}` (and similar) in the body to echo path segments from the template `/users/{id}`.

## Swap to the real API later

When the backend is ready, add a new endpoint with a higher `weight` or change the frontend base path from `/mock` to `/api`. The mock config can stay for tests.

## Related

- [Backends](../features/backends.md)
- [Echo backend](../features/backends.md#echo) — inspect raw requests during client debugging
