# ProxyCraft task runner — see `just --list`

set shell := ["bash", "-eu", "-o", "pipefail", "-c"]

python_version := env_var_or_default('PYTHON_VERSION', '3.13')

default:
    @just --list

wip:
    git add .
    git commit -m "WIP: Work in progress"
    git push

install:
    uv sync --python {{python_version}} --all-extras --group dev

check-version:
    #!/usr/bin/env bash
    if [ -z "${VERSION:-}" ]; then
        echo "VERSION is not set. Please set the VERSION environment variable."
        exit 1
    fi

build: check-version
    rm -rf dist/* || true
    ./scripts/version.sh "${VERSION}"
    @grep version pyproject.toml
    @grep version proxycraft/__init__.py
    uv build --python {{python_version}}

check:
    PYRIGHT_PYTHON_FORCE_VERSION=latest uv run pyright

deploy:
    uvx twine upload dist/*

install-local:
    pip3 install dist/*.whl

test *args:
    uv run --python {{python_version}} pytest -v --log-cli-level=INFO {{args}}

lint:
    uv run ruff check --fix
    uv run ruff format
    uv run ruff format --check

update:
    uv lock --upgrade
    uv sync

check-deps:
    .venv/bin/pip list --outdated
