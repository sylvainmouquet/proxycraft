# Package registry mirror

Run PyPI, npm, Maven, GitHub, or Alpine package traffic through a single on-prem proxy. Builds stay fast, outbound bandwidth drops, and you control what gets cached.

## Problem

CI machines and developer laptops repeatedly download the same packages from the public internet. Registries rate-limit, links in index pages point at the official host, and air-gapped sites cannot reach upstream at all.

## Solution

ProxyCraft ships ready-made endpoint presets (see `default.json` in the repository) that:

1. Proxy requests to the official registry
2. Cache GET responses on disk
3. Rewrite URLs in index pages so clients stay on your mirror

## PyPI mirror

```json
{
  "identifier": "pypi-remote-official",
  "prefix": "/pypi-remote-official",
  "match": "/pypi-remote-official/**",
  "backends": [{
    "https": [{
      "id": "pypi-primary",
      "url": "https://pypi.org/simple",
      "weight": 10,
      "ssl": true
    }]
  }],
  "upstream": {
    "proxy": { "enabled": true, "timeout_seconds": 60 },
    "cache": {
      "file": {
        "enabled": true,
        "path": ".cache/pypi/pypi-remote-official",
        "ttl": 43200,
        "max_size_mb": 256
      }
    }
  },
  "transformers": {
    "response": {
      "enabled": true,
      "textReplacements": [
        {
          "oldvalue": "https://pypi.org/simple",
          "newvalue": "http://mirror.internal:8080/pypi-remote-official"
        }
      ]
    }
  }
}
```

Point pip at your mirror:

```bash
pip install requests --index-url http://mirror.internal:8080/pypi-remote-official/simple
```

## npm mirror

Same pattern with `https://registry.npmjs.org` as the upstream and replacements pointing at `/npm-remote-npmjs`.

```bash
npm config set registry http://mirror.internal:8080/npm-remote-npmjs/
```

## Maven mirror

Proxy `https://repo1.maven.org/maven2` under `/maven-remote-central` with file cache enabled. Configure Maven `settings.xml` mirrorOf central to your ProxyCraft URL.

## GitHub API cache

Use `/github-api` to gateway `https://api.github.com` — helpful when many runners share one egress IP and hit rate limits.

## Alpine packages

The `/alpine-remote-official` preset proxies `https://dl-cdn.alpinelinux.org/alpine` for APK-based images and builders.

## Production checklist

- Replace `mirror.internal:8080` with your real hostname in all `textReplacements`
- Mount `.cache/` on persistent storage in Docker or Kubernetes
- Enable [IP filtering](../features/security.md) so only build farms can reach the mirror
- Set `ttl` and `max_size_mb` to match how often packages update in your environment

## Related

- [Caching](../features/caching.md)
- [Response transformation](../features/response-transformation.md)
- [Local and remote aggregation](virtual-repository.md)
