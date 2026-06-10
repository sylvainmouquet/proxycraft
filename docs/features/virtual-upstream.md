# Virtual upstream

Expose one URL that tries several backing endpoints in order until one succeeds.

## Configuration

```json
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
```

`sources` lists `identifier` values from other endpoints. With `first-match`, ProxyCraft tries each source internally; the first response with HTTP 200 wins.

## How it works

1. Client requests `/pypi-virtual-all/some-package/`
2. ProxyCraft tries `pypi-demo-local` first (e.g. files on disk)
3. If that returns non-200, it tries `pypi-remote-official` (remote PyPI mirror)
4. The winning response is returned to the client

No client-side fallback logic is required.

## When to use it

- **Hybrid registry** — serve vendored packages locally, pull anything else from upstream
- **Gradual migration** — keep a legacy endpoint as first source while a new backend warms up
- **Resilience** — prefer a fast internal cache endpoint before a slower remote mirror

See [Local and remote aggregation](../use-cases/virtual-repository.md) for a PyPI example.
