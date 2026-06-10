# Configuration

JSON-driven proxy configuration with typed Pydantic/dataclass models and file loading.

## Public API

- `Config` — root configuration model (`models.py`)
- `get_file_config(filepath)` — load and validate a JSON config file (`loader.py`)
- `default.json` — bundled registry-mirror preset examples

## Usage

```python
from proxycraft.features.configuration import Config, get_file_config

config = get_file_config("proxy.json")
# or
config = Config(**json_data)
```

Legacy imports `proxycraft.config.models` and `proxycraft.config.loader` remain available via compatibility shims during migration.

## Constraints

- Endpoints are sorted by `weight` (descending) on load
- `Config` uses Pydantic `BaseModel` for JSON parsing; nested types are mostly dataclasses
