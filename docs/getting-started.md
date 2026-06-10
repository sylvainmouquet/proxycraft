# Getting started

## Install

=== "pip"

    ```bash
    pip install proxycraft
    ```

=== "uv"

    ```bash
    uv add proxycraft
    ```

## Run your first proxy

1. Create a config file `proxy.json` (see [Configuration](configuration.md) for the full schema).
2. Start the server:

```python
from proxycraft import ProxyCraft

if __name__ == "__main__":
    ProxyCraft(config_file="proxy.json").serve(host="0.0.0.0", port=8091)
```

3. Send a request:

```bash
curl http://localhost:8091/
```

ProxyCraft loads defaults from its built-in template when fields are omitted. For a full working example with registry mirrors, mocks, and caches, copy `proxycraft/features/configuration/default.json` from the repository.

## Choose an ASGI server

Set the server in your config:

```json
{
  "server": {
    "type": "gunicorn",
    "port": 8080
  }
}
```

Supported values: `gunicorn` (default), `uvicorn`, `hypercorn`.

## Enable HTTPS on the proxy

Terminate TLS at ProxyCraft by providing certificate paths:

```json
{
  "ssl": true,
  "server": {
    "type": "hypercorn",
    "port": 8443,
    "certfile": "/path/to/cert.pem",
    "keyfile": "/path/to/key.pem"
  }
}
```

## Docker

```bash
docker build -t proxycraft -f dockerfiles/proxycraft.Dockerfile .
docker run -p 8080:8080 -v $(pwd)/proxy.json:/app/proxy.json proxycraft
```

Mount your config and cache directories as volumes when running registry mirrors in production.

## Where to go next

- [Configuration](configuration.md) — structure of endpoints and middleware
- [Package registry mirror](use-cases/registry-mirror.md) — common DevOps use case
- [Deployment](deployment.md) — production tips
