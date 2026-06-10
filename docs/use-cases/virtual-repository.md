# Local and remote aggregation

Serve packages from disk when you have them; otherwise fetch from a remote registry automatically. One URL for clients, no custom fallback code.

## Problem

You vendor some Python wheels internally but still need PyPI for everything else. Maintaining two index URLs in `pip.conf` is error-prone. You want **local first, remote second** transparently.

## Solution

Use [virtual upstream](../features/virtual-upstream.md) with `first-match`:

```json
[
  {
    "identifier": "pypi-demo-local",
    "prefix": "/pypi-demo-local",
    "match": "/pypi-demo-local/**",
    "upstream": {
      "file": {
        "enabled": true,
        "path": ".files/pypi/pypi-demo-local"
      }
    }
  },
  {
    "identifier": "pypi-remote-official",
    "prefix": "/pypi-remote-official",
    "match": "/pypi-remote-official/**",
    "backends": [{
      "https": [{ "url": "https://pypi.org/simple", "ssl": true }]
    }],
    "upstream": {
      "proxy": { "enabled": true },
      "cache": { "file": { "enabled": true, "path": ".cache/pypi" } }
    }
  },
  {
    "prefix": "/pypi-virtual-all",
    "match": "/pypi-virtual-all/**",
    "upstream": {
      "virtual": {
        "sources": ["pypi-demo-local", "pypi-remote-official"],
        "strategy": "first-match"
      }
    }
  }
]
```

## Client configuration

Point pip at the virtual endpoint only:

```bash
pip install my-internal-package --index-url http://mirror.internal:8080/pypi-virtual-all/simple
```

## Request flow

```text
pip → /pypi-virtual-all/my-package/
        ├─ try pypi-demo-local  → 200? return
        └─ else pypi-remote-official  → return (and cache)
```

## When to use it

- Approved packages on disk, everything else from upstream
- Staging a migration from remote-only to fully local
- Reducing bandwidth — hot packages never leave the LAN after the first remote fetch populates cache

## Related

- [Package registry mirror](registry-mirror.md)
- [Virtual upstream](../features/virtual-upstream.md)
