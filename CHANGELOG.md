# Changelog

All notable changes to this project are documented in this file.

## Unreleased

### Added

- Feature-based package layout under `proxycraft/features/`, `proxycraft/shared/`, and `proxycraft/app/`
- `docs/architecture.md` and ADR `docs/decisions/0001-feature-based-architecture.md`

### Changed

- Reorganized package from layer-based folders to `features/`, `shared/`, and `app/`
- Moved logging, utilities, connection pooling, and async file reader into `proxycraft/shared/`
- Moved configuration, routing, upstream backends, middleware, authentication, protocols, virtual upstream, and deployment into `proxycraft/features/`
- Co-located unit tests beside feature and shared modules
- Updated `SPECS.md`, `README.md`, and `pytest.ini` test discovery paths

### Fixed

### Removed
