#!/usr/bin/env bash
set -euo pipefail

# Run from the repository root, or pass COMPOSE_FILE to select another file.
DIR="$( realpath $(dirname "${BASH_SOURCE[0]}")/../ )"
COMPOSE_FILE="${DIR}/docker-compose.yml"

if ! command -v docker >/dev/null 2>&1; then
    echo "Error: Docker is not installed or not on PATH." >&2
    exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
    echo "Error: Docker Compose v2 is required." >&2
    exit 1
fi



if ! python3 -c "import setuptools_scm" >/dev/null 2>&1; then
    echo "Warning: setuptools-scm is not installed in the active Python environment." >&2
    TMP_VENV="$(mktemp -d)"
    echo "Creating temp venv at ${TMP_VENV}"
    trap 'rm -rf "$TMP_VENV"' EXIT

    python3 -m venv "$TMP_VENV"
    source ${TMP_VENV}/bin/activate
    which python
    echo "Installing setuptools-scm" >&2
    pip3 install --quiet setuptools-scm
fi

# Keep the setuptools_scm version, replacing '+' because Docker tags do not allow it.
VERSION="$(python3 -m setuptools_scm)"
VERSION_LABEL="$(python3 -m setuptools_scm | tr '+' '-')"
export VERSION 
export VERSION_LABEL
export GIT_COMMIT="$(git rev-parse HEAD)"
docker compose -f "${COMPOSE_FILE}" config

echo "Building docker image"
docker compose -f "${COMPOSE_FILE}" build

echo "Built docker image"
