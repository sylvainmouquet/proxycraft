# Backends

Each endpoint uses one **backend** handler to produce a response. Pick the handler that fits the job.

## HTTPS

Forward to a remote service. The most common backend.

```json
"backends": {
  "https": {
    "url": "https://api.github.com",
    "ssl": true
  }
}
```

## Echo

Return request details — useful for debugging clients and load balancers.

```json
"backends": {
  "echo": {
    "enabled": true,
    "add_headers": {
      "X-Echo-Service": "true"
    },
    "response_delay_ms": 100
  }
}
```

## Mock

Serve canned JSON without a real upstream. Ideal for frontend development and contract tests.

```json
"backends": {
  "mock": {
    "enabled": true,
    "path_templates": {
      "/users": {
        "status_code": 200,
        "content_type": "application/json",
        "body": { "users": [{ "id": 1, "name": "Jane" }] }
      },
      "/users/{id}": {
        "status_code": 200,
        "body": { "id": "${path.id}", "name": "User ${path.id}" }
      }
    },
    "default_response": {
      "status_code": 404,
      "body": { "error": "Not found" }
    }
  }
}
```

See [Mock API for development](../use-cases/mock-api.md).

## Redirect

Send clients to another URL, optionally keeping the original path:

```json
"backends": {
  "redirect": {
    "enabled": true,
    "location": "https://api.github.com",
    "preserve_path": true
  }
}
```

## Command

Run a shell command and return its output (platform-specific; use with care in production):

```json
"backends": {
  "command": {
    "id": "diagnostics",
    "default": "echo ok"
  }
}
```

## Choosing a backend

| Need | Backend |
|------|---------|
| Call a real HTTP API | `https` |
| Stub responses during development | `mock` |
| Verify what the client sent | `echo` |
| Move traffic to a new host | `redirect` |
| Run a one-off diagnostic script | `command` |
