# Response transformation

Rewrite text inside upstream responses so clients see URLs that point back to your proxy instead of the original host.

## Text replacements

```json
"transformers": {
  "response": {
    "enabled": true,
    "textReplacements": [
      {
        "oldvalue": "https://pypi.org/simple",
        "newvalue": "http://mirror.internal:8080/pypi-remote-official"
      },
      {
        "oldvalue": "/simple",
        "newvalue": "/pypi-remote-official"
      }
    ]
  }
}
```

Rules run in order. Each `oldvalue` is replaced with `newvalue` in the response body.

## Why it matters for mirrors

Package registries embed their own URLs in HTML index pages. Without rewriting, `pip`, `npm`, or Maven would follow links back to the public internet instead of your mirror.

Typical replacements:

| Registry | Replace |
|----------|---------|
| PyPI | `https://pypi.org/simple` → your mirror base URL |
| npm | `https://registry.npmjs.org` → your mirror base URL |
| GitHub API | `https://api.github.com` → your gateway path |

## When to use it

- [Package registry mirror](../use-cases/registry-mirror.md) — mandatory for PyPI simple index and npm metadata
- **API gateway** — rewrite documentation links in proxied HTML (use carefully)
- **Legacy app migration** — swap old domain strings in responses during a cutover

!!! tip
    Set `newvalue` to the hostname and path your clients actually use (`http://mirror.internal:8080/...`), not `0.0.0.0`.
