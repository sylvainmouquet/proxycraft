# Path routing

ProxyCraft selects an **endpoint** for each request using Ant-style path patterns and optional weights.

## Match patterns

| Pattern | Matches |
|---------|---------|
| `/**` | Everything under the root |
| `/api/**` | Anything under `/api` |
| `/users/{id}` | `/users/42`, `/users/alice` |
| `/files/*.json` | `/files/config.json` |

Patterns use the same syntax as Spring's Ant path matcher.

## Weighted selection

When several endpoints could match, the one with the **highest** `weight` wins:

```json
[
  {
    "prefix": "/",
    "match": "**/*",
    "weight": 0,
    "backends": { "https": { "url": "https://fallback.example.com" } }
  },
  {
    "prefix": "/v2",
    "match": "/v2/**",
    "weight": 100,
    "backends": { "https": { "url": "https://api-v2.example.com" } }
  }
]
```

Traffic to `/v2/users` uses the v2 backend; everything else goes to the fallback.

## Identifiers for virtual upstreams

Give endpoints an `identifier` when other endpoints need to reference them:

```json
{
  "identifier": "pypi-remote-official",
  "prefix": "/pypi-remote-official",
  "match": "/pypi-remote-official/**",
  "backends": { "https": { "url": "https://pypi.org/simple" } }
}
```

Identifiers are required for [virtual upstream](virtual-upstream.md) `sources` lists.

## When to use it

- Route `/pypi/**` to a package mirror and `/api/**` to your application API on one port
- Pin a high-priority rule for admin paths while keeping a catch-all for public traffic
- Version APIs with `/v1/**` and `/v2/**` on the same proxy instance
