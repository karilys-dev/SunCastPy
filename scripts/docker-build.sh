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

setup_vars(){
    if [[ -z "${VERSION:-}" ]]; then
        if ! python3 -c "import setuptools_scm" >/dev/null 2>&1; then
            echo "Warning: setuptools-scm is not installed in the active Python environment." >&2
            TMP_VENV="$(mktemp -d)"
            echo "Creating temp venv at ${TMP_VENV}"
            trap 'rm -rf "$TMP_VENV"' EXIT

            python3 -m venv "$TMP_VENV"
            source ${TMP_VENV}/bin/activate

            echo "Installing setuptools-scm" >&2
            pip3 install --quiet setuptools-scm
        fi    
        VERSION="$(python3 -m setuptools_scm)"
        VERSION_LABEL="$(python3 -m setuptools_scm | tr '+' '-')"
    else
        VERSION_LABEL="$(echo ${VERSION} | tr '+' '-')"
    fi
    if [ "${GITHUB_REF_TYPE:-}" = "tag" ]; then
        echo "This is a tag: $GITHUB_REF_NAME"
        COMPOSE_FILE+=" -f ${DIR}/docker-compose.ci.yml"
    fi
    export VERSION 
    export VERSION_LABEL
    export GIT_COMMIT="${GIT_COMMIT:-$(git rev-parse HEAD)}"
    export BUILD_DATE="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
    export SOURCE_URL="${SOURCE_URL:-https://github.com/$(git config --get remote.origin.url | sed -E 's#.*github.com[:/]##; s#\.git$##')}"
}

config(){
    docker compose -f ${COMPOSE_FILE} config
}

build(){
    echo "Building docker image"
    docker compose -f ${COMPOSE_FILE} build
    echo "Built docker image"
}

push(){
    docker compose -f ${COMPOSE_FILE} push
}

github_action(){
    docker compose -f ${COMPOSE_FILE} build --push
}

usage() {
    echo "Usage: $(basename "$0") [-h help] [-c config] [-b build] [-p push] [-a github_action]" >&2
}

while getopts ":abcph" opt; do
    case $opt in
        a) setup_vars && github_action ;;
        c) setup_vars && config ;;
        b) setup_vars && build ;;
        p) setup_vars && push ;;
        h) usage ;;
        \?)
            echo "Error: Invalid option -$OPTARG" >&2
            exit 1
            ;;
  esac
done

shift $((OPTIND - 1))
if [[ $OPTIND -eq 1 ]]; then
    echo "Error: At least one option is required." >&2
    usage
    exit 1
fi