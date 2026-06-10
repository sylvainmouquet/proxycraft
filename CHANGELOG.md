# Changelog

All notable changes to this project are documented in this file.

## Unreleased

### Added

- MkDocs user documentation (features, use cases, configuration, deployment)
- `just docs-build` and `just docs-serve` recipes; GitHub Actions workflow to build and publish docs
- `proxycraft/shared/utilities/http_compat.py` shim for `HTTPMethod` on Python 3.10
- `proxycraft/shared/utilities/path_compat.py` helper for `Path.is_file(follow_symlinks=...)` on Python 3.10 and 3.11
- Feature-based package layout under `proxycraft/features/`, `proxycraft/shared/`, and `proxycraft/app/`
- `docs/architecture.md` and ADR `docs/decisions/0001-feature-based-architecture.md`

### Changed

- Supported Python versions expanded from 3.13+ to 3.10 through 3.14
- Reorganized package from layer-based folders to `features/`, `shared/`, and `app/`
- Moved logging, utilities, connection pooling, and async file reader into `proxycraft/shared/`
- Moved configuration, routing, upstream backends, middleware, authentication, protocols, virtual upstream, and deployment into `proxycraft/features/`
- Co-located unit tests beside feature and shared modules
- Updated `SPECS.md`, `README.md`, and `pytest.ini` test discovery paths

### Fixed

### Removed
