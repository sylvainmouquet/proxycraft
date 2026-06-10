# ADR 0001: Feature-based architecture

## Status

Accepted

## Context

ProxyCraft was organized by technical layer (`middlewares/`, `networking/`, `upstreams/`, `security/`, `protocols/`). As features grew, the central `proxycraft.py` module became a god-object importing across all layers. Tests mirrored layer folders rather than living beside the code they validate.

Workspace rules require feature-based organization: code grouped by business capability with shared infrastructure extracted only when reused without business logic.

## Decision

Reorganize the Python package into:

- `proxycraft/features/` — capability-owned modules, tests, and docs
- `proxycraft/shared/` — logging, connection pooling, persistence helpers, utilities
- `proxycraft/app/` — thin composition root

Migrate in phases with re-export shims at legacy import paths (`proxycraft.config`, `proxycraft.middlewares`, etc.) until all callers are updated and shims are removed.

## Consequences

### Positive

- Clear ownership boundaries per capability
- Easier to locate and extend features
- Tests co-located with feature code
- Smaller, focused app composition module

### Negative

- Temporary duplication via compatibility shims during migration
- Import path churn in SPECS, README, and examples until cleanup completes

## Alternatives considered

**Keep layer-based layout** — Rejected; scales poorly and conflicts with project conventions.

**Big-bang migration** — Rejected; higher risk of breaking external importers; phased approach with shims is safer.
