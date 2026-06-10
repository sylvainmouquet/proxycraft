# Security filtering

Control who can reach your proxy with IP and User-Agent filters. Rules use Ant-style patterns and apply globally through `middlewares.security`.

## IP filter

Block or allow clients by IP address or CIDR-style patterns:

```json
"middlewares": {
  "security": {
    "ip_filter": {
      "enabled": true,
      "blacklist": ["*.0.0.2", "203.0.113.0/24"]
    }
  }
}
```

## Bot filter

Match crawlers and scrapers by User-Agent string:

```json
"bot_filter": {
  "enabled": true,
  "blacklist": [
    {
      "name": "googlebot",
      "user-agent": "*googlebot*"
    }
  ],
  "whitelist": []
}
```

Use `whitelist` to explicitly allow agents that would otherwise match a blacklist rule.

## When to use it

- **Internal package mirror** — allow only your CI subnet and office IP ranges
- **Public API gateway** — block known bad bots while keeping browsers and approved tools
- **Staging environment** — restrict access before go-live

!!! note
    Inbound authentication (Digest, NTLM, Kerberos) is on the roadmap. Today, filtering is IP- and User-Agent-based.
